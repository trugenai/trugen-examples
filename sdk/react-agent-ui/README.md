# TruGen Agent UI — React Integration Guide

This repository is a working example of how to embed a TruGen AI agent into a React application using the `@trugen/agent-ui` package.

---

## Prerequisites

- Node.js 18 or later
- A TruGen **API Key** and **Agent ID** — find these in your [TruGen dashboard](https://trugen.ai)
- React 19 or later in your project

---

## Running This Example

```bash
npm install
npm run dev
```

Open [http://localhost:3001](http://localhost:3001), enter your API Key and Agent ID, and click **Connect**.

---

## Adding the Agent to Your Own React App

### 1. Install the package

```bash
npm install @trugen/agent-ui
# or
yarn add @trugen/agent-ui
# or
pnpm add @trugen/agent-ui
```

### 2. Import the component and its styles

```tsx
import { TrugenAgentProvider, TrugenAgent } from "@trugen/agent-ui";
import "@trugen/agent-ui/dist/index.css";
```

The CSS import is required — it includes the component's layout and theme styles.

### 3. Render the agent

Wrap `TrugenAgent` with `TrugenAgentProvider` and pass your credentials:

```tsx
import { TrugenAgentProvider, TrugenAgent } from "@trugen/agent-ui";
import "@trugen/agent-ui/dist/index.css";

export default function App() {
  return (
    <TrugenAgentProvider>
      <div style={{ height: "100vh", width: "100vw" }}>
        <TrugenAgent
          agentId="your-agent-id-here"
          apiKey="your-api-key-here"
        />
      </div>
    </TrugenAgentProvider>
  );
}
```

The agent fills whatever container you give it — size the wrapper to fit your layout.

---

## API Reference

### `TrugenAgentProvider`

A context provider that supplies theme and session settings to all child agent components. Place it once near the top of your component tree, or just around the section that renders a `TrugenAgent`.

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `children` | `React.ReactNode` | Yes | The components to wrap |

### `TrugenAgent`

The main agent interface component. Handles audio/video via LiveKit and the full conversational experience.

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `agentId` | `string` | Yes | The unique ID of the agent from your TruGen dashboard |
| `apiKey` | `string` | Yes | Your TruGen API key |
| `context` | `string` | No | Optional text passed to the agent at session start |

---

## Letting Users Supply Their Own Credentials

If you want users to enter their own API Key and Agent ID (as this example does), manage them as state and pass them to `TrugenAgent` once both are provided:

```tsx
import { useState } from "react";
import { TrugenAgentProvider, TrugenAgent } from "@trugen/agent-ui";
import "@trugen/agent-ui/dist/index.css";

export default function App() {
  const [apiKey, setApiKey] = useState("");
  const [agentId, setAgentId] = useState("");
  const [connected, setConnected] = useState(false);

  if (!connected) {
    return (
      <div>
        <input
          type="password"
          placeholder="API Key"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />
        <input
          type="text"
          placeholder="Agent ID"
          value={agentId}
          onChange={(e) => setAgentId(e.target.value)}
        />
        <button
          disabled={!apiKey || !agentId}
          onClick={() => setConnected(true)}
        >
          Connect
        </button>
      </div>
    );
  }

  return (
    <TrugenAgentProvider>
      <div style={{ height: "100vh", width: "100vw" }}>
        <TrugenAgent apiKey={apiKey} agentId={agentId} />
      </div>
    </TrugenAgentProvider>
  );
}
```

---

## Notes

- `@trugen/agent-ui` requires **React 19 or later** as a peer dependency.
- The package uses client-side rendering — it is not compatible with server-side rendering (SSR) or React Server Components.
- With npm v7+, peer dependencies (`react`, `react-dom`) are installed automatically. On npm v6, install them manually.

---

## Support

Visit [trugen.ai](https://trugen.ai) or reach out through your TruGen dashboard for help with API keys, agent configuration, or billing.
