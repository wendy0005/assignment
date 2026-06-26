(function () {
  if (window.__camuScraperLoaded) return;
  window.__camuScraperLoaded = true;

  function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

  function cleanText(raw) { return (raw || "").replace(/[]/g, "").trim(); }

  function getCourseInfo() {
    const h6s = document.querySelectorAll("h6");
    const courseName = Array.from(h6s).find((h) => !h.textContent.includes("All Courses"))?.textContent?.trim() || "";
    const meta = document.querySelector(".user-info p, .sub-infocontent p, .dept-name p");
    return { courseName, meta: meta?.textContent?.trim() || "" };
  }

  function getStudentInfo() {
    const nameEl = document.querySelector(".staff-name, .user-name");
    return { name: nameEl?.textContent?.trim() || "" };
  }

  // Fetch iframe content via background service worker
  async function scrapeIframeSrc(url) {
    if (!url) return { html: "", text: "", error: "" };
    try {
      const response = await chrome.runtime.sendMessage({ action: "fetch-url", url });
      if (response.error) return { html: "", text: "", error: response.error };
      const parser = new DOMParser();
      const doc = parser.parseFromString(response.html, "text/html");
      const container = doc.querySelector(".container");
      if (container) return { html: container.innerHTML, text: container.textContent.trim(), error: "" };
      const body = doc.querySelector("body");
      return { html: body?.innerHTML || "", text: body?.textContent?.trim() || "", error: "" };
    } catch (e) { return { html: "", text: "", error: e.message }; }
  }

  // Ensure Content tab is active
  function ensureContentTab() {
    const contentLinks = document.querySelectorAll('a[href*="content-page"], a.nav-link');
    for (const link of contentLinks) {
      if (link.textContent.trim() === "Content" && link.classList.contains("active")) return true;
    }
    // Click Content tab
    for (const link of contentLinks) {
      if (link.textContent.trim() === "Content") {
        link.click();
        return true;
      }
    }
    return false;
  }

  // Get current visible content from the page
  function getCurrentContent() {
    const content = {};

    // 1. From item view (page-content route with quill editor)
    const quill = document.querySelector('.ql-editor.quill-editor-view');
    if (quill) {
      content.quillHtml = quill.innerHTML;
      content.quillText = quill.textContent.trim();
    }

    // 2. Item header info
    const chapName = document.querySelector(".page-chap_name");
    const titleName = document.querySelector(".page-title_name");
    content.topic = chapName?.textContent?.trim() || "";
    content.label = titleName?.textContent?.trim() || "";

    // 3. Iframe
    const iframe = document.querySelector('.ql-video, iframe.ql-video');
    if (iframe) {
      content.iframeSrc = iframe.src || "";
      content.iframeTitle = iframe.title || "";
    }

    // 4. Next-chapter for navigation
    const nextChapter = document.querySelector(".next-chapter");
    if (nextChapter) {
      content.nextChapterTopic = nextChapter.querySelector(".subchapter__name")?.textContent?.trim() || "";
      content.nextChapterItem = nextChapter.querySelector(".subchapter__items")?.textContent?.trim() || "";
      content.hasNextChapter = true;
    } else {
      content.hasNextChapter = false;
    }

    return content;
  }

  // Click next-chapter to go to next item
  function clickNextChapter() {
    const el = document.querySelector(".next-chapter");
    if (!el) return false;
    el.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true }));
    return true;
  }

  // ---- COLLECT ALL SIDEBAR ITEMS ----
  function getSidebarItems() {
    const items = [];
    const seen = new Set();
    const labels = document.querySelectorAll("p.sub-chapter_label");

    for (const p of labels) {
      const text = cleanText(p.textContent);
      if (!text || text.length > 120) continue;

      // Find topic context
      let topic = "";
      let el = p.parentElement;
      for (let i = 0; i < 10; i++) {
        if (!el) break;
        const b = el.querySelector("button");
        if (b) {
          const bt = cleanText(b.textContent);
          if (bt.startsWith("Topic ") && bt.includes("COMPLETE")) { topic = bt.split("COMPLETE")[0].trim(); break; }
        }
        el = el.parentElement;
      }
      if (!topic) continue;

      const key = topic + "||" + text;
      if (seen.has(key)) continue;
      seen.add(key);

      if (/^\d+\s/.test(text)) {
        const clickable = p.closest(".list__date");
        if (clickable) items.push({ label: text, topic, element: clickable });
      }
    }
    return items;
  }

  // Click sidebar item via native event + React fiber fallback
  function clickSidebarItem(element) {
    // Try native click first
    element.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true }));
  }

  // ---- EXPAND ALL ----
  async function expandAll() {
    const btn = Array.from(document.querySelectorAll("button")).find(
      (b) => cleanText(b.textContent) === "Expand all"
    );
    if (btn) { btn.click(); await sleep(2000); }

    const allBtns = document.querySelectorAll("button");
    for (const btn of allBtns) {
      const raw = btn.textContent || "";
      if (!raw.includes("")) continue;
      const t = cleanText(raw);
      if (t.startsWith("Topic ") || /^\d+\.\s/.test(t)) { btn.click(); await sleep(300); }
    }
    await sleep(1000);
  }

  // ---- MAIN SCRAPE ----
  async function scrapeModuleTopics() {
    const result = {
      url: window.location.href,
      timestamp: new Date().toISOString(),
      course: getCourseInfo(),
      student: getStudentInfo(),
      status: "started",
      contents: [],
    };

    // Step 1: Ensure we're on Content tab
    ensureContentTab();
    await sleep(1000);

    // Step 2: Check if we're already in item view (page-content route)
    const isItemView = window.location.hash.includes("page-content");
    
    if (isItemView) {
      // We're already viewing an item - scrape it and use next-chapter
      const first = getCurrentContent();
      let iframeContent = { html: "", text: "" };
      if (first.iframeSrc) iframeContent = await scrapeIframeSrc(first.iframeSrc);

      result.contents.push({
        label: first.label || "Item 1",
        topic: first.topic || "",
        quillHtml: first.quillHtml || "",
        quillText: first.quillText || "",
        iframeSrc: first.iframeSrc || "",
        iframeTitle: first.iframeTitle || "",
        iframeHtml: iframeContent.html || "",
        iframeBodyText: iframeContent.text || "",
        iframeError: iframeContent.error || "",
      });

      // Navigate remaining items via next-chapter
      let prevLabel = first.label || "";
      for (let step = 0; step < 50; step++) {
        if (!clickNextChapter()) break;
        await sleep(3000);

        const c = getCurrentContent();
        const label = c.label || c.nextChapterItem || "";
        if (!label || label === prevLabel) break;
        if (result.contents.some((cc) => cc.label === label)) break;

        let ic = { html: "", text: "" };
        if (c.iframeSrc) ic = await scrapeIframeSrc(c.iframeSrc);

        result.contents.push({
          label,
          topic: c.topic || c.nextChapterTopic || "",
          quillHtml: c.quillHtml || "",
          quillText: c.quillText || "",
          iframeSrc: c.iframeSrc || "",
          iframeTitle: c.iframeTitle || "",
          iframeHtml: ic.html || "",
          iframeBodyText: ic.text || "",
          iframeError: ic.error || "",
        });

        chrome.runtime.sendMessage({
          action: "scrape-progress",
          current: result.contents.length,
          total: "?",
          label: `${c.topic || ""} > ${label}`,
        });

        prevLabel = label;
      }
    } else {
      // We're on the main content page with sidebar
      // Expand all sections first
      await expandAll();

      // Collect all sidebar items
      const items = getSidebarItems();
      if (items.length === 0) {
        result.status = "error: no sidebar items found";
        return result;
      }

      // Click each sidebar item and extract content
      let prevTopic = "";
      for (let i = 0; i < items.length; i++) {
        const { label, topic, element } = items[i];

        chrome.runtime.sendMessage({
          action: "scrape-progress",
          current: i + 1,
          total: items.length,
          label: `${topic} > ${label}`,
        });

        clickSidebarItem(element);
        await sleep(3000);

        const c = getCurrentContent();

        // Check if we're now in item view
        if (window.location.hash.includes("page-content")) {
          let ic = { html: "", text: "" };
          if (c.iframeSrc) ic = await scrapeIframeSrc(c.iframeSrc);

          result.contents.push({
            label: c.label || label,
            topic: c.topic || topic,
            quillHtml: c.quillHtml || "",
            quillText: c.quillText || "",
            iframeSrc: c.iframeSrc || "",
            iframeTitle: c.iframeTitle || "",
            iframeHtml: ic.html || "",
            iframeBodyText: ic.text || "",
            iframeError: ic.error || "",
          });

          // Now in item view, use next-chapter for remaining items
          let prevLabel = c.label || "";
          for (let step = 0; step < 50; step++) {
            if (!clickNextChapter()) break;
            await sleep(3000);

            const nc = getCurrentContent();
            const nLabel = nc.label || nc.nextChapterItem || "";
            if (!nLabel || nLabel === prevLabel) break;
            if (result.contents.some((cc) => cc.label === nLabel)) break;

            let nic = { html: "", text: "" };
            if (nc.iframeSrc) nic = await scrapeIframeSrc(nc.iframeSrc);

            result.contents.push({
              label: nLabel,
              topic: nc.topic || nc.nextChapterTopic || topic,
              quillHtml: nc.quillHtml || "",
              quillText: nc.quillText || "",
              iframeSrc: nc.iframeSrc || "",
              iframeTitle: nc.iframeTitle || "",
              iframeHtml: nic.html || "",
              iframeBodyText: nic.text || "",
              iframeError: nic.error || "",
            });

            chrome.runtime.sendMessage({
              action: "scrape-progress",
              current: result.contents.length,
              total: "?",
              label: `${nc.topic || topic} > ${nLabel}`,
            });

            prevLabel = nLabel;
          }
          break; // exit sidebar loop since we're now in item view + next-chapter
        } else {
          // Not in item view yet - sidebar click didn't navigate
          result.contents.push({
            label,
            topic,
            quillHtml: c.quillHtml || "",
            quillText: c.quillText || "",
            iframeSrc: c.iframeSrc || "",
            iframeTitle: c.iframeTitle || "",
            fallbackText: (document.querySelector('.tab-pane.show.active')?.textContent?.trim() || "").substring(0, 500),
          });
        }
      }
    }

    result.status = "completed";
    return result;
  }

  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "scrape-module-topics") {
      scrapeModuleTopics().then((data) => sendResponse(data));
      return true;
    }
  });
})();
