import path from "node:path";
import { pathToFileURL } from "node:url";

const DETAIL_PATH = "/aweme/v1/web/aweme/detail/";

function option(name, fallback = "") {
  const prefix = `--${name}=`;
  const value = process.argv.find((arg) => arg.startsWith(prefix));
  return value ? value.slice(prefix.length) : fallback;
}

function positionalArgs() {
  return process.argv.slice(2).filter((arg) => !arg.startsWith("--"));
}

function isTextContent(contentType) {
  return /(?:^|\/)json|(?:^|\/)javascript|(?:^|\/)xml|(?:^|\/)text|html/i.test(contentType);
}

async function sendOverriddenDetail(page, templateUrl, overrideAwemeId) {
  return page.evaluate(
    async ({ templateUrl, overrideAwemeId }) => {
      const originalOpen = XMLHttpRequest.prototype.open;
      if (!originalOpen || originalOpen.__dtAwemeIdHook) {
        throw new Error("XMLHttpRequest.open hook is unavailable");
      }

      const hookedOpen = function(method, url, ...rest) {
        let nextUrl = url;
        try {
          const requestUrl = new URL(String(url), window.location.href);
          if (requestUrl.pathname === "/aweme/v1/web/aweme/detail/") {
            const rawUrl = String(url);
            const replacedUrl = rawUrl.replace(
              /([?&]aweme_id=)[^&#]*/i,
              (match, prefix) => prefix + overrideAwemeId,
            );
            if (replacedUrl !== rawUrl) {
              nextUrl = replacedUrl;
            } else {
              const separator = rawUrl.includes("?") ? "&" : "?";
              nextUrl = rawUrl + separator + "aweme_id=" + overrideAwemeId;
            }
          }
        } catch {
          // Keep the original URL when the page passes a non-standard URL value.
        }
        return originalOpen.call(this, method, nextUrl, ...rest);
      };

      Object.defineProperty(hookedOpen, "__dtAwemeIdHook", { value: true });
      XMLHttpRequest.prototype.open = hookedOpen;

      const requestUrl = new URL(templateUrl, window.location.href);
      for (const key of ["a_bogus", "timestamp", "x-secsdk-web-signature"]) {
        requestUrl.searchParams.delete(key);
      }
      requestUrl.searchParams.set("aweme_id", overrideAwemeId);

      const xhr = new XMLHttpRequest();
      xhr.open("GET", requestUrl.href, true);
      xhr.send();
      return { sent: true };
    },
    { templateUrl, overrideAwemeId },
  );
}

async function sendOverriddenDetailWithRetry(page, templateUrl, overrideAwemeId) {
  try {
    return await sendOverriddenDetail(page, templateUrl, overrideAwemeId);
  } catch (error) {
    if (!/execution context was destroyed|most likely because of a navigation/i.test(error.message)) {
      throw error;
    }
    await new Promise((resolve) => setTimeout(resolve, 1500));
    return sendOverriddenDetail(page, templateUrl, overrideAwemeId);
  }
}

function isValidDetailPayload(response, body) {
  const contentType = response.headers()["content-type"] || "";
  if (response.status() !== 200 || !contentType.includes("application/json")) return null;
  try {
    const payload = JSON.parse(body);
    return payload && payload.aweme_detail ? payload : null;
  } catch {
    return null;
  }
}

function waitForResponse(page, responsePattern, expectedAwemeId = "") {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      page.off("response", onResponse);
      reject(new Error(`timed out waiting for response matching: ${responsePattern}`));
    }, Number(option("timeout-ms", "75000")));

    async function onResponse(response) {
      if (!response.url().includes(responsePattern)) return;
      try {
        const requestUrl = new URL(response.url());
        const requestAwemeId = requestUrl.searchParams.get("aweme_id") || "";
        if (expectedAwemeId && requestAwemeId !== expectedAwemeId) {
          if (process.env.BROWSER_DEBUG === "true") {
            console.error(
              `detail response skipped status=${response.status()} expected_id_length=${expectedAwemeId.length} actual_id_length=${requestAwemeId.length}`,
            );
          }
          return;
        }
        const responseHeaders = response.headers();
        const bodyEncoding = isTextContent(responseHeaders["content-type"] || "")
          ? "utf8"
          : "base64";
        const bodyBuffer = await response.body();
        const body = bodyBuffer.toString(bodyEncoding);
        const isDetail = responsePattern.includes(DETAIL_PATH);
        const payload = isDetail ? isValidDetailPayload(response, body) : null;
        if (isDetail && !payload) {
          if (process.env.BROWSER_DEBUG === "true") {
            console.error(
              `detail response skipped status=${response.status()} content_type=${responseHeaders["content-type"] || ""} body_length=${body.length}`,
            );
          }
          return;
        }
        clearTimeout(timeout);
        page.off("response", onResponse);
        resolve({ response, payload, bodyBuffer, bodyEncoding });
      } catch {
        // Ignore transient risk-control or non-JSON detail responses.
      }
    }

    page.on("response", onResponse);
  });
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
  const [targetUrl, responsePattern] = positionalArgs();
  if (!/^https?:\/\//i.test(targetUrl || "")) {
    throw new Error("browser_request_listener requires an http(s) URL");
  }
  if (!responsePattern) {
    throw new Error("browser_request_listener requires a response URL pattern");
  }

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
    const overrideAwemeId = option("override-aweme-id");
    if (overrideAwemeId && !/^\d{8,}$/.test(overrideAwemeId)) {
      throw new Error("override-aweme-id must be a numeric value");
    }
    const initialResponsePromise = waitForResponse(page, responsePattern);

    await page.goto(targetUrl, { waitUntil: "domcontentloaded", timeout }).catch((error) => {
      console.error(`page navigation did not finish: ${error.message}`);
    });
    let found = await initialResponsePromise;

    if (overrideAwemeId) {
      const overriddenResponsePromise = waitForResponse(page, responsePattern, overrideAwemeId);
      await sendOverriddenDetailWithRetry(
        page,
        found.response.request().url(),
        overrideAwemeId,
      );
      found = await overriddenResponsePromise;
    }

    const request = found.response.request();
    const responseHeaders = found.response.headers();
    console.log(
      JSON.stringify({
        request: {
          url: request.url(),
          method: request.method(),
          headers: request.headers(),
          body: request.postData() || null,
        },
        response: {
          url: found.response.url(),
          statusCode: found.response.status(),
          statusText: found.response.statusText(),
          headers: responseHeaders,
          body: found.bodyBuffer.toString(found.bodyEncoding),
          bodyEncoding: found.bodyEncoding,
        },
      }),
    );
  } finally {
    if (context) await context.close().catch(() => {});
    if (browser) await browser.close().catch(() => {});
  }
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : error);
  process.exitCode = 1;
});
