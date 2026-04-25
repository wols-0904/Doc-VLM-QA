from __future__ import annotations

from doc_vlm_qa.ui.gradio_app import create_app


if __name__ == "__main__":
    app = create_app()
    app.launch()
