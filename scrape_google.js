const puppeteer = require('puppeteer-core');
const fs = require('fs');

(async () => {
  console.log('Launching browser...');
  const browser = await puppeteer.launch({
    executablePath: 'E:\\cloning_project\\face-identification\\chrome\\win64-131.0.6778.204\\chrome-win64\\chrome.exe',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-web-security', '--ignore-certificate-errors']
  });
  console.log('Browser launched. Opening new page...');
  const page = await browser.newPage();
  
  console.log('Navigating to https://www.google.com ...');
  await page.goto('https://www.google.com', { waitUntil: 'domcontentloaded', timeout: 60000 });
  
  const title = await page.title();
  console.log(`Page title successfully scraped: ${title}`);
  
  // optionally get some content
  const html = await page.content();
  console.log(`Successfully fetched HTML. Length: ${html.length} characters.`);

  console.log('Taking a screenshot...');
  const screenshotPath = 'google_screenshot.png';
  await page.screenshot({path: screenshotPath});
  console.log(`Screenshot saved to ${screenshotPath}`);

  await browser.close();
  console.log('Browser closed. Test complete.');
})();
