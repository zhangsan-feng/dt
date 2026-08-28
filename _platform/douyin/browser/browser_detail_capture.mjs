import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(SCRIPT_DIR, "..", "..", "..");
const DEBUG = process.env.BROWSER_DEBUG === "true";

function option(name, fallback = "") {
  const prefix = `--${name}=`;
  const value = process.argv.find((arg) => arg.startsWith(prefix));
  return value ? value.slice(prefix.length) : fallback;
}

function getTargetUrl() {
  const value = process.argv.slice(2).find((arg) => !arg.startsWith("--")) || "";
  if (/^https?:\/\//i.test(value)) return value;
  if (/^\d{8,}$/.test(value)) return `https://www.douyin.com/video/${value}`;
  return "";
}

function parseJsonOption(name, fallback) {
  const rawValue = option(name);
  if (!rawValue) return fallback;
  try {
    return JSON.parse(rawValue);
  } catch (error) {
    throw new Error(`--${name} must be valid JSON: ${error.message}`);
  }
}

function normalizeQueryReplacements(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error("replace-query must be a JSON object");
  }
  return Object.fromEntries(
    Object.entries(value).map(([key, replacement]) => {
      if (!key || replacement === null || replacement === undefined) {
        throw new Error("replace-query keys and values must be non-empty");
      }
      return [key, String(replacement)];
    }),
  );
}

function validateRequestPath(requestPath) {
  if (!requestPath.startsWith("/") || requestPath.includes("?")) {
    throw new Error("request-path must be a URL pathname");
  }
}

function hasAllowedHost(hostname, hostSuffix) {
  const normalizedSuffix = String(hostSuffix || "").replace(/^\.+/, "").toLowerCase();
  if (!normalizedSuffix) return true;
  const normalizedHost = hostname.toLowerCase();
  return normalizedHost === normalizedSuffix || normalizedHost.endsWith(`.${normalizedSuffix}`);
}

function matchesExpectedQuery(requestUrl, expectedQuery) {
  return Object.entries(expectedQuery).every(([key, expectedValue]) => (
    requestUrl.searchParams.has(key) && requestUrl.searchParams.get(key) === expectedValue
  ));
}

function isMatchingResponse(
  response,
  requestPath,
  requestMethod,
  hostSuffix,
  expectedQuery,
) {
  let requestUrl;
  try {
    requestUrl = new URL(response.url());
  } catch {
    return false;
  }
  return (
    (requestMethod === "*" || response.request().method().toUpperCase() === requestMethod) &&
    hasAllowedHost(requestUrl.hostname, hostSuffix) &&
    requestUrl.pathname === requestPath &&
    matchesExpectedQuery(requestUrl, expectedQuery)
  );
}

function getResponseField(payload, fieldPath) {
  if (!fieldPath) return payload;
  return fieldPath.split(".").reduce((value, key) => value?.[key], payload);
}

function parseResponsePayload(response, body, responseField) {
  const contentType = response.headers()["content-type"] || "";
  if (response.status() !== 200 || !contentType.toLowerCase().includes("json")) return null;
  try {
    const payload = JSON.parse(body);
    if (responseField && getResponseField(payload, responseField) === undefined) return null;
    return payload;
  } catch {
    return null;
  }
}

function parseCookieHeader(cookieHeader) {
  return String(cookieHeader || "")
    .split(";")
    .map((part) => part.trim())
    .filter((part) => part.includes("="))
    .map((part) => {
      const separator = part.indexOf("=");
      return {
        name: part.slice(0, separator).trim(),
        value: part.slice(separator + 1).trim(),
      };
    })
    .filter(({ name, value }) => /^[A-Za-z0-9_\-]+$/.test(name) && value.length > 0)
    .map(({ name, value }) => ({
      name,
      value,
      domain: ".douyin.com",
      path: "/",
      secure: true,
    }));
}

async function installQueryReplacementHook(page, requestPath, queryReplacements) {
  if (!Object.keys(queryReplacements).length) return;
  await page.addInitScript(
    ({ targetPath, replacements }) => {
      const xhrPrototype = XMLHttpRequest.prototype;
      const descriptor = Object.getOwnPropertyDescriptor(xhrPrototype, "open");
      const initialOpen = descriptor?.value || xhrPrototype.open;
      if (typeof initialOpen !== "function") return;

      const escapeRegex = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      const replaceQuery = (rawUrl) => {
        const hashIndex = rawUrl.indexOf("#");
        const hash = hashIndex >= 0 ? rawUrl.slice(hashIndex) : "";
        let baseUrl = hashIndex >= 0 ? rawUrl.slice(0, hashIndex) : rawUrl;

        for (const [key, replacement] of Object.entries(replacements)) {
          const encodedKey = encodeURIComponent(key);
          const encodedValue = encodeURIComponent(String(replacement));
          const pattern = new RegExp(
            `([?&]${escapeRegex(encodedKey)}=)[^&#]*`,
            "gi",
          );
          let replaced = false;
          baseUrl = baseUrl.replace(pattern, (match, prefix) => {
            replaced = true;
            return prefix + encodedValue;
          });

          if (!replaced) {
            const separator = baseUrl.includes("?")
              ? (/[?&]$/.test(baseUrl) ? "" : "&")
              : "?";
            baseUrl += separator + encodedKey + "=" + encodedValue;
          }
        }
        return baseUrl + hash;
      };

      const wrapOpen = (targetOpen) => {
        if (typeof targetOpen !== "function" || targetOpen.__dtQueryReplacementHook) {
          return targetOpen;
        }
        const hookedOpen = function(method, url, ...rest) {
          let nextUrl = url;
          try {
            const requestUrl = new URL(String(url), window.location.href);
            if (requestUrl.pathname === targetPath) {
              nextUrl = replaceQuery(String(url));
            }
          } catch {
            // Preserve non-standard URLs and let the page handle them.
          }
          return targetOpen.call(this, method, nextUrl, ...rest);
        };

        Object.defineProperty(hookedOpen, "__dtQueryReplacementHook", { value: true });
        return hookedOpen;
      };

      if (descriptor?.configurable) {
        let currentOpen = initialOpen;
        Object.defineProperty(xhrPrototype, "open", {
          configurable: true,
          enumerable: descriptor.enumerable,
          get() {
            return currentOpen;
          },
          set(value) {
            currentOpen = wrapOpen(value);
          },
        });
      } else {
        xhrPrototype.open = wrapOpen(initialOpen);
      }
    },
    { targetPath: requestPath, replacements: queryReplacements },
  );
}

async function loadChromium() {
  const configured = process.env.BROWSER_PATCHRIGHT_MODULE || process.env.DOUYIN_PATCHRIGHT_MODULE;
  const modulePath = configured
    ? path.resolve(configured)
    : path.join(
        PROJECT_ROOT,
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

async function launchContext(chromium) {
  const launchOptions = {
    channel: option("channel", "chrome"),
    headless: option(
      "headless",
      process.env.BROWSER_HEADLESS || process.env.DOUYIN_BROWSER_HEADLESS || "false",
    ) === "true",
    args: ["--test-type", "--hide-crash-restore-bubble"],
  };
  const contextOptions = {
    viewport: null,
    ignoreHTTPSErrors: true,
  };
  const browser = await chromium.launch(launchOptions);
  const context = await browser.newContext(contextOptions);
  return { context, browser, profileMode: "isolated" };
}

async function captureBrowserRequest() {
  const targetUrl = getTargetUrl();
  if (!targetUrl) throw new Error("browser request capture requires a page URL or numeric ID");

  const requestPath = option("request-path");
  validateRequestPath(requestPath);
  const requestMethod = option("request-method", "GET").toUpperCase();
  const hostSuffix = option("host-suffix", "douyin.com");
  const queryReplacements = normalizeQueryReplacements(
    parseJsonOption("replace-query", {}),
  );
  const responseField = option("response-field");

  const chromium = await loadChromium();
  const { context, browser, profileMode } = await launchContext(chromium);
  try {
    const cookieHeader = process.env.DOUYIN_COOKIE || "";
    if (cookieHeader) await context.addCookies(parseCookieHeader(cookieHeader));

    const page = await context.newPage();
    if (DEBUG) {
      page.on("request", (request) => {
        let requestUrl;
        try {
          requestUrl = new URL(request.url());
        } catch {
          return;
        }
        if (requestUrl.pathname !== requestPath) return;
        console.error(
          `[douyin-browser-debug] request method=${request.method()} ` +
            `path=${requestPath} query_keys=${[...requestUrl.searchParams.keys()].join(",")}`,
        );
      });
    }
    await installQueryReplacementHook(page, requestPath, queryReplacements);

    const responsePromise = new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        page.off("response", onResponse);
        reject(new Error(`timed out waiting for response: ${requestMethod} ${requestPath}`));
      }, Number(option("timeout-ms", "45000")));

      async function onResponse(response) {
        if (!isMatchingResponse(
          response,
          requestPath,
          requestMethod,
          hostSuffix,
          queryReplacements,
        )) return;
        try {
          const contentType = response.headers()["content-type"] || "";
          const body = await response.text();
          const payload = parseResponsePayload(response, body, responseField);
          if (DEBUG) {
            console.error(
              `[douyin-browser-debug] response status=${response.status()} ` +
                `path=${requestPath} content_type=${contentType} body_length=${body.length}`,
            );
          }
          if (payload === null) return;
          clearTimeout(timeout);
          page.off("response", onResponse);
          resolve({ response, payload, bodyLength: body.length });
        } catch {
          // Ignore transient risk-control or unreadable responses.
        }
      }

      page.on("response", onResponse);
    });

    await page.goto(
      targetUrl,
      { waitUntil: "domcontentloaded", timeout: Number(option("timeout-ms", "45000")) },
    ).catch((error) => {
      console.error(`page navigation did not finish: ${error.message}`);
    });
    const found = await responsePromise;
    const request = found.response.request();
    const requestUrl = new URL(request.url());
    const result = {
      ok: true,
      source: "browser",
      profileMode,
      requestPath,
      requestMethod,
      status: found.response.status(),
      contentType: found.response.headers()["content-type"] || "",
      bodyLength: found.bodyLength,
      signedUrl: request.url(),
      requestHeaders: request.headers(),
      signature: {
        aBogusLength: requestUrl.searchParams.get("a_bogus")?.length || 0,
        hasTimestamp: requestUrl.searchParams.has("timestamp"),
        hasSecSdkSignature: requestUrl.searchParams.has("x-secsdk-web-signature"),
      },
      payload: found.payload,
    };
    console.log(JSON.stringify(result));
  } finally {
    await context.close().catch(() => {});
    if (browser) await browser.close().catch(() => {});
  }
}

captureBrowserRequest().catch((error) => {
  console.error(error && error.stack ? error.stack : error);
  process.exitCode = 1;
});
