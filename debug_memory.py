"""
Quick diagnostic: add a test memory then immediately search for it.
Run with:  uv run python debug_memory.py
"""
from __future__ import annotations

import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logging.getLogger("chromadb").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

from customer_support_agent.core.settings import get_settings
from customer_support_agent.integrations.memory.mem0_store import CustomerMemoryStore

settings = get_settings()
print(f"\n=== Settings ===")
print(f"  groq_model:             {settings.groq_model}")
print(f"  google_api_key set:     {bool(settings.google_api_key)}")
print(f"  openai_api_key set:     {bool(settings.openai_api_key)}")
print(f"  chroma_mem0_path:       {settings.chroma_mem0_path}\n")

store = CustomerMemoryStore(settings=settings, llm=None)

TEST_USER = "debug-test@example.com"
QUERY     = "login issue password reset"

print("=== Step 1: Adding test memory ===")
store.add_interaction(
    user_id=TEST_USER,
    user_input="I cannot log in, I forgot my password.",
    assistant_response="We have sent a password-reset link to your registered email.",
)
print("add_interaction() completed.\n")

print("=== Step 2: Searching memories ===")
results = store.search(query=QUERY, user_id=TEST_USER, limit=5)
print(f"search() returned {len(results)} result(s)")
for i, r in enumerate(results, 1):
    print(f"  [{i}] score={r.get('score')}  memory={r.get('memory', '')[:120]}")

print("\n=== Step 3: Listing all memories for user ===")
all_mems = store.list_memories(user_id=TEST_USER, limit=20)
print(f"list_memories() returned {len(all_mems or [])} item(s)")
for i, r in enumerate(all_mems or [], 1):
    print(f"  [{i}] {r.get('memory', '')[:120]}")

