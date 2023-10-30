const puppeteer = require('puppeteer');

setTimeout(() => {

const browsers = [];
const openBrowserAndNavigate = async (url) => {
  const browser = await puppeteer.launch({
    executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    headless: 'new',
    defaultViewport: null,
    args: ['--start-maximized']
  });

  browsers.push(browser);
  
  const [page] = await browser.pages();

  const networkConditions = [
    { offline: false, downloadThroughput: 2000 * 1024/8, uploadThroughput: 2000 * 1024/8, latency: 50 },
    { offline: false, downloadThroughput: 2000 * 1024/8, uploadThroughput: 2000 * 1024/8, latency: 50 },
    { offline: false, downloadThroughput: 2000 * 1024/8, uploadThroughput: 2000 * 1024/8, latency: 50 },
    { offline: false, downloadThroughput: 500 * 1024/8, uploadThroughput: 500 * 1024/8, latency: 50 },
    { offline: false, downloadThroughput: 2000 * 1024/8, uploadThroughput: 2000 * 1024/8, latency: 50 }
  ];
  const networkCycleTime = 10000

  const client = await page.target().createCDPSession();
  await client.send("Network.enable");
  let i = 0;
  await client.send('Network.emulateNetworkConditions', networkConditions[i]);
  await client.send('Network.clearBrowserCache');
  i = (i + 1) % networkConditions.length;
  const intervalId = setInterval(async () => {
    await client.send('Network.emulateNetworkConditions', networkConditions[i]);
    await client.send('Network.clearBrowserCache');
    i = (i + 1) % networkConditions.length;
  }, networkCycleTime);

  await page.goto(url);
  await page.waitForSelector('#videoPlayer');

  browser.on('disconnected', () => {
    clearInterval(intervalId);
  });
};

openBrowserAndNavigate('http://172.16.124.185:8000/A3C.html');
openBrowserAndNavigate('http://172.16.124.185:8001/SAC.html');
openBrowserAndNavigate('http://172.16.124.185:8002/PPO.html');


}, 5000);