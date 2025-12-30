# Using the Agent via Static HTML

This project also supports interacting with an existing agent using a simple static HTML file.
No React, build tools, or server setup is required.

---

## Prerequisites

- A modern web browser (Chrome, Edge, or Firefox)
- An existing **Agent ID**
- An `index.html` file already present in the project

---

## Step 1: Open the `index.html` File

Locate the existing `index.html` file in the project root.

```text
index.html
````

This file embeds the agent using an `<iframe>`.

---

## Step 2: Update Agent and User Configuration

Inside `index.html`, locate the configuration section in the `<script>` block:

```html
<script>
  const agentId = "YOUR_AGENT_ID_HERE";
  const userName = "USER_NAME_HERE";
  const userId = "USER_ID_HERE";
  const conversationContext = "CONVERSATION_CONTEXT_HERE";
</script>
```

Replace the placeholder values with actual data:

* **Agent ID** → ID of the existing agent
* **User Name** → Display name of the user
* **User ID** → Unique user identifier (email or user ID)
* **Conversation Context** → Initial context for the agent

### Example

```html
<script>
  const agentId = "4b7165c3-f297-414c-82f8-49da0a01632c";
  const userName = "Jane";
  const userId = "jane@trugen.ai";
  const conversationContext =
    "User is having trouble with her Xbox 360, it is showing a red ring and doesn't boot.";
</script>
```

Save the file after updating.

---

## Step 3: Open the HTML File in a Browser

Open the file directly in your browser:

```bash
open index.html
```

Or simply double-click the file.

The embedded agent will load automatically and start the conversation using the provided context.

---

## Notes

* No server is required — this works as a static file
* Camera and microphone permissions will be requested by the browser
* Refresh the page to restart the session

---

## Troubleshooting

### Agent Does Not Load

* Verify the Agent ID is correct
* Ensure the iframe URL is not blocked by browser extensions
* Try opening the file in a new browser window

### Camera or Microphone Not Working

* Confirm browser permissions are enabled
* Use HTTPS if hosting the file remotely

---
