import fs from "node:fs/promises";
import path from "node:path";

import {
  closeBrowser,
  launchBrowser,
  openPage,
  option,
  positionalArgs,
  timeoutMs,
} from "./browser_runtime.mjs";

async function main() {
  const [targetUrl, scriptPath] = positionalArgs();
  if (!/^https?:\/\//i.test(targetUrl || "")) {
    throw new Error("browser_call_js requires an http(s) URL");
  }
  if (!scriptPath) throw new Error("browser_call_js requires a page script path");

  const source = await fs.readFile(path.resolve(scriptPath), "utf8");
  const args = JSON.parse(option("args-json", "[]"));
  if (!Array.isArray(args)) throw new Error("browser_call_js args must be a JSON array");

  let context;
  let browser;

  try {
    ({ browser, context } = await launchBrowser());
    const page = await openPage(context);
    await page.goto(targetUrl, { waitUntil: "domcontentloaded", timeout: timeoutMs() });
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
    await closeBrowser({ browser, context });
  }
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : error);
  process.exitCode = 1;
});
