from __future__ import annotations


def build_rag_prompt(question: str, evidence: list[str]) -> str:
    context = "\n".join(f"- {item}" for item in evidence)
    return f"你是课程文档问答助手。\n问题：{question}\n证据：\n{context}"
