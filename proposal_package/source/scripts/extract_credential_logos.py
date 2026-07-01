from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image

ROOT = Path(r"C:\Users\ansar\Downloads\presidency\proposal_package")
SRC = Path(r"C:\Users\ansar\Downloads\blutrace")

FILES = {
    "dpiit": SRC / "DIPP266429_BLUETRACE_TECHNOLOGIES_PRIVATE_LIMITED_RECOGNITION_2763114265465494817.pdf",
    "udyam": SRC / "Print _ Udyam Registration Certificate.pdf",
    "mca": SRC / "INC-34_1-25411283954.pdf",
}

# Relative crop rectangles as (x0, y0, x1, y1) in fractions of page dimensions.
# Tuned to pick visible official marks from each certificate.
CROPS = {
    "dpiit": (0.70, 0.05, 0.95, 0.24),
    "udyam": (0.30, 0.01, 0.70, 0.17),
    "mca": (0.30, 0.01, 0.70, 0.20),
}

OUT = {
    "dpiit": ROOT / "startup_india_logo.png",
    "udyam": ROOT / "udyam_logo.png",
    "mca": ROOT / "mca_logo.png",
}


def trim_whitespace(img: Image.Image) -> Image.Image:
    # Trim near-white borders to keep logos compact.
    bg = Image.new(img.mode, img.size, (255, 255, 255))
    diff = Image.eval(Image.blend(img.convert("RGB"), bg, 0.5), lambda p: 255 - p)
    bbox = diff.getbbox()
    if bbox:
        return img.crop(bbox)
    return img


def crop_logo(pdf_path: Path, crop_rect, out_path: Path) -> None:
    if not pdf_path.exists():
        print(f"Missing source: {pdf_path}")
        return

    doc = fitz.open(pdf_path)
    page = doc[0]
    rect = page.rect

    x0 = rect.x0 + rect.width * crop_rect[0]
    y0 = rect.y0 + rect.height * crop_rect[1]
    x1 = rect.x0 + rect.width * crop_rect[2]
    y1 = rect.y0 + rect.height * crop_rect[3]

    clip = fitz.Rect(x0, y0, x1, y1)
    pix = page.get_pixmap(matrix=fitz.Matrix(2.8, 2.8), clip=clip, alpha=False)
    doc.close()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    temp = out_path.with_suffix(".tmp.png")
    pix.save(str(temp))

    img = Image.open(temp).convert("RGB")
    img = trim_whitespace(img)
    img.save(out_path, format="PNG")
    temp.unlink(missing_ok=True)
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    for key in ["dpiit", "udyam", "mca"]:
        crop_logo(FILES[key], CROPS[key], OUT[key])
