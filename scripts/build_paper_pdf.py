"""Build a simple text-based PDF without external dependencies."""

from pathlib import Path


def escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_simple_pdf(lines, output_path: Path) -> None:
    objects = []

    # Font object
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    content_lines = [b"BT", b"/F1 10 Tf", b"50 790 Td", b"12 TL"]
    first = True
    for line in lines:
        safe = escape_pdf_text(line)
        if not first:
            content_lines.append(b"T*")
        content_lines.append(f"({safe}) Tj".encode("latin-1", errors="replace"))
        first = False
    content_lines.append(b"ET")
    content_stream = b"\n".join(content_lines)

    objects.append(f"<< /Length {len(content_stream)} >>\nstream\n".encode() + content_stream + b"\nendstream")
    objects.append(b"<< /Type /Page /Parent 4 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 1 0 R >> >> /Contents 2 0 R >>")
    objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objects.append(b"<< /Type /Catalog /Pages 4 0 R >>")

    pdf = bytearray(b"%PDF-1.4\n")
    xref = [0]

    for idx, obj in enumerate(objects, start=1):
        xref.append(len(pdf))
        pdf.extend(f"{idx} 0 obj\n".encode())
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(objects)+1}\n".encode())
    pdf.extend(b"0000000000 65535 f \n")
    for off in xref[1:]:
        pdf.extend(f"{off:010d} 00000 n \n".encode())

    pdf.extend(
        (
            f"trailer\n<< /Size {len(objects)+1} /Root 5 0 R >>\n"
            f"startxref\n{xref_start}\n%%EOF\n"
        ).encode()
    )

    output_path.write_bytes(bytes(pdf))


def main() -> None:
    md_path = Path("paper/causalaudit_paper.md")
    out_path = Path("paper/causalaudit_paper.pdf")

    text = md_path.read_text(encoding="utf-8")
    lines = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped:
            lines.append(" ")
            continue
        # keep lines reasonably short
        while len(stripped) > 95:
            lines.append(stripped[:95])
            stripped = stripped[95:]
        lines.append(stripped)

    build_simple_pdf(lines[:220], out_path)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
