import asyncio
import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    TurnHandlingOptions,
    cli,
    inference,
)

# Import TruGen.AI plugin
from livekit.plugins import trugen

logger = logging.getLogger("huma_3_avatar_agent")

load_dotenv()

AGENT_NAME = "huma_3_avatar_agent"
INSTRUCTIONS = (Path(__file__).parent / "prompt.md").read_text()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=INSTRUCTIONS)


server = AgentServer()


@server.rtc_session(agent_name=AGENT_NAME)
async def huma_3_avatar_agent(ctx: JobContext) -> None:
    ctx.log_context_fields = {"room": ctx.room.name}
    session = AgentSession(
        stt=inference.STT("deepgram/flux-general-en", language="en"),
        llm=inference.LLM("google/gemma-4-31b-it"),
        tts=inference.TTS(
            "cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"
        ),
        turn_handling=TurnHandlingOptions(
            turn_detection=inference.TurnDetector(version="v1"),
            interruption={"mode": "adaptive"},
            preemptive_generation={"enabled": True},
        ),
        expressive=False,
    )

    # Register overlapping_speech handler to send interrupt RPC to avatar worker
    _avatar_interrupt_tasks: set[asyncio.Task] = set()

    async def _send_avatar_interrupt_rpc() -> None:
        try:
            await ctx.room.local_participant.perform_rpc(
                destination_identity="trugen_avatar",
                method="interrupt",
                payload=json.dumps({}),
            )
        except Exception as e:
            logger.warning("Failed to send interrupt RPC to avatar: %s", e)

    def _on_overlapping_speech(event) -> None:
        if event.is_interruption:
            task = asyncio.create_task(_send_avatar_interrupt_rpc())
            _avatar_interrupt_tasks.add(task)
            task.add_done_callback(_avatar_interrupt_tasks.discard)

    session.on("overlapping_speech", _on_overlapping_speech)

    # Initialize Avatar Session
    avatar_id = os.getenv("TRUGEN_AVATAR_ID") or "25da4417"
    api_key = os.getenv("TRUGEN_API_KEY")

    avatar = trugen.AvatarSession(
        avatar_id=avatar_id,
        api_key=api_key,
    )
    await avatar.start(session, room=ctx.room)

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(agent=Assistant(), room=ctx.room)
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(server)
