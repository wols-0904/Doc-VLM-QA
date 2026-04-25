from __future__ import annotations

import gradio as gr

from doc_vlm_qa.pipeline.orchestrator import run_pipeline


def _answer(question: str, pages: int | float | None) -> str:
    try:
        normalized_pages = max(0, int(pages if pages is not None else 0))
    except (TypeError, ValueError):
        normalized_pages = 0
    result = run_pipeline(question=question, num_files=1, total_pages=normalized_pages)
    cites = ", ".join(str(p) for p in result.citations) if result.citations else "无"
    return f"{result.answer}\n\n引用页码: {cites}"


def create_app() -> gr.Blocks:
    with gr.Blocks(title="Doc-VLM-QA") as demo:
        gr.Markdown("# Doc-VLM-QA")
        question = gr.Textbox(label="问题")
        pages = gr.Number(label="总页数", value=1, precision=0)
        answer = gr.Textbox(label="回答", lines=8)
        btn = gr.Button("提交")
        btn.click(fn=_answer, inputs=[question, pages], outputs=[answer])
    return demo
