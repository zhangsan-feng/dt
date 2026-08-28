import path from "node:path";
import { pathToFileURL } from "node:url";

function option(name, fallback = "") {
  const prefix = `--${name}=`;
  const value = process.argv.find((arg) => arg.startsWith(prefix));
  return value ? value.slice(prefix.length) : fallback;
}

function targetUrl() {
  const url = process.argv.slice(1).find((arg) => /^https?:\/\//i.test(arg));
  if (!url) throw new Error("browser_request requires an http(s) URL");
  return url;
}

function isTextContent(contentType) {
  return /(?:^|\/)json|(?:^|\/)javascript|(?:^|\/)xml|(?:^|\/)text|html/i.test(contentType);
}

async function loadChromium() {
  const configured = process.env.BROWSER_PATCHRIGHT_MODULE;
  const modulePath = configured
    ? path.resolve(configured)
    : path.join(
        process.cwd(),
        "js-reverse-mcp",
        "node_modules",
        "@zhizhuodemao",
        "patchright",
        "index.mjs",
      );
  const loaded = await import(pathToFileURL(modulePath).href);
  if (!loaded.chromium) throw new Error("Patchright chromium export is unavailable");
  return loaded.chromium;
}

async function main() {
  const chromium = await loadChromium();
  const headless = option("headless", process.env.BROWSER_HEADLESS || "false") === "true";
  const timeout = Number(option("timeout-ms", "75000"));
  const launchOptions = {
    channel: option("channel", "chrome"),
    headless,
    args: ["--test-type", "--hide-crash-restore-bubble"],
  };
  const contextOptions = { viewport: null, ignoreHTTPSErrors: true };
  let context;
  let browser;

  try {
    browser = await chromium.launch(launchOptions);
    context = await browser.newContext(contextOptions);

    const page = context.pages()[0] || (await context.newPage());
    const response = await page.goto(targetUrl(), {
      waitUntil: "domcontentloaded",
      timeout,
    });
    if (!response) throw new Error("browser navigation returned no response");

    const request = response.request();
    const responseHeaders = response.headers();
    let body = null;
    let bodyEncoding = "utf8";
    try {
      const bodyBuffer = await response.body();
      bodyEncoding = isTextContent(responseHeaders["content-type"] || "") ? "utf8" : "base64";
      body = bodyBuffer.toString(bodyEncoding);
    } catch (error) {
      console.error(`response body unavailable: ${error.message}`);
    }

    console.log(JSON.stringify({
      request: {
        url: request.url(),
        method: request.method(),
        headers: request.headers(),
        body: request.postData() || null,
      },
      response: {
        url: response.url(),
        statusCode: response.status(),
        statusText: response.statusText(),
        headers: responseHeaders,
        body,
        bodyEncoding,
      },
    }));
  } finally {
    if (context) await context.close().catch(() => {});
    if (browser) await browser.close().catch(() => {});
  }
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : error);
  process.exitCode = 1;
});
