import {
  closeBrowser,
  launchBrowser,
  openPage,
  option,
  positionalArgs,
  timeoutMs,
} from "./browser_runtime.mjs";

function targetUrl() {
  const url = positionalArgs().find((arg) => /^https?:\/\//i.test(arg));
  if (!url) throw new Error("browser_request requires an http(s) URL");
  return url;
}

function isTextContent(contentType) {
  return /(?:^|\/)json|(?:^|\/)javascript|(?:^|\/)xml|(?:^|\/)text|html/i.test(contentType);
}

async function main() {
  let context;
  let browser;

  try {
    ({ browser, context } = await launchBrowser());
    const page = await openPage(context);
    const response = await page.goto(targetUrl(), {
      waitUntil: "domcontentloaded",
      timeout: timeoutMs(),
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
    await closeBrowser({ browser, context });
  }
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : error);
  process.exitCode = 1;
});
