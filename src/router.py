from __future__ import annotations

import os

import openai
from dotenv import load_dotenv


load_dotenv()

ROUTE_KEYWORDS = ["图", "表", "截图", "公式", "布局"]


def route_query(query: str) -> str:
    """基于规则路由查询类型。"""
    return "multimodal" if any(word in query for word in ROUTE_KEYWORDS) else "text"


def _build_context_text(retrieved_contexts: list[dict]) -> str:
    parts: list[str] = []
    for ctx in retrieved_contexts:
        page_id = ctx.get("page_id", "?")
        text = ctx.get("chunk_text") or ctx.get("text") or ""
        text = str(text).strip()
        if text:
            parts.append(f"[第{page_id}页] {text}")
    return "\n\n".join(parts)


def generate_text_answer(query: str, retrieved_contexts: list[dict]) -> str:
    """基于检索上下文调用 LLM 生成答案。"""
    context_text = _build_context_text(retrieved_contexts)

    system_prompt = (
        "你是一个课程问答助手。请仅基于我提供的文档上下文来回答用户问题。"
        "如果上下文中没有相关信息，请直接回答‘文档中未提及’。"
        "在回答的每个段落末尾，必须附加上证据所在的页码，格式如 [第X页]。"
    )

    user_prompt = (
        f"文档上下文：\n{context_text if context_text else '（无可用上下文）'}\n\n"
        f"用户问题：{query}"
    )

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("OPENAI_MODEL", "qwen-plus")

    if not api_key:
        raise ValueError("未配置 OPENAI_API_KEY")

    try:
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
    except openai.OpenAIError:
        return "文档中未提及"
    if not response.choices:
        return "文档中未提及"
    return response.choices[0].message.content or "文档中未提及"
