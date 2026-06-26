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

  // ---- FETCH AVAILABLE TOPICS ----
  async function fetchTopicList() {
    ensureContentTab();
    await sleep(1000);
    await expandAll();

    const topics = [];
    const seen = new Set();
    const buttons = document.querySelectorAll("button");

    for (const btn of buttons) {
      const text = cleanText(btn.textContent);
      if (text.startsWith("Topic ") && text.includes("COMPLETE")) {
        const name = text.split("COMPLETE")[0].trim();
        if (!seen.has(name)) {
          seen.add(name);
          topics.push(name);
        }
      }
    }
    return topics;
  }

  // ---- GO BACK TO MAIN PAGE FROM ITEM VIEW ----
  async function goBackToMainPage() {
    const closeSelectors = [
      "button.page-close",
      ".page-close",
      "button.close",
      ".btn-close",
      ".hide-content_view",
      "[aria-label='Close']",
      "[aria-label='Back']",
      ".page-back",
      ".nav-link.back",
    ];
    for (const sel of closeSelectors) {
      const el = document.querySelector(sel);
      if (el) {
        el.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true }));
        await sleep(2000);
        const stillInView = document.querySelector(".hide-content_view");
        if (!window.location.hash.includes("page-content") || !stillInView) return true;
      }
    }
    return false;
  }

  // ---- COLLECT ALL SIDEBAR ITEMS ----
  function getSidebarItems(topicFilter) {
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
      if (topicFilter && topicFilter.length > 0 && !topicFilter.includes(topic)) continue;

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

    // Wait for AJAX-loaded items to populate expanded panels
    for (let w = 0; w < 30; w++) {
      if (!document.querySelector(".no-cont_height")) break;
      await sleep(500);
    }
    await sleep(1000);
  }

  // ---- MAIN SCRAPE ----
  async function scrapeModuleTopics(selectedTopics) {
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
        if (result.contents.some((cc) => cc.topic === (c.topic || c.nextChapterTopic || "") && cc.label === label)) break;
        if (selectedTopics && selectedTopics.length > 0) {
          const itemTopic = c.topic || c.nextChapterTopic || "";
          if (itemTopic && !selectedTopics.includes(itemTopic)) break;
        }

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

      // Determine which topics to scrape
      let topicsToScrape = selectedTopics;
      if (!topicsToScrape || topicsToScrape.length === 0) {
        topicsToScrape = await fetchTopicList();
      }
      if (!topicsToScrape || topicsToScrape.length === 0) {
        result.status = "error: no topics found";
        return result;
      }

      // Process each topic one at a time — re-expand, get fresh items, scrape, close
      for (const topicName of topicsToScrape) {
        // Re-expand sidebar (topics may have collapsed after returning from item view)
        await expandAll();

        // Get fresh items for this topic
        const topicItems = getSidebarItems([topicName]);
        if (topicItems.length === 0) continue;
        const firstItem = topicItems[0];

        chrome.runtime.sendMessage({
          action: "scrape-progress",
          current: result.contents.length + 1,
          total: "?",
          label: `${topicName} > ${firstItem.label}`,
        });

        clickSidebarItem(firstItem.element);
        await sleep(3000);

        const c = getCurrentContent();

        if (window.location.hash.includes("page-content")) {
          let ic = { html: "", text: "" };
          if (c.iframeSrc) ic = await scrapeIframeSrc(c.iframeSrc);

          result.contents.push({
            label: c.label || firstItem.label,
            topic: c.topic || topicName,
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
            if (result.contents.some((cc) => cc.topic === (nc.topic || nc.nextChapterTopic || "") && cc.label === nLabel)) break;
            if (selectedTopics && selectedTopics.length > 0) {
              const itemTopic = nc.topic || nc.nextChapterTopic || "";
              if (itemTopic && !selectedTopics.includes(itemTopic)) break;
            }

            let nic = { html: "", text: "" };
            if (nc.iframeSrc) nic = await scrapeIframeSrc(nc.iframeSrc);

            result.contents.push({
              label: nLabel,
              topic: nc.topic || nc.nextChapterTopic || topicName,
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
              label: `${nc.topic || topicName} > ${nLabel}`,
            });

            prevLabel = nLabel;
          }

          // Go back to main page for next topic
          if (!await goBackToMainPage()) break;
          await sleep(2000);
        } else {
          // Not in item view - sidebar click didn't navigate
          result.contents.push({
            label: firstItem.label,
            topic: topicName,
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

// ---- LECTURE NOTES PDF DOWNLOAD ----

async function expandLectureNotesSections() {
  const panelNameEls = document.querySelectorAll('p.panel-name');
  let lectureNotesBtn = null;
  let lectureNotesPanelId = null;
  for (const el of panelNameEls) {
    if (el.textContent.trim() === 'LECTURE NOTES') {
      lectureNotesBtn = el.closest('button');
      lectureNotesPanelId = lectureNotesBtn?.getAttribute('data-target');
      break;
    }
  }
  if (!lectureNotesBtn) throw new Error('LECTURE NOTES section not found');

  let panel = lectureNotesPanelId ? document.querySelector(lectureNotesPanelId) : null;

  if (panel && !panel.classList.contains('show')) {
    lectureNotesBtn.click();
    await sleep(1500);
  }

  if (!panel) {
    const header = lectureNotesBtn.closest('.panel-header');
    if (header) panel = header.nextElementSibling;
  }
  if (!panel) throw new Error('Could not find LECTURE NOTES panel');

  const subBtns = panel.querySelectorAll('.sub-chapter_content button[data-toggle="collapse"]');
  for (const btn of subBtns) {
    const subTargetId = btn.getAttribute('data-target');
    if (!subTargetId) continue;
    const subPanel = document.querySelector(subTargetId);
    if (!subPanel || subPanel.classList.contains('show')) continue;
    btn.click();
    await sleep(600);
  }

  await sleep(2000);
}

function collectLectureNoteItems() {
  const items = [];
  const rows = document.querySelectorAll('.list-cont_inbox');

  for (const row of rows) {
    const svgPath = row.querySelector('div.panel-list_items svg path');
    if (!svgPath) continue;
    const d = svgPath.getAttribute('d') || '';
    if (!d.startsWith('M21.44')) continue; // paperclip icon only

    const label = row.querySelector('.sub-chapter_label')?.textContent?.trim() || '';
    if (!label) continue;

    const collapsePanel = row.closest('.panel-collapse');
    let chapter = '';
    if (collapsePanel && collapsePanel.id) {
      const btn = document.querySelector(`button[data-target="#${collapsePanel.id}"]`);
      chapter = btn?.querySelector('.sub-chap_name')?.textContent?.trim() || '';
    }

    items.push({ label, chapter, element: row });
  }

  return items;
}

async function waitForFileView(timeout) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    if (document.querySelector('.file-content_box')) return true;
    if (document.querySelector('i.img-download_icon')) return true;
    await sleep(500);
  }
  return false;
}

async function closeFileView() {
  const closeSelectors = [
    '.hide-content_view',
    'button.page-close',
    '.page-close',
    'button.close',
    '.btn-close',
    '[aria-label="Close"]',
    '[aria-label="Back"]',
    '.page-back',
  ];
  for (const sel of closeSelectors) {
    const el = document.querySelector(sel);
    if (el) {
      el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      const start = Date.now();
      while (Date.now() - start < 8000) {
        await sleep(500);
        if (!document.querySelector('.file-content_box') && !document.querySelector('i.img-download_icon')) return true;
      }
    }
  }
  return !document.querySelector('.file-content_box');
}

async function downloadAllLectureNotes() {
  const result = { status: "started", total: 0, downloaded: 0, failed: 0 };

  if (document.querySelector('.file-content_box')) {
    await closeFileView();
    await sleep(2000);
  }

  await expandLectureNotesSections();

  const initialItems = collectLectureNoteItems();
  result.total = initialItems.length;

  if (result.total === 0) {
    result.status = "completed";
    return result;
  }

  chrome.runtime.sendMessage({
    action: "download-progress",
    current: 0,
    total: result.total,
    label: `Found ${result.total} items in LECTURE NOTES`,
  }).catch(() => {});

  for (let i = 0; i < result.total; i++) {
    await expandLectureNotesSections();
    const freshItems = collectLectureNoteItems();
    const item = freshItems[i];

    if (!item || !item.element) {
      result.failed++;
      continue;
    }

    const downloadLabel = `${item.chapter} > ${item.label}`;

    try {
      item.element.scrollIntoView({ block: 'center' });
      await sleep(500);
      item.element.click();

      const loaded = await waitForFileView(15000);
      if (!loaded) {
        throw new Error('File view did not load');
      }
      await sleep(2000);

      const downloadIcon = document.querySelector('i.img-download_icon span');
      if (downloadIcon && downloadIcon.isConnected) {
        downloadIcon.click();
        await sleep(3000);
        result.downloaded++;
      } else {
        throw new Error('Download icon not found');
      }

      await closeFileView();
      await sleep(1500);
    } catch (e) {
      result.failed++;
      if (document.querySelector('.file-content_box')) {
        await closeFileView();
        await sleep(1500);
      }
    }

    chrome.runtime.sendMessage({
      action: "download-progress",
      current: i + 1,
      total: result.total,
      label: downloadLabel,
    }).catch(() => {});
  }

  result.status = "completed";
  return result;
}

  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "get-topics") {
      fetchTopicList().then((topics) => sendResponse({ topics }));
      return true;
    }
    if (request.action === "scrape-module-topics") {
      scrapeModuleTopics(request.topics).then((data) => sendResponse(data));
      return true;
    }
    if (request.action === "download-lecture-notes") {
      downloadAllLectureNotes().then((data) => sendResponse(data));
      return true;
    }
  });
})();
