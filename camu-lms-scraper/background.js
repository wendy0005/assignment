// Background service worker for cross-origin fetches
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "fetch-url") {
    fetch(request.url)
      .then((resp) => resp.text())
      .then((html) => sendResponse({ html }))
      .catch((err) => sendResponse({ error: err.message }));
    return true; // keep channel open for async response
  }
});
