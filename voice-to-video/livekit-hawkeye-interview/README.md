# Hawkeye Interviewer — LiveKit Voice Agent + TruGen Avatar + Focus Monitoring

An AI-Engineer interview agent for LiveKit with:

- **A face** — [TruGen](https://trugen.ai) **Huma-2** avatar via the official `livekit-agents[trugen]` plugin.
- **A watcher** — [TruGen **Hawkeye-1**](https://docs.trugen.ai/docs/models/hawkeye-1) vision analysis attached to the room via `POST /v2/vision`. Hawkeye joins as a subscriber, watches the candidate's camera, and publishes every detection to the room's `hawkeye-events` data-channel topic.
- **Focus enforcement** — the agent consumes `hawkeye-events` directly (no callback server needed), dumps every raw event to a JSONL file and the console log, counts look-away events over a sliding window, and when the threshold is exceeded interrupts through the avatar: *"I noticed you have been looking away from the camera. Please stay focused on our conversation."*

```
┌──────────────────────────────── LiveKit Room ────────────────────────────────┐
│   Candidate (Agent Console / Agents Playground)                              │
│        │  mic + camera                                                       │
│        ▼                                                                     │
│   Interview agent (agent.py)                                                 │
│     ├── STT (deepgram/nova-3) ── LLM (gpt-4.1-mini) ── TTS (inworld-tts-2)   │
│     │        (LiveKit Inference, no extra provider keys)                     │
│     ├── trugen.AvatarSession ──► Huma-2 face (video participant)             │
│     ├── HawkeyeMonitor ── room.on("data_received", topic="hawkeye-events")   │
│     │     ├── raw log ──► console (`INFO hawkeye: hawkeye raw event: {...}`) │
│     │     ├── raw dump ──► logs/hawkeye_events_<room>_<ts>.jsonl             │
│     │     └── sliding window ──► session.say("please stay focused...")       │
│     └── POST /v2/vision ──► attaches Hawkeye-1 to this room                  │
│            (participant locked to the candidate's LiveKit SID)               │
│                                                                              │
│   Hawkeye-1 worker ── analyzes candidate video ──► publishes hawkeye-events  │
└──────────────────────────────────────────────────────────────────────────────┘
```

## How the focus monitoring works

Hawkeye publishes each detection to the room's `hawkeye-events` data topic as a
`trigger` event, for example:

```json
{
  "type": "trigger",
  "payload": {
    "session_id": "de60936b-...-u1",
    "timestamp": "2026-09-11T18:47:12.005573+00:00",
    "trigger": {
      "module": "face_pose_detection",
      "class": "Looking Right",
      "count": 2,
      "condition": {"type": "count", "op": "gt", "value": 1},
      "actions": [{"type": "message", "content": "Looking Right"}]
    }
  }
}
```

The monitor (`hawkeye.py`) reads `payload.trigger.module` / `payload.trigger.class`
and treats the attention classes as look-aways: `face_pose_detection`
(`Looking Left` / `Looking Right`), `eyegaze_tracking` (`Looking left` /
`Looking right`), `face_out_of_focus` (`out_of_frame`) and `face_count` (`2`+).
Each trigger event counts as one event; when **3** accumulate within the sliding
window the agent interrupts the candidate via `session.say`, then observes a
cooldown before it may warn again. Events outside the attention classes
(e.g. emotions) are counted for reporting but never trigger a warning.

## Prerequisites

- Python 3.10+ and [uv](https://docs.astral.sh/uv/getting-started/installation/)
- A [LiveKit Cloud](https://cloud.livekit.io) project (free tier is fine)
- A TruGen API key from [app.trugen.ai](https://app.trugen.ai) (Developers → API keys)
  - Note: Hawkeye Vision Understanding is enterprise-only on TruGen. Without vision
    access the interview agent still works; only the focus monitoring will log an
    auth/credits error.

## Setup

```bash
cp .env.example .env.local   # then fill in your keys
uv sync
```

Environment variables (`.env.local`):

| Variable | Description |
| --- | --- |
| `LIVEKIT_URL` / `LIVEKIT_API_KEY` / `LIVEKIT_API_SECRET` | LiveKit Cloud project credentials |
| `TRUGEN_API_KEY` | TruGen API key from app.trugen.ai (needs Hawkeye/Vision access) |
| `TRUGEN_AVATAR_ID` | Optional stock avatar (default `7d881c1b`), pick more at [docs.trugen.ai/docs/avatars/gallery](https://docs.trugen.ai/docs/avatars/gallery) |
| `HAWKEYE_MAX_DURATION` | Hawkeye session cap in minutes (default `30`) |
| `HAWKEYE_LOOKAWAY_THRESHOLD` | Look-away events needed to trigger a warning (default `3`) |
| `HAWKEYE_WINDOW_SECONDS` | Sliding window for the threshold (default `60`) |
| `HAWKEYE_COOLDOWN_SECONDS` | Minimum time between warnings (default `45`) |
| `HAWKEYE_WARNING_MESSAGE` | Override the spoken warning text |

## Run

```bash
lk agent dev                 # recommended (hot-reload)
# or, without the LiveKit CLI:
uv run python agent.py dev   # dev mode is deprecated upstream, still works
```

Then open the **Agent Console** for your project ([cloud.livekit.io](https://cloud.livekit.io)
→ Agents → Console, or [agents-playground.livekit.io](https://agents-playground.livekit.io)),
allow **camera + mic**, and start a session. You will see and hear the TruGen avatar
interviewer; your camera feed is what Hawkeye analyzes.

Try it: answer a couple of questions, then repeatedly glance off-screen. After **3**
look-away events within 60 seconds the interviewer interrupts and asks you to stay
focused, then stays quiet for at least 45 seconds before it can warn you again.

### What you get

- **Raw vision event log** — every Hawkeye event is logged to the console
  (`INFO hawkeye: hawkeye raw event: {...}`) and appended to
  `logs/hawkeye_events_<room>_<timestamp>.jsonl`, plus a bounded in-memory buffer.
- **Spoken focus warnings** — 3 look-away trigger events within the 60s window
  (configurable), delivered via `session.say` so the avatar lipsyncs it, with a
  45s cooldown between warnings. The warning is added to the chat context, so the
  interviewer LLM knows it happened.
- **Attention report tool** — the interviewer LLM can call `get_attention_report`
  and will use it in the closing feedback (e.g. "you looked away 12 times…"). It
  returns total counts per module/class, events in the current window, warnings
  issued, and the last raw event. A final summary is also logged at session
  shutdown.

## Troubleshooting

- `Hawkeye session rejected (402): insufficient credits: need N, have M` — your TruGen
  account is out of credits for the 1¢/min vision sessions. Top up on the TruGen
  developer platform; the interview still runs without monitoring.
- `Hawkeye session rejected (401/403)` — your `TRUGEN_API_KEY` doesn't have Vision
  enabled (enterprise feature). The interview still runs without monitoring.
- `rejected (502)` — transient backend rejection, the client retries with backoff.
- No video/face — check `TRUGEN_API_KEY` and that the `trugen-avatar` participant
  appears in the room's participant list.
- `python agent.py dev` requires `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`
  in `.env.local` (same values as your LiveKit project's API keys page).