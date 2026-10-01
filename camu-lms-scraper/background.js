// Chrome download history provides file existence; storage tracks source revisions.
const pendingDownloads = new Map();
const trustedOrigins = ["https://staff-spark.segi.edu.my", "https://student-spark.segi.edu.my"];

function downloadPath(filename) {
  if (typeof filename !== "string" || !filename || filename.includes("\\") ||
      filename.split("/").some((part) => !part || part === "." || part === "..") ||
      filename.split("/").length > 2) {
    throw new Error("Invalid filename");
  }
  return "Camu Materials/" + filename;
}

async function findExisting(filename, sourceKey) {
  const path = downloadPath(filename);
  const storageKey = "camu-download:" + path;
  const stored = (await chrome.storage.local.get(storageKey))[storageKey];
  // A changed source must be downloaded, even if its display name stays the same.
  if (stored && stored.sourceKey !== sourceKey) return null;
  const candidates = stored
    ? await chrome.downloads.search({ id: stored.id })
    : await chrome.downloads.search({ filenameRegex: path.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "$", state: "complete", exists: true });
  const item = candidates.find((item) => item.state === "complete" && item.exists && item.fileSize > 0);
  if (!item) return null;
  // Adopt files downloaded by earlier scraper versions on the first check.
  if (!stored) await chrome.storage.local.set({ [storageKey]: { id: item.id, sourceKey } });
  return { ok: true, skipped: true, id: item.id, filename: item.filename };
}

async function saveDownload(request) {
  const existing = await findExisting(request.filename, request.sourceKey);
  if (existing) return existing;
  const id = await chrome.downloads.download({
    url: request.url, filename: downloadPath(request.filename), conflictAction: "overwrite",
  });
  for (let n = 0; n < 600; n++) {
    const [item] = await chrome.downloads.search({ id });
    if (item?.state === "complete") {
      await chrome.storage.local.set({
        ["camu-download:" + downloadPath(request.filename)]: { id, sourceKey: request.sourceKey },
      });
      return { ok: true, skipped: false, id, filename: item.filename };
    }
    if (item?.state === "interrupted") throw new Error(item.error || "Download interrupted");
    await new Promise((resolve) => setTimeout(resolve, 500));
  }
  throw new Error("Download timed out");
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (["check-download", "download-file"].includes(request.action)) {
    let origin;
    try { origin = new URL(sender.tab?.url).origin; } catch (_) { /* invalid sender */ }
    if (!trustedOrigins.includes(origin) || typeof request.sourceKey !== "string" || !request.sourceKey ||
        (request.action === "download-file" && !request.url?.startsWith("blob:" + origin + "/"))) {
      sendResponse({ error: "Invalid download source" });
      return;
    }
    (async () => {
      if (request.action === "check-download") {
        return await findExisting(request.filename, request.sourceKey) || { ok: true, skipped: false };
      }
      const key = downloadPath(request.filename);
      const pending = pendingDownloads.get(key);
      if (pending) await pending.catch(() => {});
      const job = saveDownload(request);
      pendingDownloads.set(key, job);
      try { return await job; }
      finally { if (pendingDownloads.get(key) === job) pendingDownloads.delete(key); }
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
