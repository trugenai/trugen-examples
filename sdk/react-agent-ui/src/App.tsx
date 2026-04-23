import { useState } from "react";
import { TrugenAgentProvider, TrugenAgent } from "@trugen/agent-ui";
import "@trugen/agent-ui/dist/index.css";
import "./App.css";

export default function App() {
  const [apiKey, setApiKey] = useState("");
  const [agentId, setAgentId] = useState("");
  const [connected, setConnected] = useState(false);

  return (
    <div className="layout">
      <div className="center">
        {connected ? (
          <div className="agent-card">
            <TrugenAgentProvider>
              <TrugenAgent apiKey={apiKey} agentId={agentId} />
            </TrugenAgentProvider>
          </div>
        ) : (
          <div className="connect-card">
            <div className="card-header">
              <span className="brand-mark">TRUGEN</span>
            </div>

            <h1 className="card-title">Connect<br />your Agent</h1>

            <div className="field">
              <label className="field-label" htmlFor="apiKey">API KEY</label>
              <div className="input-wrap">
                <input
                  id="apiKey"
                  className="field-input"
                  type="password"
                  placeholder="tg-••••••••••••••••"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  autoFocus
                />
              </div>
            </div>

            <div className="field">
              <label className="field-label" htmlFor="agentId">AGENT ID</label>
              <div className="input-wrap">
                <input
                  id="agentId"
                  className="field-input"
                  type="text"
                  placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                  value={agentId}
                  onChange={(e) => setAgentId(e.target.value)}
                  onKeyDown={(e) =>
                    e.key === "Enter" && apiKey.trim() && agentId.trim() && setConnected(true)
                  }
                />
              </div>
            </div>

            <button
              className="btn-primary"
              disabled={!apiKey.trim() || !agentId.trim()}
              onClick={() => setConnected(true)}
            >
              <span>Connect</span>
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
        )}
      </div>

      <footer className="footer">
        Powered by{" "}
        <a href="https://trugen.ai" target="_blank" rel="noreferrer">
          TruGen.AI
        </a>
      </footer>
    </div>
  );
}
