import sys
from pathlib import Path
from pypdf import PdfReader

PDF_FILE = Path(__file__).parent / "PagerDuty - Take Home exercise.pdf"
OUTPUT_FILE = Path(__file__).parent / "PagerDuty - Take Home exercise.txt"

def pdf_to_txt(pdf_path: Path, output_path: Path) -> int:
    reader = PdfReader(str(pdf_path))
    pages = len(reader.pages)
    text_parts = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            text_parts.append(text.strip())
        else:
            text_parts.append(f"[Page {i + 1}: no extractable text]")

    full_text = "\n\n".join(text_parts)
    output_path.write_text(full_text, encoding="utf-8")
    return pages


if __name__ == "__main__":
    if not PDF_FILE.exists():
        print(f"[-] PDF not found: {PDF_FILE}")
        sys.exit(1)

    pages = pdf_to_txt(PDF_FILE, OUTPUT_FILE)
    print(f"[+] Extracted {pages} pages -> {OUTPUT_FILE}")
