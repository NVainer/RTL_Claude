# Claude RTL

A tiny Chrome extension that adds **right-to-left (RTL)** support for Hebrew and
Arabic on [claude.ai](https://claude.ai). Each paragraph is auto-directed by its
first strong character, so Hebrew sentences align right even when they're full of
English technical terms — while code blocks always stay left-to-right.

## Features

- **Per-paragraph direction** via `dir="auto"` — no clumsy whole-page flip.
- **Input box included** — the composer (ProseMirror) is handled with
  `unicode-bidi: plaintext`, which survives its re-renders.
- **Code stays LTR** — `pre`, `code`, `kbd`, `samp` are never flipped, even with
  Hebrew comments.
- **One-click toggle** in the toolbar popup; state persists across sessions.
- **Fully reversible** — every attribute the extension adds is tagged and removed
  when you turn it off.

## Install (from source)

1. Download or clone this repo.
2. Go to `chrome://extensions`, enable **Developer mode** (top right).
3. Click **Load unpacked** and select the [`claude-rtl/`](claude-rtl) folder.
4. Open [claude.ai](https://claude.ai), reload the tab, and type in Hebrew.

## Project layout

```
claude-rtl/          # the extension (load this folder unpacked)
  manifest.json
  content.js         # detects RTL blocks, tags them dir="auto"
  rtl.css            # alignment + input composer + code-stays-LTR rules
  popup.html/js      # ON/OFF toggle
  icons/             # 16 / 48 / 128 px
tools/make_icons.py  # regenerates the icons
```

## Privacy

The extension stores a single on/off flag locally (`chrome.storage`) and sends no
data anywhere. See [PRIVACY.md](PRIVACY.md).

## License

[MIT](LICENSE)
