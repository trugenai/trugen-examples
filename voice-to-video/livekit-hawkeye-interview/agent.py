"""AI Engineer interview voice agent with a TruGen avatar and Hawkeye focus monitoring.

Talk to it from https://agents-playground.livekit.io after running:
    uv run python agent.py dev
"""

import asyncio
import logging
import os
import time

from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    RunContext,
    TurnHandlingOptions,
    function_tool,
    inference,
)
from livekit.plugins import trugen

from hawkeye import AGENT_IDENTITY_PREFIXES, HawkeyeClient, HawkeyeMonitor

load_dotenv(".env.local")
load_dotenv()

logger = logging.getLogger("interviewer")

AVATAR_ID = os.getenv("TRUGEN_AVATAR_ID") or "7e95996"

INTERVIEW_INSTRUCTIONS = """
You are Hawkeye, an AI Engineering interviewer conducting a live technical
interview with a candidate over a video call. This interview is monitored for
engagement and focus by a vision system.

## Personality
- Warm, professional and encouraging. You want the candidate to succeed.
- Speak in short, natural sentences. This is a voice conversation: no
  formatting, no emojis, no lists longer than two items.

## Format
1. Greet the candidate, introduce yourself, and explain the format: about 15
   minutes, a handful of AI engineering questions, spoken answers.
2. Ask their name and a one-minute intro of their AI engineering experience.
3. Work through the question bank below in order. Ask one question at a time,
   listen, give a brief acknowledgment, and ask at most one follow-up per
   topic. Skip topics they clearly covered in their intro.
4. Once every topic is done, call get_attention_report and then give closing
   feedback covering both technical answers and focus/engagement.

## Question bank
- Python: how would you process a multi-GB log file without loading it into memory?
- ML fundamentals: bias vs variance; what do you do when a model overfits?
- LLMs: RAG vs fine-tuning — how do you decide between them?
- Prompting: how do you reduce hallucinations in a customer-facing assistant?
- System design: sketch a voice AI interview platform (STT, LLM, TTS, streaming).
- Production: how would you evaluate and monitor an LLM agent in production?

## Focus monitoring
A Hawkeye vision system watches the candidate's camera and counts look-away
events. When you receive a focus warning, gently remind the candidate to look
into the camera and stay engaged — never shame them. Mention engagement
observations naturally, for example in the closing feedback.
"""


class Interviewer(Agent):
    def __init__(self, monitor: HawkeyeMonitor) -> None:
        super().__init__(instructions=INTERVIEW_INSTRUCTIONS)
        self._monitor = monitor

    @function_tool
    async def get_attention_report(self, context: RunContext) -> str:
        """Get the candidate's attention and focus report, including look-away
        counts and warnings issued by the Hawkeye vision system. Call this
        before final feedback or whenever you want to comment on engagement."""
        return self._monitor.report_text()


async def _pick_candidate_sid(room: rtc.Room, timeout: float = 10.0) -> str:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        for participant in room.remote_participants.values():
            if not participant.identity.startswith(AGENT_IDENTITY_PREFIXES):
                return participant.sid
        await asyncio.sleep(0.5)
    return "auto"


server = AgentServer()


@server.rtc_session(agent_name="interviewer")
async def entrypoint(ctx: agents.JobContext) -> None:
    logger.info("hawkeye-interviewer starting in room %s", ctx.room.name)

    session = AgentSession(
        stt=inference.STT(model="deepgram/nova-3", language="multi"),
        llm=inference.LLM(model="openai/gpt-4.1-mini"),
        tts=inference.TTS(model="inworld/inworld-tts-2", voice="Ashley"),
        turn_handling=TurnHandlingOptions(turn_detection=inference.TurnDetector()),
    )

    avatar = trugen.AvatarSession(avatar_id=AVATAR_ID)
    await avatar.start(session, room=ctx.room)

    monitor = HawkeyeMonitor(session=session, room=ctx.room)
    await session.start(room=ctx.room, agent=Interviewer(monitor))

    monitor.start()

    candidate = await _pick_candidate_sid(ctx.room)
    logger.info("hawkeye participant lock: %s", candidate)
    await HawkeyeClient().start_session(
        ctx.room,
        participant=candidate,
        max_duration=int(os.getenv("HAWKEYE_MAX_DURATION", "300")),
    )

    async def _log_summary() -> None:
        monitor.shutdown_summary()

    ctx.add_shutdown_callback(_log_summary)

    await session.generate_reply(
        instructions="Greet the candidate, introduce yourself as the AI engineering "
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
