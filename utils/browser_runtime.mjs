import path from "node:path";
import { pathToFileURL } from "node:url";

export function option(name, fallback = "") {
  const prefix = `--${name}=`;
  const value = process.argv.find((arg) => arg.startsWith(prefix));
  return value ? value.slice(prefix.length) : fallback;
}

export function positionalArgs() {
  return process.argv.slice(2).filter((arg) => !arg.startsWith("--"));
}

export function timeoutMs(fallback = "75000") {
  return Number(option("timeout-ms", fallback));
}

export async function loadChromium() {
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

export async function launchBrowser() {
  const chromium = await loadChromium();
  const headless = option("headless", process.env.BROWSER_HEADLESS || "false") === "true";
  const launchOptions = {
    channel: option("channel", "chrome"),
    headless,
    args: ["--test-type", "--hide-crash-restore-bubble"],
  };
  const contextOptions = { viewport: null, ignoreHTTPSErrors: true };
  const browser = await chromium.launch(launchOptions);
  const context = await browser.newContext(contextOptions);
  return { browser, context };
}

export async function openPage(context) {
  return context.pages()[0] || context.newPage();
}

export async function closeBrowser({ browser, context } = {}) {
  await context?.close().catch(() => {});
  await browser?.close().catch(() => {});
}
