# LiveKit Agent with TruGen Realtime Avatar

A voice AI assistant built with LiveKit Agents featuring **TruGen.AI** real-time video avatars.

This example demonstrates how to integrate a real-time photo-realistic avatar into your LiveKit voice pipeline with interruption handling and conversational capabilities.

---

## Features

- **Real-Time Video Avatar**: Seamlessly connect your LiveKit session with TruGen.AI avatars.
- **Interruption Support**: Automatically dispatches interrupt RPCs to the avatar worker on overlapping speech.
- **Stock & Custom Avatars**: Choose from pre-configured stock avatars or generate your own custom avatar from a single photograph.
- **Multi-Model Pipeline**: Support for Deepgram STT, Google Gemma LLM, Cartesia TTS, and Google Realtime.

---

## Setup

### 1. Install Dependencies

Using [`uv`](https://docs.astral.sh/uv/):

```bash
uv sync
```

### 2. Configure Environment

Copy the example environment file to `.env`:

```bash
cp .env.example .env
```

Set the following variables in `.env`:

```bash
# LiveKit Cloud Credentials
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-livekit-api-key
LIVEKIT_API_SECRET=your-livekit-api-secret

# TruGen Config
TRUGEN_API_KEY=your-trugen-api-key
TRUGEN_AVATAR_ID=25da4417
```

---

## Run the Agent

Start the agent in development mode (with hot reload):

```bash
uv run agent.py dev
```

Or start for production:

```bash
uv run agent.py start
```

---

## Available Stock Avatars

You can use any of the following built-in stock avatars by setting `TRUGEN_AVATAR_ID` in your `.env` file:

| Avatar | ID | Gender |
|--------|-----|--------|
| Lisa | `25da4417` | Female |
| Lucy | `e4fabd5b` | Female |
| Mike | `c24c6359` | Male |
| Jessica | `647f7a13` | Female |
| Jason | `6a72a69e` | Male |
| Clara | `ae511ecf` | Female |
| Cathy | `bf96ff2c` | Female |
| Chloe | `ae47ac37` | Female |
| Alex | `d6b5da08` | Male |

---

## Custom Avatars

In addition to stock avatars, you can create your own custom avatar from a single photo using the TruGen API and use its `avatar_id` in your LiveKit agent.

### Documentation & Best Practices

- **Guide**: [Creating a custom avatar](https://docs.trugen.ai/docs/avatars/custom)
- **Guide**: [Best practices for source photos](https://docs.trugen.ai/docs/avatars/best-practices)

Before generating a custom avatar, ensure your source photo meets these requirements:
- Front-facing and looking directly at the camera with a neutral expression.
- High resolution: 1024x1024 or higher (JPG, PNG, or WebP up to 10MB).
- Evenly lit with minimal shadows across the face.
- Head and upper shoulders clearly visible.
- No accessories obstructing facial features (e.g. sunglasses, hats, heavy filters).
- Explicit consent if using a photograph of another individual.

### 1. Create a Custom Avatar (cURL)

Encode your source photo to base64 and make a `POST` request to the TruGen Custom Avatar API:

```bash
# Base64-encode your source image
IMAGE_B64=$(base64 -i ./my-photo.jpg)

# Call the TruGen Custom Avatar API
curl -X POST https://api.trugen.ai/v2/custom-avatar \
  -H "x-api-key: $TRUGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "avatar_id": "my-custom-avatar-01",
    "avatar_name": "My Custom Avatar",
    "gender": "female",
    "input_image": "data:image/jpeg;base64,'"$IMAGE_B64"'",
    "is_private": true
  }'
```

The response returns confirmation and the registered `avatar_id`.

### 2. Use the Custom Avatar ID

Set `TRUGEN_AVATAR_ID` in your `.env` or pass the ID directly when instantiating `AvatarSession` in `agent.py`:

```python
# Initialize Avatar Session with custom avatar ID
avatar = trugen.AvatarSession(
    avatar_id="my-custom-avatar-01",  # Your custom avatar ID
    api_key=os.getenv("TRUGEN_API_KEY"),
)
await avatar.start(session, room=ctx.room)
```

---

## Testing Your Avatar

1. Start your agent worker:
   ```bash
   uv run agent.py dev
   ```
2. Open the [LiveKit Agents Playground](https://agents-playground.livekit.io/).
3. Connect using the same LiveKit project credentials (`LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`).
4. Join the room to interact with your real-time video avatar.

---

## Docker Deployment

Build and run using Docker:

```bash
# Build Docker image
docker build -t trugen-livekit-agent .

# Run container with environment variables
docker run --env-file .env trugen-livekit-agent
```
