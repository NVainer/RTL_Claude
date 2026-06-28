"""Generate Chrome Web Store promo screenshots for Claude RTL.

Renders a Claude-style dark chat showing Hebrew RTL output (with English
tech terms reading LTR inside) and Hebrew being typed in the composer.
Outputs exact 1280x800 and 640x400 PNGs. Run from repo root:

    python tools/make_promo.py
"""
import os
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display

W, H = 1280, 800
OUT_DIR = "dist"

# Claude-ish warm dark palette
BG = (31, 30, 29)
CARD = (38, 37, 35)
BUBBLE = (52, 51, 47)
BORDER = (58, 56, 53)
WHITE = (236, 233, 228)
MUTED = (150, 146, 140)
ORANGE = (217, 119, 87)

AR = r"C:\Windows\Fonts\arial.ttf"
ARB = r"C:\Windows\Fonts\arialbd.ttf"

LEFT, RIGHT = 250, 1030  # centered content column (width 780)


def F(path, size):
    return ImageFont.truetype(path, size)


def vis(text):
    """Logical -> visual order, forcing an RTL base direction."""
    return get_display(text, base_dir="R")


def rtl_line_width(draw, text, font):
    return draw.textlength(vis(text), font=font)


def wrap_rtl(draw, text, font, max_w):
    """Word-wrap logical Hebrew text to fit max_w (measured in visual order)."""
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if cur and rtl_line_width(draw, trial, font) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def draw_rtl(draw, text, font, y, fill, right=RIGHT, max_w=None, lh=1.5, gap=14):
    """Draw right-aligned, wrapped RTL text. Returns the next y."""
    max_w = max_w or (right - LEFT)
    line_h = int(font.size * lh)
    for line in wrap_rtl(draw, text, font, max_w):
        v = vis(line)
        w = draw.textlength(v, font=font)
        draw.text((right - w, y), v, font=font, fill=fill)
        y += line_h
    return y + gap


def rounded(draw, box, r, **kw):
    draw.rounded_rectangle(box, radius=r, **kw)


def build():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_head = F(ARB, 30)
    f_sub = F(AR, 18)
    f_body = F(AR, 22)
    f_bubble = F(ARB, 22)
    f_small = F(AR, 16)
    f_model = F(ARB, 17)

    # --- Headline (English, so store reviewers read it instantly) ---
    head = "Hebrew & Arabic, right-to-left on Claude"
    hw = d.textlength(head, font=f_head)
    d.text(((W - hw) / 2, 34), head, font=f_head, fill=WHITE)
    sub = "Every paragraph aligns itself - automatically.  Code blocks stay left-to-right."
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 74), sub, font=f_sub, fill=MUTED)

    # --- User message bubble (right-aligned) ---
    user_text = "כתוב לי הסבר קצר על אבטחת סייבר"
    bw = rtl_line_width(d, user_text, f_bubble)
    padx, pady = 22, 14
    bub_w = bw + padx * 2
    bub_h = int(f_bubble.size * 1.5) + pady
    bx1, by1 = RIGHT - bub_w, 130
    rounded(d, [bx1, by1, RIGHT, by1 + bub_h], 18, fill=BUBBLE)
    d.text((RIGHT - padx - bw, by1 + pady - 2), vis(user_text), font=f_bubble, fill=WHITE)

    # --- Assistant avatar (our aleph badge) ---
    y = by1 + bub_h + 34
    badge = 30
    try:
        ic = Image.open("claude-rtl/icons/icon48.png").convert("RGBA").resize((badge, badge), Image.LANCZOS)
        img.paste(ic, (RIGHT - badge, y), ic)
    except Exception:
        rounded(d, [RIGHT - badge, y, RIGHT, y + badge], 7, fill=ORANGE)
    y += badge + 16

    # --- Assistant response (RTL, with English terms reading LTR inside) ---
    paras = [
        ("בטח! הנה הסבר קצר ופשוט על אבטחת סייבר:", f_bubble, WHITE),
        ("אבטחת סייבר היא ההגנה על מערכות, רשתות ומידע מפני התקפות וגישה לא מורשית.", f_body, WHITE),
        ("הכלים הנפוצים כוללים firewall, אנטי-וירוס והצפנה. איומים נפוצים הם phishing וכופרה (ransomware).", f_body, WHITE),
        ("בארגונים גדולים נעזרים במערכת SIEM כדי לנטר אירועים ולזהות חריגות בזמן אמת.", f_body, WHITE),
    ]
    for text, font, fill in paras:
        y = draw_rtl(d, text, font, y, fill, gap=16)

    # --- Feature chips (fills the middle, doubles as marketing) ---
    f_chip = F(AR, 17)
    chips = ["Per-paragraph direction", "Works in the input box", "Code stays LTR"]
    ch_h, ipad, cgap = 40, 20, 16
    widths = [d.textlength(c, font=f_chip) + 22 + ipad * 2 for c in chips]
    total = sum(widths) + cgap * (len(chips) - 1)
    cx0 = (W - total) / 2
    crow = 520
    for c, w in zip(chips, widths):
        rounded(d, [cx0, crow, cx0 + w, crow + ch_h], 20, outline=BORDER, width=1)
        chk = cx0 + ipad
        midy = crow + ch_h / 2
        d.line([chk, midy + 1, chk + 6, midy + 7], fill=ORANGE, width=2)
        d.line([chk + 6, midy + 7, chk + 16, midy - 7], fill=ORANGE, width=2)
        d.text((chk + 22, crow + (ch_h - f_chip.size) / 2 - 2), c, font=f_chip, fill=WHITE)
        cx0 += w + cgap

    # --- Composer (rounded box) with Hebrew being typed, RTL ---
    comp_h = 116
    cy1 = H - 40 - comp_h
    rounded(d, [LEFT, cy1, RIGHT, cy1 + comp_h], 18, fill=CARD, outline=BORDER, width=1)
    typed = "מה ההבדל בין IDS ל-IPS?"
    tw = rtl_line_width(d, typed, f_body)
    tx = RIGHT - 24 - tw
    ty = cy1 + 22
    d.text((tx, ty), vis(typed), font=f_body, fill=WHITE)
    # caret sits at the LEFT end of RTL text
    d.rectangle([tx - 3, ty + 1, tx - 1, ty + 28], fill=ORANGE)

    # bottom controls row
    row_y = cy1 + comp_h - 38
    # "+" on the left
    d.ellipse([LEFT + 16, row_y, LEFT + 44, row_y + 28], outline=MUTED, width=2)
    d.line([LEFT + 30, row_y + 8, LEFT + 30, row_y + 20], fill=MUTED, width=2)
    d.line([LEFT + 24, row_y + 14, LEFT + 36, row_y + 14], fill=MUTED, width=2)
    # send button (orange) on the right
    bs = 34
    sx2, sy2 = RIGHT - 16, row_y - 2
    sx1, sy1 = sx2 - bs, sy2 + (28 - bs) // 2
    rounded(d, [sx1, sy1, sx2, sy1 + bs], 9, fill=ORANGE)
    cx = (sx1 + sx2) / 2
    cyc = sy1 + bs / 2
    d.line([cx, cyc + 8, cx, cyc - 8], fill=WHITE, width=3)
    d.line([cx, cyc - 8, cx - 6, cyc - 2], fill=WHITE, width=3)
    d.line([cx, cyc - 8, cx + 6, cyc - 2], fill=WHITE, width=3)
    # model label to the left of the send button
    label = "Opus 4.8"
    lw = d.textlength(label, font=f_model)
    hint = "High"
    hw2 = d.textlength(hint, font=f_small)
    gap = 10
    hint_x = sx1 - 18 - hw2
    label_x = hint_x - gap - lw
    d.text((label_x, row_y + 5), label, font=f_model, fill=WHITE)
    d.text((hint_x, row_y + 6), hint, font=f_small, fill=MUTED)

    os.makedirs(OUT_DIR, exist_ok=True)
    big = os.path.join(OUT_DIR, "promo-1280x800.png")
    img.save(big)
    small = os.path.join(OUT_DIR, "promo-640x400.png")
    img.resize((640, 400), Image.LANCZOS).save(small)
    print("wrote", big)
    print("wrote", small)


if __name__ == "__main__":
    build()
