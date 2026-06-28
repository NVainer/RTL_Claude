# Security

## Threat model

Claude RTL is a content-script extension that adjusts text *direction* on
claude.ai. By design it:

- makes **no network requests** and contains **no remote or dynamically
  evaluated code** (no `eval`, `Function`, or string timers);
- uses **no dangerous DOM sinks** — it only reads `textContent` and sets a
  constant `dir="auto"` attribute, never `innerHTML`/`outerHTML`/`document.write`;
- **does not read, store, or transmit** the content of your conversations;
- stores a **single boolean** (on/off) in `chrome.storage.local` on your device;
- requests **least-privilege** permissions: `storage` plus host access limited to
  `claude.ai` / `claude.site` (never `<all_urls>`);
- declares an explicit Content-Security-Policy for extension pages
  (`script-src 'self'; object-src 'self'; base-uri 'none'`).

## Reporting a vulnerability

If you believe you've found a security issue, please **do not** open a public
issue with exploit details. Instead, open a
[GitHub security advisory](https://github.com/NVainer/RTL_Claude/security/advisories/new)
or email the maintainer. We aim to respond within a few days.
