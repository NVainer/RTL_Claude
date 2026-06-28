"""Generate PNG icons for the Claude RTL extension.

Produces 16/48/128 px icons: a rounded Claude-orange tile with a white
Hebrew aleph (א) — signalling "Hebrew / RTL". Run from the repo root:

    python tools/make_icons.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ORANGE = (217, 119, 87, 255)   # Claude send-button terracotta
WHITE = (255, 255, 255, 255)
OUT_DIR = os.path.join("claude-rtl", "icons")

# A font that contains the Hebrew aleph. Arial ships on Windows.
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def make(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    radius = max(2, round(size * 0.22))
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=ORANGE)

    glyph = "א"  # Hebrew letter aleph
    font = load_font(round(size * 0.74))
    # Center the glyph using its bounding box.
    box = d.textbbox((0, 0), glyph, font=font)
    gw, gh = box[2] - box[0], box[3] - box[1]
    x = (size - gw) / 2 - box[0]
    y = (size - gh) / 2 - box[1]
    d.text((x, y), glyph, font=font, fill=WHITE)
    return img


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for size in (16, 48, 128):
        path = os.path.join(OUT_DIR, f"icon{size}.png")
        make(size).save(path)
        print("wrote", path)


if __name__ == "__main__":
    main()
