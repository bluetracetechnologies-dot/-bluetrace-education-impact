from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

OUTPUT_DIR = Path(__file__).resolve().parent
TODAY = date.today().isoformat()
COMPANY = "Bluetrace Technologies Pvt. Ltd."
AUTHOR = "A.R. Ansari | Bluetrace Engineering"
CLASSIFICATION = "Client Shareable"
DOC_PREFIX = "BT-REFARCH"

LOGO_CANDIDATES = ["logo.png", "bluetrace_logo.png", "bluetrace-logo.png"]
CRED_LOGOS = ["startup_india_logo.png", "udyam_logo.png", "mca_logo.png"]

NAVY = colors.HexColor("#14324a")
TEAL = colors.HexColor("#1f8a70")
GOLD = colors.HexColor("#c58f2b")
BORDER = colors.HexColor("#d5dee5")
TEXT = colors.HexColor("#24333f")
MUTED = colors.HexColor("#5c6b73")
SOFT = colors.HexColor("#f7fafc")


def first_existing(candidates: list[str]) -> Path | None:
    for name in candidates:
        p = OUTPUT_DIR / name
        if p.exists():
            return p
    return None


def existing_credential_logos() -> list[Path]:
    paths: list[Path] = []
    for name in CRED_LOGOS:
        p = OUTPUT_DIR / name
        if p.exists():
            paths.append(p)
    return paths


def draw_header(c: canvas.Canvas, title: str, doc_id: str) -> None:
    w, h = landscape(A4)
    c.setFillColor(NAVY)
    c.rect(0, h - 20 * mm, w, 20 * mm, fill=1, stroke=0)

    logo = first_existing(LOGO_CANDIDATES)
    text_x = 16 * mm
    if logo is not None:
        try:
            c.drawImage(str(logo), 10 * mm, h - 17 * mm, width=12 * mm, height=12 * mm, preserveAspectRatio=True, mask="auto")
            text_x = 24 * mm
        except Exception:
            text_x = 16 * mm

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(text_x, h - 11.5 * mm, COMPANY)
    c.setFont("Helvetica", 9)
    c.drawRightString(w - 10 * mm, h - 11.5 * mm, doc_id)

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(text_x, h - 16.2 * mm, title)


def draw_footer(c: canvas.Canvas, page_no: int = 1) -> None:
    w, _ = landscape(A4)
    c.setFillColor(NAVY)
    c.rect(0, 0, w, 14 * mm, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica", 8)
    c.drawString(10 * mm, 5 * mm, f"Confidential - Internal Proposal Draft | Page {page_no}")

    c.drawRightString(
        w - 10 * mm,
        5 * mm,
        f"Version v1.0 | Revision R0 | Date {TODAY}",
    )


def wrap_text_to_width(text: str, font_name: str, font_size: float, max_width: float) -> list[str]:
    words = text.split()
    if not words:
        return [""]

    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if pdfmetrics.stringWidth(candidate, font_name, font_size) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def draw_metadata_strip(c: canvas.Canvas, doc_id: str) -> None:
    w, h = landscape(A4)
    y = h - 34 * mm
    c.setFillColor(SOFT)
    c.setStrokeColor(BORDER)
    c.rect(10 * mm, y - 14 * mm, w - 20 * mm, 14 * mm, fill=1, stroke=1)

    c.setFillColor(TEXT)
    c.setFont("Helvetica", 7.5)
    top_fields = [
        f"Company: Bluetrace Technologies",
        f"Doc ID: {doc_id}",
        "Version: v1.0",
        "Revision: R0",
    ]
    bottom_fields = [
        f"Date: {TODAY}",
        f"Author: {AUTHOR}",
        f"Classification: {CLASSIFICATION}",
    ]

    top_x = [12 * mm, 74 * mm, 154 * mm, 194 * mm]
    for x, field in zip(top_x, top_fields):
        c.drawString(x, y - 5.5 * mm, field)

    bottom_x = [12 * mm, 74 * mm, 194 * mm]
    for x, field in zip(bottom_x, bottom_fields):
        c.drawString(x, y - 10.8 * mm, field)


def draw_credential_strip(c: canvas.Canvas) -> None:
    logos = existing_credential_logos()
    if not logos:
        return

    w, h = landscape(A4)
    strip_y = h - 49 * mm
    c.setFillColor(colors.white)
    c.setStrokeColor(BORDER)
    c.roundRect(10 * mm, strip_y - 9 * mm, w - 20 * mm, 9 * mm, 2 * mm, fill=1, stroke=1)

    gap = 10 * mm
    box_h = 6 * mm
    box_w = 28 * mm
    total_w = len(logos) * box_w + (len(logos) - 1) * gap
    start_x = (w - total_w) / 2.0

    x = start_x
    for p in logos:
        try:
            c.drawImage(str(p), x, strip_y - 7.5 * mm, width=box_w, height=box_h, preserveAspectRatio=True, anchor="s", mask="auto")
        except Exception:
            pass
        x += box_w + gap


def draw_box(c: canvas.Canvas, x: float, y: float, w: float, h: float, title: str, body: str, fill=colors.white) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(BORDER)
    c.roundRect(x, y, w, h, 4 * mm, fill=1, stroke=1)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 11)
    title_lines = wrap_text_to_width(title, "Helvetica-Bold", 11, w - 8 * mm)
    title_y = y + h - 7 * mm
    for line in title_lines[:2]:
        c.drawString(x + 4 * mm, title_y, line)
        title_y -= 4.5 * mm

    c.setFillColor(TEXT)
    font_name = "Helvetica"
    font_size = 9.5
    c.setFont(font_name, font_size)
    lines: list[str] = []
    for raw in body.split("\n"):
        lines.extend(wrap_text_to_width(raw, font_name, font_size, w - 8 * mm))

    line_y = y + h - 16 * mm
    line_step = 4.6 * mm
    max_lines = max(1, int((h - 18 * mm) / line_step))
    for idx, line in enumerate(lines[:max_lines]):
        if idx == max_lines - 1 and len(lines) > max_lines:
            ell = "..."
            while pdfmetrics.stringWidth(line + ell, font_name, font_size) > (w - 8 * mm) and len(line) > 1:
                line = line[:-1]
            line = line + ell
        c.drawString(x + 4 * mm, line_y, line)
        line_y -= line_step


def draw_arrow(c: canvas.Canvas, x1: float, y1: float, x2: float, y2: float, label: str = "") -> None:
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.7)
    c.line(x1, y1, x2, y2)

    # Arrow head
    dx = x2 - x1
    dy = y2 - y1
    length = (dx * dx + dy * dy) ** 0.5
    if length <= 0:
        return
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    size = 4.0
    c.line(x2, y2, x2 - ux * size + px * size * 0.6, y2 - uy * size + py * size * 0.6)
    c.line(x2, y2, x2 - ux * size - px * size * 0.6, y2 - uy * size - py * size * 0.6)

    if label:
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawCentredString((x1 + x2) / 2.0, (y1 + y2) / 2.0 + 3 * mm, label)


def draw_elbow_arrow(c: canvas.Canvas, x1: float, y1: float, x2: float, y2: float, bend_y: float, label: str = "") -> None:
    """Draw a right-angle connector: vertical to bend_y, horizontal, then vertical to target."""
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.7)
    c.line(x1, y1, x1, bend_y)
    c.line(x1, bend_y, x2, bend_y)
    c.line(x2, bend_y, x2, y2)

    # Arrow head at target point (last segment direction).
    dy = y2 - bend_y
    direction = 1.0 if dy >= 0 else -1.0
    size = 4.0
    c.line(x2, y2, x2 - size * 0.45, y2 - direction * size)
    c.line(x2, y2, x2 + size * 0.45, y2 - direction * size)

    if label:
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawCentredString((x1 + x2) / 2.0, bend_y + 2.5 * mm, label)


def build_ble_mobile_embedded_architecture() -> None:
    title = "BLE + Mobile + Embedded Architecture"
    doc_id = f"{DOC_PREFIX}-BLE-MOBILE-EMBEDDED"
    out = OUTPUT_DIR / "BLE_Mobile_Embedded_Architecture_Diagram_v1.pdf"

    c = canvas.Canvas(str(out), pagesize=landscape(A4))
    w, h = landscape(A4)

    draw_header(c, title, doc_id)
    draw_metadata_strip(c, doc_id)
    draw_credential_strip(c)

    # Top-row system blocks, centered in usable content area.
    top_h = 34 * mm
    gap = 8 * mm
    box_w = 48 * mm
    group_w = 4 * box_w + 3 * gap
    x0 = (w - group_w) / 2.0

    ref_h = 9 * mm
    ota_h = 14 * mm
    gap_ref_to_ota = 10 * mm
    gap_ota_to_top = 16 * mm
    cluster_h = ref_h + gap_ref_to_ota + ota_h + gap_ota_to_top + top_h

    content_top = h - 62 * mm
    content_bottom = 20 * mm
    cluster_bottom = content_bottom + (content_top - content_bottom - cluster_h) / 2.0

    ref_y = cluster_bottom
    ota_y = ref_y + ref_h + gap_ref_to_ota
    top_y = ota_y + ota_h + gap_ota_to_top

    draw_box(
        c,
        x0,
        top_y,
        box_w,
        top_h,
        "Android App",
        "Chamberlain Field App\nDoor status and control\nTechnician diagnostics\nProvisioning and logs",
    )
    draw_box(
        c,
        x0 + box_w + gap,
        top_y,
        box_w,
        top_h,
        "BLE Communication",
        "GATT services\nSecure pairing/bonding\nCommand + telemetry frames\nLow-latency control path",
    )
    draw_box(
        c,
        x0 + 2 * (box_w + gap),
        top_y,
        box_w,
        top_h,
        "Embedded Firmware",
        "nRF52/STM32 firmware\nState machine + safety logic\nMotor/actuator I/O\nDiagnostics events",
    )
    draw_box(
        c,
        x0 + 3 * (box_w + gap),
        top_y,
        box_w,
        top_h,
        "Cloud/Backend",
        "Device inventory\nPackage registry\nLogs/alerts (optional)\nMQTT/HTTPS endpoints",
    )

    # Explicit OTA update flow block (was previously implicit/missing in visuals).
    ota_w = 60 * mm
    ota_x = x0 + 2 * (box_w + gap) + 2 * mm
    draw_box(
        c,
        ota_x,
        ota_y,
        ota_w,
        ota_h,
        "OTA Update Flow",
        "Signed package -> version check -> safe rollback",
        fill=SOFT,
    )

    cy = top_y + top_h / 2.0
    draw_arrow(c, x0 + box_w, cy, x0 + box_w + gap, cy, "BLE")
    draw_arrow(c, x0 + 2 * box_w + gap, cy, x0 + 2 * box_w + 2 * gap, cy, "GATT")
    draw_arrow(c, x0 + 3 * box_w + 2 * gap, cy, x0 + 3 * box_w + 3 * gap, cy, "MQTT/HTTPS")

    # OTA lane arrows separated from the main horizontal lane to prevent overlap.
    cloud_x = x0 + 3 * (box_w + gap)
    firmware_x = x0 + 2 * (box_w + gap)
    draw_elbow_arrow(
        c,
        cloud_x + box_w * 0.65,
        top_y,
        ota_x + ota_w * 0.8,
        ota_y + ota_h,
        bend_y=ota_y + ota_h + 7 * mm,
        label="Update package",
    )
    draw_elbow_arrow(
        c,
        ota_x + ota_w * 0.25,
        ota_y + ota_h,
        firmware_x + box_w * 0.45,
        top_y,
        bend_y=ota_y + ota_h + 12 * mm,
        label="Deploy/rollback",
    )

    c.setFillColor(SOFT)
    c.setStrokeColor(BORDER)
    ref_w = group_w
    ref_x = (w - ref_w) / 2.0
    c.roundRect(ref_x, ref_y, ref_w, ref_h, 2 * mm, fill=1, stroke=1)
    c.setFillColor(TEXT)
    c.setFont("Helvetica", 8.8)
    c.drawString(
        ref_x + 4 * mm,
        ref_y + 3.3 * mm,
        "Reference: Chamberlain commercial door operator implementation pattern (mobile ↔ BLE ↔ embedded ↔ OTA/cloud).",
    )

    draw_footer(c)
    c.showPage()
    c.save()


def build_android_image_ai_workflow() -> None:
    title = "Android Image-to-AI Automation Workflow – Reference Architecture"
    doc_id = f"{DOC_PREFIX}-ANDROID-IMAGE-AI"
    out = OUTPUT_DIR / "Android_Image_to_AI_Automation_Workflow_Reference_Architecture_v1.pdf"

    c = canvas.Canvas(str(out), pagesize=landscape(A4))
    w, h = landscape(A4)

    draw_header(c, title, doc_id)
    draw_metadata_strip(c, doc_id)
    draw_credential_strip(c)

    steps = [
        "USB Camera",
        "Samsung S22 App",
        "Image Processing",
        "AI Engine/API",
        "Text Response",
        "Android TTS",
        "Bluetooth Earpiece",
    ]

    # Center workflow cluster in usable content area.
    box_w = 31 * mm
    box_h = 22 * mm
    gap = 4 * mm
    flow_w = len(steps) * box_w + (len(steps) - 1) * gap
    x = (w - flow_w) / 2.0

    summary_h = 20 * mm
    gap_summary_to_flow = 12 * mm
    cluster_h = summary_h + gap_summary_to_flow + box_h
    content_top = h - 62 * mm
    content_bottom = 20 * mm
    cluster_bottom = content_bottom + (content_top - content_bottom - cluster_h) / 2.0
    summary_y = cluster_bottom
    top_y = summary_y + summary_h + gap_summary_to_flow

    for i, step in enumerate(steps):
        fill = colors.white if i % 2 == 0 else SOFT
        draw_box(c, x, top_y, box_w, box_h, f"Step {i + 1}", step, fill=fill)
        if i < len(steps) - 1:
            draw_elbow_arrow(
                c,
                x + box_w,
                top_y + box_h / 2.0,
                x + box_w + gap,
                top_y + box_h / 2.0,
                bend_y=top_y + box_h / 2.0 + 2.2 * mm,
            )
        x += box_w + gap

    c.setFillColor(SOFT)
    c.setStrokeColor(BORDER)
    summary_w = flow_w
    summary_x = (w - summary_w) / 2.0
    c.roundRect(summary_x, summary_y, summary_w, summary_h, 2 * mm, fill=1, stroke=1)
    c.setFillColor(TEXT)
    c.setFont("Helvetica", 10)
    c.drawString(summary_x + 4 * mm, summary_y + 13 * mm, "Operational Outcome")
    c.setFont("Helvetica", 9)
    outcome = "Real-time capture-to-response assistive loop: camera input -> AI inference -> spoken guidance over Bluetooth earpiece."
    wrapped = wrap_text_to_width(outcome, "Helvetica", 9, summary_w - 8 * mm)
    oy = summary_y + 7 * mm
    for line in wrapped[:2]:
        c.drawString(summary_x + 4 * mm, oy, line)
        oy -= 4.6 * mm

    draw_footer(c)
    c.showPage()
    c.save()


def build_company_capability_sheet() -> None:
    title = "Bluetrace Company Capability Sheet"
    doc_id = f"{DOC_PREFIX}-CAPABILITY-SHEET"
    out = OUTPUT_DIR / "Bluetrace_Company_Capability_Sheet_One_Page_v1.pdf"

    c = canvas.Canvas(str(out), pagesize=landscape(A4))
    w, h = landscape(A4)

    draw_header(c, title, doc_id)
    draw_metadata_strip(c, doc_id)
    draw_credential_strip(c)

    c.setFillColor(colors.white)
    c.setStrokeColor(BORDER)
    c.roundRect(14 * mm, 28 * mm, w - 28 * mm, h - 94 * mm, 4 * mm, fill=1, stroke=1)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(22 * mm, h - 63 * mm, "Core Engineering Capability")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(22 * mm, h - 69 * mm, "Integrated mobile, embedded, and AI delivery for production-grade systems.")

    capabilities = [
        "Android Development",
        "Embedded Linux",
        "STM32",
        "nRF52",
        "BLE",
        "OTA",
        "AI Integration",
        "Computer Vision",
        "IoT Gateways",
        "Cloud Connectivity",
    ]

    start_x = 24 * mm
    start_y = h - 82 * mm
    col_w = (w - 50 * mm) / 2.0
    row_h = 11 * mm

    for i, item in enumerate(capabilities):
        col = i % 2
        row = i // 2
        x = start_x + col * col_w
        y = start_y - row * row_h

        c.setFillColor(SOFT)
        c.setStrokeColor(BORDER)
        c.roundRect(x, y - 8 * mm, col_w - 8 * mm, 8 * mm, 2 * mm, fill=1, stroke=1)
        c.setFillColor(TEXT)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 3 * mm, y - 5.5 * mm, f"• {item}")

    c.setFillColor(SOFT)
    c.setStrokeColor(BORDER)
    c.roundRect(22 * mm, 34 * mm, w - 44 * mm, 15 * mm, 2 * mm, fill=1, stroke=1)
    c.setFillColor(TEXT)
    c.setFont("Helvetica", 9)
    c.drawString(
        26 * mm,
        42 * mm,
        "Delivery Model: discovery -> architecture -> implementation -> validation -> deployment -> support.",
    )
    c.drawString(
        26 * mm,
        36.5 * mm,
        "Suitable for education-tech, industrial IoT, assistive AI, and connected embedded product lines.",
    )

    draw_footer(c)
    c.showPage()
    c.save()


def main() -> None:
    build_ble_mobile_embedded_architecture()
    build_android_image_ai_workflow()
    build_company_capability_sheet()
    print("Generated BLE_Mobile_Embedded_Architecture_Diagram_v1.pdf")
    print("Generated Android_Image_to_AI_Automation_Workflow_Reference_Architecture_v1.pdf")
    print("Generated Bluetrace_Company_Capability_Sheet_One_Page_v1.pdf")


if __name__ == "__main__":
    main()
