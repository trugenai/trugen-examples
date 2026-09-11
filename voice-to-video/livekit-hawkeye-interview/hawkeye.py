"""Hawkeye-1 vision monitoring for LiveKit rooms.

Attaches a TruGen Hawkeye-1 vision session to the agent's room via
``POST /v2/vision`` and consumes the alerts Hawkeye publishes on the
``hawkeye-events`` data-channel topic. Raw events are dumped to a JSONL file
and kept in memory; look-away style events are counted over a sliding window
and trigger a spoken warning through the agent when a threshold is exceeded.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

import httpx
from livekit import rtc

logger = logging.getLogger("hawkeye")

DEFAULT_WARNING_MESSAGE = (
    "I noticed you have been looking away from the camera. "
    "Please stay focused on our conversation."
)

DATA_TOPIC = "hawkeye-events"

MODULES = {
    "face_pose_detection": ["Looking Left", "Looking Right"],
    "eyegaze_tracking": ["Looking left", "Looking right"],
    "face_out_of_focus": ["out_of_frame"],
    "face_count": ["2", "3", "4"],
}

ATTENTION_CLASSES = {
    "face_pose_detection": {"Looking Left", "Looking Right"},
    "eyegaze_tracking": {"Looking left", "Looking right"},
    "face_out_of_focus": {"out_of_frame"},
    "face_count": {"2", "3", "4"},
}

AGENT_IDENTITY_PREFIXES = ("trugen-avatar", "hawkeye-vision")


class HawkeyeClient:
    """Starts Hawkeye-1 vision sessions against the TruGen API."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self._api_key = api_key or os.getenv("TRUGEN_API_KEY", "")
        self._base_url = (base_url or os.getenv("TRUGEN_API_BASE_URL", "https://api.trugen.ai")).rstrip("/")

    def room_join_token(self, room_name: str, identity: str = "hawkeye-vision-agent") -> str:
        from livekit import api as lk_api

        token = lk_api.AccessToken(
            os.getenv("LIVEKIT_API_KEY"),
            os.getenv("LIVEKIT_API_SECRET"),
        ).with_identity(identity).with_name("Hawkeye Vision").with_grants(
            lk_api.VideoGrants(room_join=True, room=room_name, can_publish_data=True)
        )
        return token.to_jwt()

    async def start_session(
        self,
        room: rtc.Room,
        *,
        participant: str = "auto",
        max_duration: int = 30,
        modules: dict[str, list[str]] | None = None,
    ) -> dict | None:
        """Attach Hawkeye-1 to ``room``. Returns the session payload or None."""
        if not self._api_key:
            logger.error("TRUGEN_API_KEY is not set, cannot start a Hawkeye session")
            return None

        body = {
            "livekit_url": os.getenv("LIVEKIT_URL"),
            "access_token": self.room_join_token(room.name),
            "participant": participant,
            "max_duration": max_duration,
            "modules": modules or MODULES,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            for attempt in range(3):
                try:
                    resp = await client.post(
                        f"{self._base_url}/v2/vision",
                        json=body,
                        headers={"x-api-key": self._api_key, "Content-Type": "application/json"},
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        logger.info("Hawkeye session accepted: %s", data)
                        return data
                    logger.error(
                        "Hawkeye session rejected (%s): %s", resp.status_code, resp.text
                    )
                    if resp.status_code in (400, 401, 403):
                        return None
                except Exception:
                    logger.exception("failed to start Hawkeye session (attempt %s)", attempt + 1)
                await asyncio.sleep(2**attempt)

        logger.error("giving up on Hawkeye session after retries")
        return None


class HawkeyeMonitor:
    """Consumes ``hawkeye-events`` data packets and enforces the focus policy."""

    def __init__(
        self,
        *,
        session,
        room: rtc.Room,
        threshold: int | None = None,
        window_seconds: float | None = None,
        cooldown_seconds: float | None = None,
        warning_message: str | None = None,
    ) -> None:
        self._session = session
        self._room = room
        self.threshold = threshold or int(os.getenv("HAWKEYE_LOOKAWAY_THRESHOLD", "3"))
        self.window_seconds = window_seconds or float(os.getenv("HAWKEYE_WINDOW_SECONDS", "60"))
        self.cooldown_seconds = cooldown_seconds or float(os.getenv("HAWKEYE_COOLDOWN_SECONDS", "45"))
        self.warning_message = warning_message or os.getenv(
            "HAWKEYE_WARNING_MESSAGE", DEFAULT_WARNING_MESSAGE
        )

        self._attention: deque[tuple[float, str, str]] = deque()
        self._events: deque[dict] = deque(maxlen=1000)
        self._counts: dict[tuple[str, str], int] = {}
        self._last_warning_ts = 0.0
        self._warnings = 0
        self._tasks: set[asyncio.Task] = set()

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._dump_path = Path("logs") / f"hawkeye_events_{room.name}_{stamp}.jsonl"

    def start(self) -> None:
        self._room.on("data_received")(self._on_data)
        logger.info(
            "Hawkeye monitor armed: threshold=%s events / %ss window, cooldown=%ss",
            self.threshold,
            self.window_seconds,
            self.cooldown_seconds,
        )

    def shutdown_summary(self) -> dict:
        summary = json.loads(self.report_text())
        logger.info("Hawkeye session summary: %s", json.dumps(summary))
        logger.info("raw event dump written to %s", self._dump_path)
        return summary

    def _on_data(self, packet: rtc.DataPacket) -> None:
        if packet.topic != DATA_TOPIC:
            return
        try:
            event = json.loads(packet.data.decode("utf-8"))
        except Exception:
            logger.exception("failed to decode hawkeye event")
            return

        record = {"received_at": datetime.now(timezone.utc).isoformat(), "event": event}
        self._events.append(record)
        try:
            self._dump_path.parent.mkdir(parents=True, exist_ok=True)
            with self._dump_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
        except Exception:
            logger.exception("failed to write hawkeye event dump")

        payload = event.get("payload", {})
        trigger = payload.get("trigger", {})
        module = trigger.get("module") or payload.get("module", "unknown")
        cls = trigger.get("class") or payload.get("class", "unknown")
        logger.info("hawkeye raw event: %s", json.dumps(event))

        self._counts[(module, cls)] = self._counts.get((module, cls), 0) + 1

        if cls in ATTENTION_CLASSES.get(module, set()):
            self._register_attention(module, cls)

    def _register_attention(self, module: str, cls: str) -> None:
        now = time.monotonic()
        self._attention.append((now, module, cls))
        while self._attention and now - self._attention[0][0] > self.window_seconds:
            self._attention.popleft()

        if len(self._attention) < self.threshold:
            return
        if now - self._last_warning_ts < self.cooldown_seconds:
            return

        self._last_warning_ts = now
        self._warnings += 1
        count = len(self._attention)
        self._attention.clear()
        logger.warning(
            "focus threshold exceeded (%s events in %ss), issuing warning #%s",
            count,
            self.window_seconds,
            self._warnings,
        )
        task = asyncio.create_task(self._warn(count))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    async def _warn(self, count: int) -> None:
        try:
            await self._session.say(self.warning_message, allow_interruptions=True)
        except Exception:
            logger.exception("failed to deliver focus warning")

    @property
    def warnings_issued(self) -> int:
        return self._warnings

    def report_text(self) -> str:
        """Compact JSON summary for the interviewer LLM."""
        now = time.monotonic()
        recent = sum(1 for ts, _, _ in self._attention if now - ts <= self.window_seconds)
        counts = {f"{m}/{c}": n for (m, c), n in sorted(self._counts.items())}
        last = self._events[-1]["event"] if self._events else None
        return json.dumps(
            {
                "total_events": sum(self._counts.values()),
                "counts_by_module_and_class": counts,
                "attention_events_last_window": recent,
                "window_seconds": self.window_seconds,
                "threshold": self.threshold,
                "warnings_issued": self._warnings,
                "last_event": last,
                "raw_event_dump": str(self._dump_path),
            }
        )
