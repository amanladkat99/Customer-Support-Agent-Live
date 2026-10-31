from __future__ import annotations

import logging
from typing import Any

from customer_support_agent.core.settings import Settings

logger = logging.getLogger(__name__)

try:
    from mem0 import Memory
except ImportError:
    Memory = None

class CustomerMemoryStore:

    # mem0 normally calls an LLM internally to "extract" facts from messages
    # before storing them (infer=True). On Groq free tier the extraction prompt
    # alone can exceed the 8 000 TPM limit for available models, causing a 413.
    # Setting infer=False stores the summarised content directly without an
    # extra LLM round-trip, which is reliable and still fully searchable.
    _INFER_MEMORIES = False

    # Hard-cap characters per message role to keep stored content concise.
    _MAX_MSG_CHARS = 600

    def __init__(self, settings:Settings, llm:Any):
        if Memory is None:
            raise RuntimeError("mem0ai is not installed. Install dependencies with `uv sync`.")
        _ = llm

        config: dict[str, Any] = {
            "llm": {
                "provider": "groq",
                "config": {
                    "model": settings.groq_model,
                    "api_key": settings.groq_api_key,
                    "temperature": settings.llm_temperature,
                },
            },
            "vector_store": {
                "provider": "chroma",
                "config": {
                    "path": str(settings.chroma_mem0_path),
                },
            },
        }

        if settings.google_api_key:
            config["embedder"] = {
                "provider": "gemini",
                "config": {
                    "api_key": settings.google_api_key,
                    "model": settings.effective_google_embedding_model,
                },
            }

        elif settings.openai_api_key:
            config["embedder"] = {
                "provider": "openai",
                "config": {
                    "api_key": settings.openai_api_key,
                },
            }

        elif settings.enable_local_embeddings:
            config["embedder"] = {
                "provider": "huggingface",
                "config": {
                    "model": "all-MiniLM-L6-v2",
                },
            }

        else:
            raise RuntimeError(
                "No embedding provider configured for Mem0. Set GOOGLE_API_KEY (recommended) "
                "or OPENAI_API_KEY. Set ENABLE_LOCAL_EMBEDDINGS=true to use local HuggingFace embeddings."
            )

        self._memory = Memory.from_config(config)

    def search(self, query: str, user_id: str, limit: int = 5) -> list[dict[str, Any]]:
        # mem0 >= 2.0: user_id is passed via filters={}; top_k replaces limit.
        logger.debug("memory.search user_id=%s limit=%d query=%r", user_id, limit, query[:80])
        try:
            raw = self._memory.search(
                query,
                filters={"user_id": user_id},
                top_k=limit,
            )
        except TypeError:
            # Fallback for older mem0 builds that still accept positional kwargs.
            raw = self._memory.search(query, user_id=user_id, limit=limit)
        results = self._normalize_results(raw, limit)
        logger.debug("memory.search returned %d results for user_id=%s", len(results), user_id)
        return results

    def list_memories(self, user_id: str, limit: int = 20) -> list[dict[str, Any]]:
        if hasattr(self._memory, "get_all"):
            # mem0 >= 2.0: user_id via filters={}; top_k replaces limit.
            try:
                raw = self._memory.get_all(
                    filters={"user_id": user_id},
                    top_k=limit,
                )
            except TypeError:
                raw = self._memory.get_all(user_id=user_id)
            return self._normalize_results(raw, limit)

    def add_interaction(
        self,
        user_id: str,
        user_input: str,
        assistant_response: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        messages = [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": assistant_response},
        ]

        self._add_messages(messages=messages, user_id=user_id, metadata=metadata)

    def add_resolution(
        self,
        user_id: str,
        ticket_subject: str,
        ticket_description: str,
        accepted_draft: str,
        entity_links: list[str] | None = None,
    ) -> None:
        entity_text = ""
        if entity_links:
            entity_text = "\nLinked entities: " + ", ".join(entity_links)

        messages = [
            {
                "role": "user",
                "content": f"Ticket subject: {ticket_subject}\nProblem: {ticket_description}",
            },
            {
                "role": "assistant",
                "content": (
                    "Resolution accepted by support agent:\n"
                    f"{accepted_draft}{entity_text}"
                ),
            },
        ]

        metadata = {"type": "resolution"}

        self._add_messages(messages=messages, user_id=user_id, metadata=metadata)

    def _add_messages(
        self,
        messages: list[dict[str, str]],
        user_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        # Truncate each message to stay within Groq TPM limits for the
        # lightweight extraction model used by mem0 internally.
        safe_messages = [
            {
                "role": msg["role"],
                "content": msg["content"][: self._MAX_MSG_CHARS],
            }
            for msg in messages
        ]
        logger.debug("memory.add user_id=%s messages=%d", user_id, len(safe_messages))
        try:
            result = self._memory.add(
                safe_messages,
                user_id=user_id,
                metadata=metadata or {},
                infer=self._INFER_MEMORIES,
            )
            logger.debug("memory.add result: %s", result)
        except TypeError:
            self._memory.add(safe_messages, user_id=user_id)
        except Exception:
            logger.exception("memory.add failed for user_id=%s", user_id)
            raise


    def _normalize_results(self, raw: Any, limit: int) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []

        if isinstance(raw, dict) and "results" in raw:
            iterable = raw.get("results") or []
        elif isinstance(raw, list):
            iterable = raw
        else:
            iterable = []

        for entry in iterable[:limit]:
            if isinstance(entry, dict):
                memory_text = entry.get("memory") or entry.get("content") or ""
                if memory_text:
                    items.append(
                        {
                            "memory": memory_text,
                            "score": entry.get("score"),
                            "metadata": entry.get("metadata") or {},
                        }
                    )
            elif entry:
                items.append({"memory": str(entry), "score": None, "metadata": {}})

        return items
