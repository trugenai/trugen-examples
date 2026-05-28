# Using the Agent via Static HTML (FAQ Agent)

This project also supports interacting with an existing agent using a simple static HTML file.
No React, build tools, or server setup is required.

---

## Prerequisites

- A modern web browser (Chrome, Edge, or Firefox)
- An existing **Agent ID**
- An `apiKey` value required by the TruGen widget (from your TruGen dashboard)
- An `index.html` file already present in the project

---

## Step 1: Open the `index.html` File

Locate the existing `index.html` file in the project root.

```text
index.html
```

This file embeds the agent using the TruGen widget script.

---

## Step 2: Update Agent and Widget Configuration

Inside `index.html`, locate the configuration section in the `<script>` block:

```html
<script>
  window.TrugenWidget = {
    agentName: "FAQ Assistant",
    agentId: "YOUR_AGENT_ID_HERE",
    apiKey: "YOUR_WIDGET_API_KEY_HERE",
    heading: "Ask our FAQ",
    subHeading: "Get answers from our help center",
    logoUrl: "YOUR_LOGO_URL_HERE",
    displayAvatarUrl: "YOUR_AVATAR_URL_HERE"
  };
</script>
```

Replace the placeholder values with actual data:

- **Agent ID** -> ID of the existing TruGen agent
- **apiKey** -> TruGen widget key
- **logoUrl / displayAvatarUrl** -> publicly reachable image URLs

Save the file after updating.

---

## Step 3: Open the HTML File in a Browser

Open the file directly in your browser:

```bash
open index.html
```

Or simply double-click the file.

The embedded agent will load automatically and start the conversation.

---

## Notes

- No server is required if you open the file locally.
- If you host the files remotely, ensure the page is served over `https`.
- Refresh the page to restart the widget session.

---

## Troubleshooting

### Agent Does Not Load

- Verify the `agentId` is correct
- Verify the `apiKey` is correct
- Try opening the page in a new browser window (disable extensions that block scripts)

### Widget Styling Issues

- Hard refresh the page
- Ensure `logoUrl` and `displayAvatarUrl` are publicly reachable

