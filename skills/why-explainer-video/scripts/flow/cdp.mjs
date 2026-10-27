// Shared helpers: resolve playwright (from PLAYWRIGHT_DIR or next to this script), the persistent profile, the CDP endpoint, and attach().
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import os from 'node:os';

const here = path.dirname(fileURLToPath(import.meta.url));
const pwDir = process.env.PLAYWRIGHT_DIR || here;
let playwright;
try { playwright = createRequire(path.join(pwDir, 'package.json'))('playwright'); }
catch { try { playwright = createRequire(path.join(here, 'package.json'))('playwright'); }
  catch { console.error(`playwright not found. Run "npm i playwright" in a folder and set PLAYWRIGHT_DIR to it (tried ${pwDir}).`); process.exit(2); } }

export const { chromium } = playwright;
export const PROFILE = process.env.FLOW_PROFILE || path.join(os.homedir(), '.flow-profile');
export const CDP_PORT = Number(process.env.FLOW_PORT || 9222);
export const CDP = `http://127.0.0.1:${CDP_PORT}`;
export const FLOW_URL = 'https://labs.google/fx/tools/flow';
export const sleep = (ms) => new Promise(r => setTimeout(r, ms));
export const stamp = () => new Date().toTimeString().slice(0, 8);

/** Attach to the Chrome started by browser.mjs and return its Flow page (or the first page). */
export async function attach() {
  let browser;
  try { browser = await chromium.connectOverCDP(CDP, { timeout: 5000 }); }
  catch (e) { console.error(`No Chrome on ${CDP}. Start it first: node scripts/flow/browser.mjs (keep it running).`); process.exit(2); }
  const ctx = browser.contexts()[0] || await browser.newContext();
  const pages = ctx.pages();
  const page = pages.find(p => p.url().includes('labs.google')) || pages[0] || await ctx.newPage();
  return { browser, ctx, page };
}
