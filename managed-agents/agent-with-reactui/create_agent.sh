curl --request POST \
  --url https://api.trugen.ai/v1/ext/agent \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: <TRUGEN_API_KEY>' \
  --data @- <<EOF
{
  "agent_name": "Custom Support Agent",
  "agent_system_prompt": "Speak in a warm, engaging tone and provide clear answers. Assist the user with any issues that the user has been facing with the issue.",
  "config": {
    "timeout": 240
  },
  "knowledge_base": null,
  "record": false,
  "callback_url": null,
  "callback_events": null,
  "avatars": [
    {
      "avatar_key_id": "665a1170",
      "config": {
        "llm": {
          "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
          "provider": "groq"
        },
        "stt": {
          "model": "flux-general-en",
          "provider": "deepgram-v2",
          "min_endpointing_delay": 0.3,
          "max_endpointing_delay": 0.4
        },
        "tts": {
          "model_id": "eleven_turbo_v2_5",
          "provider": "elevenlabs",
          "voice_id": "ZUrEGyu8GFMwnHbvLhv2"
        },
        "turn_detector": true
      },
      "idle_timeout": {
        "timeout": 30,
        "filler_phrases": [
          "Hey it's been a while since we last spoke, are you still connected?",
          "I notice we haven't talked for a bit, is everything okay?"
        ]
      },
      "welcome_message": {
        "wait_time": 2,
        "messages": [
          "Hi, how are you doing today?",
          "Hello, how can I help you?"
        ]
      },
      "warning_exit_message": {
        "callout_before": 10,
        "messages": [
          "We are almost at the end of our call, thank you for your time.",
          "Thank you for your time. We will see you next time."
        ]
      },
      "exit_message": {
        "max_call_duration": 180,
        "messages": [
          "We are at the end of our call, hope I was able to help you.",
          "Thank you for your time today."
        ]
      }
    }
  ]
}
EOF
