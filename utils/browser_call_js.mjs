import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

function option(name, fallback = "") {
  const prefix = `--${name}=`;
  const value = process.argv.find((arg) => arg.startsWith(prefix));
  return value ? value.slice(prefix.length) : fallback;
}

function positionalArgs() {
  return process.argv.slice(2).filter((arg) => !arg.startsWith("--"));
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
  const [targetUrl, scriptPath] = positionalArgs();
  if (!/^https?:\/\//i.test(targetUrl || "")) {
    throw new Error("browser_call_js requires an http(s) URL");
  }
  if (!scriptPath) throw new Error("browser_call_js requires a page script path");

  const source = await fs.readFile(path.resolve(scriptPath), "utf8");
  const args = JSON.parse(option("args-json", "[]"));
  if (!Array.isArray(args)) throw new Error("browser_call_js args must be a JSON array");

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
    await page.goto(targetUrl, { waitUntil: "domcontentloaded", timeout });
    const result = await page.evaluate(
      ({ source: pageSource, args: pageArgs }) => {
        const pageFunction = (0, eval)(`(${pageSource}\n)`);
        if (typeof pageFunction !== "function") {
          throw new Error("page script must evaluate to a function");
        }
        return pageFunction(...pageArgs);
      },
      { source, args },
    );

    console.log(JSON.stringify({ ok: true, result: result === undefined ? null : result }));
  } finally {
    if (context) await context.close().catch(() => {});
    if (browser) await browser.close().catch(() => {});
  }
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : error);
  process.exitCode = 1;
});
