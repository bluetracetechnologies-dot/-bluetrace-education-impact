from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).resolve().parent
TODAY = date.today().isoformat()
COMPANY = "Bluetrace Technologies Pvt. Ltd."
AUTHOR = "A.R. Ansari | Bluetrace Engineering"
CLASSIFICATION = "Client Shareable"

NAVY = colors.HexColor("#14324a")
TEAL = colors.HexColor("#1f8a70")
GOLD = colors.HexColor("#c58f2b")
BORDER = colors.HexColor("#d5dee5")
SOFT = colors.HexColor("#f7fafc")
TEXT = colors.HexColor("#24333f")

LOGO_CANDIDATES = [
    BASE_DIR / "logo.png",
    BASE_DIR.parent / "logo.png",
]
CREDENTIALS = [
    BASE_DIR / "startup_india_logo.png",
    BASE_DIR.parent / "startup_india_logo.png",
    BASE_DIR / "udyam_logo.png",
    BASE_DIR.parent / "udyam_logo.png",
    BASE_DIR / "mca_logo.png",
    BASE_DIR.parent / "mca_logo.png",
]


def first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    return None


def existing_credentials():
    seen = set()
    out = []
    for p in CREDENTIALS:
        if p.exists() and p.name not in seen:
            seen.add(p.name)
            out.append(p)
    return out


def draw_header(c, title, doc_id):
    w, h = landscape(A4)
    c.setFillColor(NAVY)
    c.rect(0, h - 20 * mm, w, 20 * mm, fill=1, stroke=0)

    logo = first_existing(LOGO_CANDIDATES)
    text_x = 14 * mm
    if logo is not None:
        try:
            c.drawImage(str(logo), 8 * mm, h - 16.5 * mm, width=11 * mm, height=11 * mm, preserveAspectRatio=True, mask="auto")
            text_x = 21 * mm
        except Exception:
            pass

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(text_x, h - 11.5 * mm, COMPANY)
    c.setFont("Helvetica", 8.5)
    c.drawRightString(w - 8 * mm, h - 11.5 * mm, doc_id)

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(text_x, h - 16 * mm, title)


def draw_metadata(c, doc_id):
    w, h = landscape(A4)
    y = h - 34 * mm
    c.setFillColor(SOFT)
    c.setStrokeColor(BORDER)
    c.rect(8 * mm, y - 13 * mm, w - 16 * mm, 13 * mm, fill=1, stroke=1)

    c.setFillColor(TEXT)
    c.setFont("Helvetica", 7.3)
    c.drawString(10 * mm, y - 5 * mm, f"Company: Bluetrace Technologies")
    c.drawString(62 * mm, y - 5 * mm, f"Doc ID: {doc_id}")
    c.drawString(122 * mm, y - 5 * mm, "Version: v1.0")
    c.drawString(156 * mm, y - 5 * mm, "Revision: R0")
    c.drawString(10 * mm, y - 10 * mm, f"Date: {TODAY}")
    c.drawString(62 * mm, y - 10 * mm, f"Author: {AUTHOR}")
    c.drawString(156 * mm, y - 10 * mm, f"Classification: {CLASSIFICATION}")


def draw_credential_strip(c):
    logos = existing_credentials()
    if not logos:
        return
    w, h = landscape(A4)
    y = h - 50 * mm
    c.setFillColor(colors.white)
    c.setStrokeColor(BORDER)
    c.roundRect(8 * mm, y - 8 * mm, w - 16 * mm, 8 * mm, 2 * mm, fill=1, stroke=1)

    box_w = 22 * mm
    gap = 8 * mm
    total = len(logos) * box_w + (len(logos) - 1) * gap
    x = (w - total) / 2
    for p in logos:
        try:
            c.drawImage(str(p), x, y - 6.6 * mm, width=box_w, height=5.2 * mm, preserveAspectRatio=True, anchor="s", mask="auto")
        except Exception:
            pass
        x += box_w + gap


def draw_footer(c):
    w, _ = landscape(A4)
    c.setFillColor(NAVY)
    c.rect(0, 0, w, 13 * mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 7.5)
    c.drawString(8 * mm, 4.5 * mm, "Confidential - Internal Proposal Draft | Page 1")
    c.drawRightString(w - 8 * mm, 4.5 * mm, f"Version v1.0 | Revision R0 | Date {TODAY}")


def rounded(c, x, y, w, h, title, lines):
    c.setFillColor(colors.white)
    c.setStrokeColor(BORDER)
    c.roundRect(x, y, w, h, 3 * mm, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + 3 * mm, y + h - 6 * mm, title)
    c.setFillColor(TEXT)
    c.setFont("Helvetica", 8.7)
    py = y + h - 12 * mm
    for ln in lines:
        c.drawString(x + 3 * mm, py, ln)
        py -= 4.7 * mm


def arrow(c, x1, y1, x2, y2, label=""):
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.line(x1, y1, x2, y2)
    c.line(x2, y2, x2 - 3, y2 + 2)
    c.line(x2, y2, x2 - 3, y2 - 2)
    if label:
        c.setFillColor(TEXT)
        c.setFont("Helvetica", 7)
        c.drawCentredString((x1 + x2) / 2, y1 + 2.5 * mm, label)


def build_architecture_pdf():
    out = BASE_DIR / "Driving_School_App_Reference_Architecture_v1.pdf"
    c = canvas.Canvas(str(out), pagesize=landscape(A4))
    w, h = landscape(A4)

    draw_header(c, "Driving School App - Reference Architecture", "BT-DRIVE-ARCH")
    draw_metadata(c, "BT-DRIVE-ARCH")
    draw_credential_strip(c)

    top = h - 101 * mm
    bw = 54 * mm
    bh = 30 * mm
    gap = 8 * mm
    total_w = 4 * bw + 3 * gap
    x = (w - total_w) / 2

    rounded(c, x, top, bw, bh, "Student App", ["Signup/Login", "Lesson booking", "Progress tracking", "Notifications"])
    rounded(c, x + bw + gap, top, bw, bh, "Instructor App", ["Schedule calendar", "Session status", "Student feedback", "Attendance updates"])
    rounded(c, x + 2 * (bw + gap), top, bw, bh, "Backend/API", ["Role-based auth", "Slot management", "Booking engine", "Analytics events"])
    rounded(c, x + 3 * (bw + gap), top, bw, bh, "Admin Panel", ["Instructor setup", "Calendar control", "Reporting", "Audit logs"])

    cy = top + bh / 2
    arrow(c, x + bw, cy, x + bw + gap, cy, "sync")
    arrow(c, x + 2 * bw + gap, cy, x + 2 * bw + 2 * gap, cy, "REST")
    arrow(c, x + 3 * bw + 2 * gap, cy, x + 3 * bw + 3 * gap, cy, "admin")

    lower_y = 30 * mm
    rounded(c, x + 30 * mm, lower_y, 70 * mm, 16 * mm, "Integrations", ["FCM/APNs", "Email/SMS OTP"])
    rounded(c, x + 116 * mm, lower_y, 70 * mm, 16 * mm, "Data Layer", ["Firebase or PostgreSQL", "Cloud storage / media"])
    arrow(c, x + 160 * mm, top, x + 145 * mm, lower_y + 16 * mm, "events")
    arrow(c, x + 190 * mm, lower_y + 16 * mm, x + 210 * mm, top, "config")

    draw_footer(c)
    c.showPage()
    c.save()


def build_milestone_pdf():
    out = BASE_DIR / "Driving_School_App_Milestone_Plan_v1.pdf"
    c = canvas.Canvas(str(out), pagesize=landscape(A4))
    w, h = landscape(A4)

    draw_header(c, "Driving School App - MVP Milestone Plan", "BT-DRIVE-MILESTONE")
    draw_metadata(c, "BT-DRIVE-MILESTONE")
    draw_credential_strip(c)

    c.setFillColor(colors.white)
    c.setStrokeColor(BORDER)
    c.roundRect(12 * mm, 20 * mm, w - 24 * mm, h - 82 * mm, 3 * mm, fill=1, stroke=1)

    milestones = [
        ("M1", "Discovery + UX + Data Model", "$38", "2 days"),
        ("M2", "Student App Core", "$25", "2 days"),
        ("M3", "Instructor Workflow Core", "$15", "1 day"),
        ("M4", "Backend Integration + Notifications", "$17", "1 day"),
        ("M5", "QA + Handoff Docs", "$5", "1 day"),
    ]

    table_x = 20 * mm
    table_y = h - 66 * mm
    col_w = [20 * mm, 120 * mm, 26 * mm, 24 * mm]
    row_h = 12 * mm

    headers = ["Milestone", "Scope", "Budget", "Duration"]
    c.setFillColor(NAVY)
    c.rect(table_x, table_y, sum(col_w), row_h, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    hx = table_x + 3 * mm
    for i, htxt in enumerate(headers):
        c.drawString(hx, table_y + 4.1 * mm, htxt)
        hx += col_w[i]

    y = table_y - row_h
    for idx, m in enumerate(milestones):
        c.setFillColor(SOFT if idx % 2 == 0 else colors.white)
        c.setStrokeColor(BORDER)
        c.rect(table_x, y, sum(col_w), row_h, fill=1, stroke=1)

        c.setFillColor(TEXT)
        c.setFont("Helvetica", 9)
        c.drawString(table_x + 3 * mm, y + 4.1 * mm, m[0])
        c.drawString(table_x + col_w[0] + 3 * mm, y + 4.1 * mm, m[1])
        c.drawString(table_x + col_w[0] + col_w[1] + 3 * mm, y + 4.1 * mm, m[2])
        c.drawString(table_x + col_w[0] + col_w[1] + col_w[2] + 3 * mm, y + 4.1 * mm, m[3])
        y -= row_h

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(NAVY)
    c.drawString(20 * mm, y - 4 * mm, "Total Budget: $100 | Total Duration: 7 days")

    c.setFont("Helvetica", 8.5)
    c.setFillColor(TEXT)
    c.drawString(20 * mm, y - 10 * mm, "Note: This plan is an MVP aligned to the posted budget and can be expanded under contract-to-hire.")

    draw_footer(c)
    c.showPage()
    c.save()


def main():
    build_architecture_pdf()
    build_milestone_pdf()
    print("Generated Driving_School_App_Reference_Architecture_v1.pdf")
    print("Generated Driving_School_App_Milestone_Plan_v1.pdf")


if __name__ == "__main__":
    main()
