import 'dotenv/config';

import { defineAgent, cli, ServerOptions, voice } from '@livekit/agents';
import * as openai from '@livekit/agents-plugin-openai';
import * as trugen from '@livekit/agents-plugin-trugen';
import { fileURLToPath } from 'url';
console.log("Avatar ID:", process.env.TRUGEN_AVATAR_ID);
export default defineAgent({
  entry: async (ctx) => {

    console.log(" Agent starting...");

    // 1. Create agent 
    const agent = new voice.Agent({
      instructions: `
        You are a friendly AI assistant.
        Keep responses short and clear.
      `,
    });

    // 2. Create session (OpenAI realtime)
    const session = new voice.AgentSession({
      llm: new openai.realtime.RealtimeModel({
        voice: 'alloy',
      }),
    });

    // 3. Connect to LiveKit
    await ctx.connect();

    // 4. Start agent
    await session.start({
      agent,
      room: ctx.room,
    });

    console.log(" Agent connected to room");

    // 5. Try to start Trugen avatar 
    try {
      const avatar = new trugen.AvatarSession({
        avatarId: process.env.TRUGEN_AVATAR_ID,
      });

      await avatar.start(session, ctx.room);
      console.log(" Avatar started");

    } catch (e) {
      console.log(" Avatar failed (ignored):", e.message);
    }

    // 6. Greeting
    session.generateReply({
      instructions: 'Say: Hello! I am your AI assistant. How can I help you today?',
    });

  },
});

// Run app
cli.runApp(new ServerOptions({
  agent: fileURLToPath(import.meta.url),
}));