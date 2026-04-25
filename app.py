from __future__ import annotations

from pathlib import Path

import gradio as gr

from src.parser import parse_pdf


def _parse_and_preview(pdf_file: str | None) -> tuple[str, str, str | None]:
    if not pdf_file:
        return "请先上传 PDF 文件。", "", None

    try:
        parsed = parse_pdf(pdf_file)
        if not parsed:
            return "未解析到任何页面。", "", None

        first_page = parsed[0]
        image_path = Path(first_page["image_path"])
        if not image_path.is_absolute():
            image_path = Path(__file__).resolve().parent / image_path

        status = f"成功解析 {len(parsed)} 页！"
        return status, str(first_page.get("text", "")), str(image_path)
    except Exception as exc:
        return f"解析失败：{exc}", "", None


with gr.Blocks(title="Doc-VLM-QA PDF 解析系统") as demo:
    gr.Markdown("""
# Doc-VLM-QA 文档解析系统
上传 PDF 后，系统将提取每页文本并渲染图片，右侧展示第 1 页结果。
""")

    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="上传 PDF 文件", file_types=[".pdf"], type="filepath")
            parse_btn = gr.Button("开始解析", variant="primary")

        with gr.Column(scale=2):
            status_text = gr.Textbox(label="系统提示信息", interactive=False)
            first_page_text = gr.Textbox(label="第一页提取文本", lines=16, interactive=False)
            first_page_image = gr.Image(label="第一页图片", type="filepath")

    parse_btn.click(
        fn=_parse_and_preview,
        inputs=[file_input],
        outputs=[status_text, first_page_text, first_page_image],
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=6006)
