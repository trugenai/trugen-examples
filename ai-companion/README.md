# Using the Agent via Static HTML (AI Companion)

This example embeds an existing TruGen agent into a simple static `index.html` file (no React, no build tools, no server).

It does *not* require any `companion.js`—it loads the widget directly from `https://dist.trugen.ai/trugen-chat.js`.

---

## Prerequisites

- A modern web browser (Chrome, Edge, or Firefox)
- Your TruGen **Agent ID**
- Your TruGen **widget `apiKey`** (from your TruGen dashboard)

---

## Step 1: Update `agentId` and `apiKey`

Open `ai-companion/index.html` and update the widget config:

```html
<script>
  window.TrugenWidget = {
    agentName: "Knowledge Base Assistant",
    agentId: "REPLACE_WITH_YOUR_AGENT_ID",
    apiKey: "REPLACE_WITH_YOUR_API_KEY",
    heading: "Ask anything from your docs",
    subHeading: "Powered by your Knowledge Base"
  };
</script>
```

Save the file after updating.

---

## Step 2: Open in a Browser

You can open it directly:

- Double-click `index.html`, or
- Right-click `index.html` -> Open with -> your browser

If the page is hosted remotely, serve it over `https`.

---

## Troubleshooting

### Agent Does Not Load

- Verify `agentId` and `apiKey` are correct
- Hard refresh the page
- If scripts are blocked by browser settings/extensions, allow scripts for this page and reload

