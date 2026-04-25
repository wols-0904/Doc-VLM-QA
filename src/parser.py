from __future__ import annotations

from pathlib import Path

import fitz


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = PROJECT_ROOT / "cache"
ALLOWED_BASE_DIRS = [PROJECT_ROOT, Path("/tmp"), Path("/var/tmp")]


def parse_pdf(pdf_path: str) -> list[dict]:
    """解析 PDF：提取每页文本并渲染页面图片。"""
    pdf_file = Path(pdf_path).expanduser()
    if pdf_file.suffix.lower() != ".pdf":
        raise ValueError(f"仅支持 PDF 文件: {pdf_path}")

    try:
        pdf_file = pdf_file.resolve(strict=True)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"PDF 文件不存在: {pdf_path}") from exc

    if not any(pdf_file.is_relative_to(base) for base in ALLOWED_BASE_DIRS):
        raise ValueError("PDF 文件路径不在允许目录中")
    if not pdf_file.is_file():
        raise FileNotFoundError(f"PDF 文件不存在: {pdf_path}")

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []

    try:
        with fitz.open(pdf_file) as doc:
            for page_idx, page in enumerate(doc, start=1):
                text = page.get_text("text")
                image_name = f"page_{page_idx}.png"
                image_abs_path = CACHE_DIR / image_name
                pix = page.get_pixmap()
                pix.save(image_abs_path)
                try:
                    image_rel_path = image_abs_path.relative_to(PROJECT_ROOT)
                except ValueError:
                    image_rel_path = Path("cache") / image_name

                results.append(
                    {
                        "page_id": page_idx,
                        "text": text,
                        "image_path": str(image_rel_path),
                    }
                )
    except fitz.FileDataError as exc:
        raise ValueError(f"PDF 文件损坏或无法解析: {pdf_path}") from exc
    except PermissionError as exc:
        raise ValueError(f"没有权限读取 PDF 文件: {pdf_path}") from exc
    except RuntimeError as exc:
        raise ValueError(f"PDF 处理失败: {pdf_path}") from exc

    return results
