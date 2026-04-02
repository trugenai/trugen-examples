# LiveKit + TruGen Agent Example

Simple Node.js example that runs a LiveKit voice agent and starts a TruGen avatar session in the same room.

## Project Structure

- `agent.js`: Agent entrypoint (LiveKit + OpenAI realtime + TruGen avatar session)
- `.env.example`: Required environment variables template
- `package.json`: Project scripts and dependencies

## Prerequisites

- Node.js 18+
- A LiveKit Cloud project
- A TruGen account and avatar ID
- An OpenAI API key

## Setup

1. Install dependencies:

```bash
npm install
```

2. Copy env template and set your credentials:

```bash
# macOS/Linux
cp .env.example .env

# Windows PowerShell
Copy-Item .env.example .env
```

3. Update `.env` values.

## Run

```bash
npm start
```

## Notes

- `agent.js` creates a voice session using OpenAI realtime model (`alloy` voice).
- If avatar startup fails, the agent still runs (error is logged and ignored).
- Never commit your real `.env` file to GitHub.
