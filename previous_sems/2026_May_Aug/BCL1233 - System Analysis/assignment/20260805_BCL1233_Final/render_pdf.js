const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const htmlPath = path.resolve(__dirname, 'BCL1233_FinalAssessment_Answers.html');
  const pdfPath = path.resolve(__dirname, 'BCL1233_FinalAssessment_Answers.pdf');
  
  console.log('Launching Playwright Chrome...');
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true
  });
  
  const page = await browser.newPage();
  console.log('Navigating to HTML file:', `file://${htmlPath}`);
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle' });
  
  console.log('Waiting for Mermaid diagrams to complete rendering...');
  try {
    await page.waitForSelector('.mermaid svg', { timeout: 20000 });
  } catch (err) {
    console.warn('Warning: .mermaid svg timeout, proceeding to check document body rendered class...');
  }
  
  try {
    await page.waitForFunction(() => document.body.classList.contains('rendered'), { timeout: 10000 });
  } catch (err) {
    console.warn('Warning: body rendered class timeout, proceeding after fallback delay...');
  }
  
  await page.waitForTimeout(3000);
  
  console.log('Generating A4 PDF...');
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    margin: {
      top: '20mm',
      bottom: '20mm',
      left: '20mm',
      right: '20mm'
    }
  });
  
  console.log('PDF rendered successfully:', pdfPath);
  await browser.close();
})();
