// Background service worker for cross-origin fetches
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "download-file") {
    const origin = sender.tab?.url && new URL(sender.tab.url).origin;
    if (!origin || !["https://staff-spark.segi.edu.my", "https://student-spark.segi.edu.my"].includes(origin) ||
        !request.url?.startsWith("blob:" + origin + "/")) {
      sendResponse({ error: "Invalid download source" });
      return;
    }
    (async () => {
      const id = await chrome.downloads.download({ url: request.url, filename: "Camu Materials/" + request.filename, conflictAction: "uniquify" });
      // Keep the blob alive until Chrome confirms the file is complete.
      for (let n = 0; n < 600; n++) {
        const [item] = await chrome.downloads.search({ id });
        if (item?.state === "complete") return { ok: true, id };
        if (item?.state === "interrupted") throw new Error(item.error || "Download interrupted");
        await new Promise((resolve) => setTimeout(resolve, 500));
      }
      throw new Error("Download timed out");
    })().then(sendResponse).catch((e) => sendResponse({ error: e.message }));
    return true;
  }
  if (request.action === "fetch-url") {
    fetch(request.url)
      .then((resp) => resp.text())
      .then((html) => sendResponse({ html }))
      .catch((err) => sendResponse({ error: err.message }));
    return true; // keep channel open for async response
  }
});
