from __future__ import annotations


def llm_answer(question: str, context: str) -> str:
    return f"LLM answer: {question}\nContext: {context[:200]}"
