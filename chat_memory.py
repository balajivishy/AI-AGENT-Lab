# chat_memory.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

# Load .env if present
load_dotenv()

# Init OpenAI client (will read OPENAI_API_KEY from env or .env)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MEMORY_FILE = "memory.json"
SYSTEM_PROMPT = (
    "You are a helpful, concise assistant. Remember user preferences and context across the conversation. "
    "If the conversation gets long, keep the important facts and preferences and forget trivial chatter."
)

# --- helpers to load/save memory ---
def load_memory() -> List[Dict]:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # Default starting messages (system role + empty history)
    return [{"role": "system", "content": SYSTEM_PROMPT}]

def save_memory(messages: List[Dict]):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

# --- simple summarization/compression to keep memory small ---
def compress_memory_if_needed(messages: List[Dict], max_messages: int = 40) -> List[Dict]:
    """
    If messages length > max_messages, summarize the older part and replace it with a short summary.
    Keeps the system prompt and the most recent messages intact.
    """
    if len(messages) <= max_messages:
        return messages

    # keep system prompt, keep last N recent messages, summarize the middle chunk
    system = messages[0]
    recent_keep = 10
    to_summarize = messages[1 : -recent_keep]  # exclude system and last recent_keep elements
    if not to_summarize:
        return messages

    # Build summarization prompt
    concat = []
    for m in to_summarize:
        role = m.get("role", "user")
        content = m.get("content", "")
        concat.append(f"{role.upper()}: {content}")

    summarize_prompt = (
        "Please produce a short, factual summary (3-6 bullet points) of the following conversation. "
        "Keep user preferences, facts, and outstanding action items. Be concise.\n\n"
        + "\n".join(concat)
    )

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": summarize_prompt}],
            temperature=0.0,
            max_tokens=300,
        )
        summary = resp.choices[0].message.content.strip()
        # rebuild messages: system + summary-as-assistant + last recent_keep messages
        new_messages = [system, {"role": "assistant", "content": f"Memory summary:\n{summary}"}] + messages[-recent_keep:]
        return new_messages
    except Exception as e:
        # if summarization fails, just return original messages to avoid data loss
        print("⚠️ Summarization failed:", e)
        return messages

# --- main loop ---
def main():
    messages = load_memory()
    print(f"🤖 Agent with persistent memory ready. ({len(messages)} messages loaded)")
    print("Type 'exit' or 'quit' to stop. Type 'reset memory' to wipe saved memory (except system prompt).")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("👋 Goodbye!")
            break

        if user_input.lower() == "reset memory":
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            save_memory(messages)
            print("🗑️ Memory reset (kept system prompt).")
            continue

        # Add user message to history
        messages.append({"role": "user", "content": user_input})

        # Compress history if needed
        messages = compress_memory_if_needed(messages, max_messages=40)

        # Ask model with full current history
        try:
            print("📡 Sending request...")
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )
            assistant_text = resp.choices[0].message.content
            print("Agent:", assistant_text)
            # Append assistant reply to history and persist
            messages.append({"role": "assistant", "content": assistant_text})
            save_memory(messages)
        except Exception as e:
            print("❌ Error while calling API:", e)

if __name__ == "__main__":
    main()
