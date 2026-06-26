const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");
const outputEl = document.getElementById("output");
const progressEl = document.getElementById("progress");
const progressFill = document.getElementById("progress-fill");
const progressText = document.getElementById("progress-text");
const errorEl = document.getElementById("error");
const scrapeBtn = document.getElementById("scrape-btn");

let scrapedData = null;

function showError(msg) {
  errorEl.textContent = msg;
  errorEl.classList.remove("hidden");
  statusEl.textContent = "Error";
  scrapeBtn.disabled = false;
}

function setStatus(msg) {
  statusEl.textContent = msg;
}

async function getActiveTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

async function sendMessage(action) {
  const tab = await getActiveTab();
  if (!tab) {
    showError("No active tab found.");
    return null;
  }
  if (
    !tab.url.includes("staff-spark.segi.edu.my") &&
    !tab.url.includes("student-spark.segi.edu.my")
  ) {
    showError("Not on a Camu LMS page.");
    return null;
  }
  return new Promise((resolve) => {
    chrome.tabs.sendMessage(tab.id, { action }, (response) => {
      if (chrome.runtime.lastError) {
        showError("Content script not loaded. Refresh the page.");
        resolve(null);
        return;
      }
      resolve(response);
    });
  });
}

scrapeBtn.addEventListener("click", async () => {
  errorEl.classList.add("hidden");
  resultEl.classList.add("hidden");
  progressEl.classList.remove("hidden");
  scrapeBtn.disabled = true;
  setStatus("Scraping Module Topics...");

  const tab = await getActiveTab();
  if (!tab) {
    scrapeBtn.disabled = false;
    return;
  }

  chrome.runtime.onMessage.addListener(function listener(msg) {
    if (msg.action === "scrape-progress") {
      const pct = Math.round((msg.current / msg.total) * 100);
      progressFill.style.width = pct + "%";
      progressText.textContent = `[${msg.current}/${msg.total}] ${msg.label}`;
    }
  });

  const data = await sendMessage("scrape-module-topics");
  if (!data) {
    progressEl.classList.add("hidden");
    scrapeBtn.disabled = false;
    return;
  }

  scrapedData = data;
  displayResults(data);
  progressEl.classList.add("hidden");
  resultEl.classList.remove("hidden");
  scrapeBtn.disabled = false;
  setStatus(`Completed — ${data.contents?.length || 0} items scraped`);
});

function displayResults(data) {
  let summary = `Course: ${data.course?.courseName || "N/A"}\n`;
  summary += `Student: ${data.student?.name || "N/A"}\n`;
  summary += `Status: ${data.status}\n`;
  summary += `Items scraped: ${data.contents?.length || 0}\n\n`;

  if (data.contents && data.contents.length > 0) {
    summary += `=== Scraped Content ===\n`;
    for (const c of data.contents) {
      summary += `\n[${c.topic}] ${c.label}\n`;
      
      if (c.quillText) {
        const preview = c.quillText.substring(0, 200).replace(/\s+/g, " ") + (c.quillText.length > 200 ? "..." : "");
        summary += `  Content: ${preview}\n`;
      } else if (c.iframeBodyText) {
        const preview = c.iframeBodyText.substring(0, 200).replace(/\s+/g, " ") + (c.iframeBodyText.length > 200 ? "..." : "");
        summary += `  Iframe content: ${preview}\n`;
      } else if (c.iframeSrc) {
        summary += `  Iframe URL: ${c.iframeSrc}\n`;
        if (c.iframeError) summary += `  ⚠ Fetch error: ${c.iframeError}\n`;
      } else if (c.fallbackText) {
        const preview = c.fallbackText.substring(0, 200).replace(/\s+/g, " ") + (c.fallbackText.length > 200 ? "..." : "");
        summary += `  Text: ${preview}\n`;
      } else {
        summary += `  (empty)\n`;
      }
    }
  } else {
    summary += `⚠ No content extracted.\n`;
    summary += `Make sure you're on a course content page.\n`;
  }

  outputEl.textContent = summary;
}

document.getElementById("export-json").addEventListener("click", () => {
  if (!scrapedData) return;
  const clean = {
    course: scrapedData.course,
    student: scrapedData.student,
    structure: scrapedData.structure,
    contents: scrapedData.contents.map((c) => ({
      topic: c.topic,
      label: c.label,
      title: c.title,
      text: c.text,
    })),
  };
  const blob = new Blob([JSON.stringify(clean, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `camu-module-topics-${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(url);
  setStatus("JSON exported");
});

document.getElementById("export-markdown").addEventListener("click", () => {
  if (!scrapedData) return;
  const md = toMarkdown(scrapedData);
  const blob = new Blob([md], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `camu-module-topics-${Date.now()}.md`;
  a.click();
  URL.revokeObjectURL(url);
  setStatus("Markdown exported");
});

document.getElementById("copy-btn").addEventListener("click", async () => {
  if (!scrapedData) return;
  await navigator.clipboard.writeText(outputEl.textContent);
  setStatus("Copied to clipboard");
});

function toMarkdown(data) {
  let md = `# ${data.course?.courseName || "Course"}\n\n`;
  if (data.student?.name) md += `**Student:** ${data.student.name}\n\n`;
  md += `---\n\n`;

  if (data.contents) {
    for (const c of data.contents) {
      const heading = c.topic ? `${c.topic} > ${c.label}` : c.label;
      md += `## ${heading}\n\n`;

      if (c.quillText) md += c.quillText.replace(/\s+/g, " ").trim() + "\n\n";
      if (c.iframeBodyText) {
        md += c.iframeBodyText + "\n\n";
      } else if (c.iframeSrc) {
        md += `> Interactive content: [${c.iframeTitle || "Open"}](${c.iframeSrc})\n\n`;
        if (c.iframeError) md += `> ⚠ Fetch error: ${c.iframeError}\n\n`;
      }
      if (c.fallbackText && !c.quillText && !c.iframeBodyText) md += c.fallbackText.replace(/\s+/g, " ").trim() + "\n\n";

      md += `---\n\n`;
    }
  }

  return md;
}
