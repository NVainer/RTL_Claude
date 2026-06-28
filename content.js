(() => {
  "use strict";

  const KEY = "crtlEnabled";

  // Hebrew + Arabic (incl. presentation forms) and Latin ranges.
  const RTL = /[\u0590-\u05FF\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB1D-\uFDFF\uFE70-\uFEFF]/g;
  const LTR = /[A-Za-z\u00C0-\u024F]/g;

  // Block-level text elements we may flip.
  const SELECTOR = "p, li, h1, h2, h3, h4, h5, h6, blockquote, td, th, summary";
  const MARK = "data-crtl"; // marks attributes WE added, so teardown is clean/reversible.

  let enabled = true;

  // Majority rule: a block flips to RTL only if it has more Hebrew/Arabic than Latin chars.
  // Returns "rtl" or null (we never force ltr — we just leave LTR text untouched).
  function wantsRtl(text) {
    const r = (text.match(RTL) || []).length;
    if (!r) return false;
    const l = (text.match(LTR) || []).length;
    return r >= l;
  }

  function tag(el) {
    if (!el || el.nodeType !== 1) return;
    if (el.closest("pre, code")) return; // never touch code
    if (!wantsRtl(el.textContent || "")) return;

    if (el.getAttribute("dir") !== "rtl") {
      el.setAttribute("dir", "rtl");
      el.setAttribute(MARK, "1");
    }
    // Fix the list container too, so the marker (number/bullet) sits on the right.
    const list = el.closest("ul, ol");
    if (list && list.getAttribute("dir") !== "rtl") {
      list.setAttribute("dir", "rtl");
      list.setAttribute(MARK, "1");
    }
  }

  function scan(node) {
    if (!node || node.nodeType !== 1) return;
    if (node.matches && node.matches(SELECTOR)) tag(node);
    if (node.querySelectorAll) node.querySelectorAll(SELECTOR).forEach(tag);
  }

  function clearAll() {
    document.querySelectorAll("[" + MARK + "]").forEach((el) => {
      el.removeAttribute("dir");
      el.removeAttribute(MARK);
    });
  }

  function enable() {
    document.documentElement.classList.add("crtl-on");
    if (document.body) scan(document.body);
  }

  function disable() {
    document.documentElement.classList.remove("crtl-on");
    clearAll();
  }

  // Debounced observer so streaming responses don't thrash the DOM.
  const pending = new Set();
  let queued = false;
  const flush = () => {
    queued = false;
    const nodes = [...pending];
    pending.clear();
    nodes.forEach((n) => scan(n.nodeType === 1 ? n : n.parentElement));
  };
  const observer = new MutationObserver((muts) => {
    if (!enabled) return;
    for (const m of muts) {
      m.addedNodes.forEach((n) => pending.add(n));
      if (m.type === "characterData" && m.target.parentElement) {
        pending.add(m.target.parentElement);
      }
    }
    if (!queued) {
      queued = true;
      requestAnimationFrame(flush);
    }
  });

  function start() {
    if (!document.body) {
      requestAnimationFrame(start);
      return;
    }
    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true,
    });
  }

  chrome.storage.local.get(KEY, (res) => {
    enabled = res[KEY] !== false; // default ON
    if (enabled) enable();
    start();
  });

  chrome.storage.onChanged.addListener((changes) => {
    if (KEY in changes) {
      enabled = changes[KEY].newValue !== false;
      enabled ? enable() : disable();
    }
  });
})();
