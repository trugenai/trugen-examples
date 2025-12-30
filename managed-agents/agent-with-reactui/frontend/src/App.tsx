export function App() {
  const agentId = "4b7165c3-f297-414c-82f8-49da0a01632c";
  const userName = "Jane";
  const userId = "jane@trugen.ai";
  const conversationContext =
    "User is having trouble with her Xbox 360, it is showing a red ring and doesn't boot.";

  const baseUrl = "https://app.trugen.ai/embed";
  const params = new URLSearchParams({
    username: userName,
    id: userId,
    context: conversationContext,
  });

  const iframeSrc = `${baseUrl}/${agentId}?${params.toString()}`;

  return (
    <div className="app">
      <h1>TruGen.AI - Customer Support Agent</h1>

      {/* Agent iFrame */}
      <div style={{ width: "100%", height: "900px" }}>
        <iframe
          src={iframeSrc}
          title="TruGen AI Agent"
          width="100%"
          height="100%"
          allow="camera; microphone; fullscreen; display-capture"
          allowFullScreen
          loading="lazy"
          sandbox="allow-scripts allow-same-origin"
          style={{ border: "none" }}
        />
      </div>
    </div>
  );
}

export default App;
