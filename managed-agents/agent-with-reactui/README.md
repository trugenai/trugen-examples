# Agent Creation & React Integration

This repository shows how to create a Customer Support Video Agent using a bash script and connect it using a React application.

---

## Prerequisites

Ensure the following tools are installed on your system:

* **Bun**
* **Bash** (macOS, Linux, or WSL on Windows)

Verify Bun installation:

```bash
bun --version
```

---

## Project Structure

```text
.
├── create_agent.sh        # Bash script to create a new agent
├── frontend/              # React app (created using Bun)
│   ├── src/
│   │   └── App.tsx
└── README.md
```

---

## Step 1: Create the Agent

The agent is created using a bash script via the TruGen.AI API.

### 1.1 Make the Script Executable

```bash
chmod +x create_agent.sh
```

### 1.2 Run the Script

```bash
./create_agent.sh
```

After successful execution, the script will output an **Agent ID**, for example:

```text
{
  "id": "045302f0-9783-4ff2-846e-3888fb2a7894",
  "message": "Agent created successfully"
}
```

**Copy this Agent ID** — it will be used in the React app.

---

## Step 2: Install Frontend Dependencies (Bun)

Navigate to the React frontend directory and install all dependencies using **Bun**.

```bash
cd frontend
bun install
```

This will install all required packages and generate a `bun.lockb` file.

> 💡 If you encounter dependency issues later, you can safely delete `node_modules` and `bun.lockb`, then re-run `bun install`.

---

## Step 3: Configure Agent and User Details in the React App

Open the main React component where the agent iFrame is configured.

```ts
// frontend/src/App.tsx

const agentId = "YOUR_AGENT_ID_HERE";
const userName = "USER_NAME_HERE";
const userId = "USER_ID_HERE";
const conversationContext = "CONVERSATION_CONTEXT_HERE";
```

Replace the placeholders with actual values:

* `agentId` → Agent ID generated in **Step 1**
* `userName` → Display name of the user
* `userId` → Unique identifier for the user (email or user ID)
* `conversationContext` → Initial conversational context for the agent

### Example

```ts
const agentId = "4b7165c3-f297-414c-82f8-49da0a01631c";
const userName = "Jane";
const userId = "jane@trugen.ai";
const conversationContext =
  "User is having trouble with her Xbox 360, it is showing a red ring and doesn't boot.";
```

Save the file after updating the values.

---

## Step 4: Run the React Application

Start the development server using **Bun**:

```bash
bun run dev
```

The application should now be running, and the embedded agent will load with the configured user details and conversational context.

---

## Troubleshooting

### Permission Denied When Running Script

```bash
chmod +x create_agent.sh
```

### Agent Not Connecting

* Verify the Agent ID is correct
* Restart the Bun dev server
* Ensure `.env` variables are loaded correctly

### React App Fails to Start

* Confirm Bun is installed and up to date
* Reinstall dependencies:

```bash
rm -rf node_modules bun.lockb
bun install
```

---
