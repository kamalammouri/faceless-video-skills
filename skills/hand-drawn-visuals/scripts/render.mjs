// Renders hand-drawn inserts (symbols, number cards, scoreboards, phone screens, charts, timelines, titles) from JSON specs
// to 1920x1080 PNG, through a real browser: HTML + CSS + rough.js (sketchy shapes) + chart.xkcd (sketchy charts) + Lucide icons.
//   node render.mjs specs.json out/            -> out/<file>.png for every spec (existing files skipped; --force redraws)
//   node render.mjs shots.json out/ --shots    -> only the shots that carry an "html" key; file = H<i padded to 4>
//   node render.mjs --demo out/                -> one PNG per template type, then a contact sheet is up to sheets.py
// Env: PLAYWRIGHT_DIR (folder that has node_modules/playwright), BG / BG_DARK (background images painted under every insert,
//      e.g. the empty pages generated once in Flow), FONT (CSS font-family override).
// Spec: {"file": "H0012", "type": "symbol", "icon": "check", "caption": "verified", "dark": false}  (all types: references/spec-format.md)
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { dirname, join, resolve } from 'node:path';

const HERE = dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const args = process.argv.slice(2);
const flag = f => args.includes(f);
const pos = args.filter(a => !a.startsWith('--'));
const outDir = pos[flag('--demo') ? 0 : 1] || 'html';
mkdirSync(outDir, { recursive: true });

async function pw() {
  const dir = process.env.PLAYWRIGHT_DIR;
  return dir ? import(pathToFileURL(join(dir, 'node_modules/playwright/index.mjs')).href) : import('playwright');
}

let specs;
if (flag('--demo')) specs = JSON.parse(readFileSync(join(HERE, 'demo.json'), 'utf8'));
else {
  const src = JSON.parse(readFileSync(pos[0], 'utf8'));
  specs = flag('--shots')
    ? src.filter(s => s.html).map(s => ({ file: `H${String(s.i).padStart(4, '0')}`, dark: !!s.dark, ...s.html }))
    : src;
}
const todo = specs.filter(s => flag('--force') || !existsSync(join(outDir, `${s.file}.png`)));
console.log(`${specs.length} specs, ${todo.length} to render -> ${outDir}`);
if (!todo.length) process.exit(0);

// Lucide icons: fetched once from unpkg, cached in vendor/icons/<name>.svg (ISC licence, 1,600+ names at lucide.dev/icons)
const iconDir = join(HERE, 'vendor', 'icons'); mkdirSync(iconDir, { recursive: true });
async function icon(name) {
  if (!name) return '';
  const f = join(iconDir, `${name}.svg`);
  if (existsSync(f)) return readFileSync(f, 'utf8');
  const r = await fetch(`https://unpkg.com/lucide-static@0.468.0/icons/${name}.svg`);
  if (!r.ok) { console.log(`  icon "${name}" not found on lucide (check the name at lucide.dev/icons)`); return ''; }
  const svg = await r.text(); writeFileSync(f, svg); return svg;
}
for (const s of todo) {
  for (const k of ['icon', 'icon2', 'icon_left', 'icon_right']) if (s[k]) s[`${k}_svg`] = await icon(s[k]);
  if (Array.isArray(s.items)) for (const it of s.items) if (it.icon) it.icon_svg = await icon(it.icon);
}

const { chromium } = await pw();
const browser = await chromium.launch({ channel: process.env.BROWSER_CHANNEL || 'chrome', headless: true }).catch(() => chromium.launch({ headless: true }));
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const bgUrl = p => (p && existsSync(p) ? pathToFileURL(resolve(p)).href : '');
const env = { bg: bgUrl(process.env.BG), bgDark: bgUrl(process.env.BG_DARK), font: process.env.FONT || '' };
await page.goto(pathToFileURL(join(HERE, 'template.html')).href, { waitUntil: 'load' });
await page.waitForFunction(() => document.fonts.status === 'loaded' && window.render, null, { timeout: 30000 }).catch(() => console.log('  fonts or template not ready, rendering anyway'));
let ok = 0;
for (const s of todo) {
  try {
    await page.evaluate(([spec, e]) => window.render(spec, e), [s, env]);
    await page.waitForTimeout(80);
    await page.screenshot({ path: join(outDir, `${s.file}.png`), type: 'png' });
    ok++; console.log(`  ${s.file} ${s.type}`);
  } catch (e) { console.log(`  ${s.file} ERROR ${e.message.split('\n')[0]}`); }
}
await browser.close();
console.log(`done: ${ok}/${todo.length} rendered`);
