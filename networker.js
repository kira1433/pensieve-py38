const puppeteer = require('puppeteer');
const args = process.argv;
const ind = args[2];
const networks = [
  [
    [
      { offline: false, downloadThroughput: 2000 * 1024/8, uploadThroughput: 2000 * 1024/8, latency: 50 },
    ],
    10000,
  ],
  [
    [
      { offline: false, downloadThroughput: 1000 * 1024/8, uploadThroughput: 1000 * 1024/8, latency: 50 },
    ],
    10000,
  ],
]

setTimeout(() => {
const browsers = [];
const openBrowserAndNavigate = async (url) => {
  const browser = await puppeteer.launch({
    executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    headless: 'new',
    // headless: false,
    defaultViewport: null,
    args: ['--start-maximized']
  });

  browsers.push(browser);
  
  const [page] = await browser.pages();

  const networkConditions = networks[ind][0]
  const networkCycleTime = networks[ind][1]

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
  // await page.waitForSelector('#videoPlayer');

  browser.on('disconnected', () => {
    clearInterval(intervalId);
  });
};

openBrowserAndNavigate('http://172.16.124.185:8000/A3C.html');
openBrowserAndNavigate('http://172.16.124.185:8001/SAC.html');
openBrowserAndNavigate('http://172.16.124.185:8002/PPO.html');

}, 5000);