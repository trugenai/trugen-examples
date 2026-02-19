# LiveKit TruGen.AI Realtime Avatar

This example demonstrates how to create a realtime avatar session for your Livekit Voice Agents using [TruGen Developer Studio](https://app.trugen.ai/).

Select your avatar [list](https://docs.trugen.ai/docs/avatars/overview)

## Usage

### Update the environment:

```bash
# TruGen Config
export TRUGEN_API_KEY="..."

export TRUGEN_AVATAR_ID="..." (optional)

# Google config (or other models, tts, stt)
export GOOGLE_API_KEY="..."

# LiveKit config
export LIVEKIT_API_KEY="..."
export LIVEKIT_API_SECRET="..."
export LIVEKIT_URL="..."
```

#### Example Avatar Ids
- c5b563de - Female
- 7d881c1b - Female
- be5b2ce0 - Male
- 48d778c9 - Male

### Install depdencies:
```bash
uv sync
```

### Start the agent worker:

```bash
uv run agent_worker.py dev
```
Note: agent_worker.py is a simple example of a Livekit agent, feel free to change this with your own agent worker.

## Test your avatar:
- Launch [Livekit Agent Playgroun](https://agents-playground.livekit.io/) and sign in with the same Livekit credentials
- Click on `connect` and talk to your avatar.
