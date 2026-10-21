import json
import os

from dotenv import load_dotenv
from openai import APIConnectionError, OpenAI

from tools import TOOLS, run_tool
from Utilities.utilities import log

load_dotenv()  # by default looks for .env file

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
)

# Safety limit: the max number of model rounds for ONE user question
MAX_STEPS = 5

# This list stores the whole chat, so the model remembers earlier messages
messages = [
    {
        "role": "system",
        "content": "Act like a very humble agent and respond always under 10 words.",
    }
]


def save_output():
    """Save the full chat into output.json"""
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)


def get_reply():
    """Ask the model. If it wants a tool, run the tool and ask again."""
    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools=TOOLS,
        )
        msg = response.choices[0].message

        # No tool needed: this is the final answer
        if not msg.tool_calls:
            reply = msg.content or ""
            messages.append({"role": "assistant", "content": reply})
            return reply

        # Model asked for tools: save its request, then run each tool
        messages.append(msg.model_dump(exclude_none=True))
        for tool_call in msg.tool_calls:
            result = run_tool(tool_call)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )

    # Too many rounds, stop here
    fallback = "Sorry, I could not finish that. Please try again."
    messages.append({"role": "assistant", "content": fallback})
    return fallback


# Chat loop starts from here
while True:
    try:
        user_input = input("\n🧑 SujalVerma: ")
    except (KeyboardInterrupt, EOFError):
        user_input = "exit"

    if not user_input.strip():
        continue

    if user_input.lower().strip() in ["exit", "quit", "bye", "goodbye"]:
        save_output()
        print("Assistant: Bye! Take care.")
        break

    chat_size = len(messages)  # to undo this turn if something fails
    messages.append({"role": "user", "content": user_input})

    try:
        reply = get_reply()
    except APIConnectionError:
        del messages[chat_size:]
        print("Assistant: Cannot reach the model. Start Ollama with 'ollama serve' and try again.")
        continue
    except Exception as e:
        del messages[chat_size:]
        log(f"Error: {e}")
        print(f"Assistant: Something went wrong ({e}).")
        continue

    save_output()
    print("🤖 Assistant: " + reply)