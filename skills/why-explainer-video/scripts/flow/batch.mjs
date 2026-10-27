// Pastes every prompt of prompts.json into Google Flow (direct image mode), waits for the result tile, downloads it. Resumable.
//   PACE=12000 node scripts/flow/batch.mjs prompts.json flow/<video>
// prompts.json = [{"file": "F001", "prompt": "..."}, ...]. A file already present in the output folder is skipped.
// Env: PACE (ms pause after each image, 12000 keeps under Flow's rate limit), WAIT (ms max per image, 150000),
//      QUEUE (ms to see the prompt appear in a result tile, 20000). Output: <out>/<file>.jpg (or .png/.webp as served).
// Flow UI (flow.google.com, October 2026): prompt bar at the bottom with the textbox "Que voulez-vous créer ?", the "Agent"
// toggle OFF (direct mode), the settings trigger set to Image · 16:9 · x1, and the button "Lancer la génération". Each result is a
// `group` in <main> whose text carries the full prompt and whose <img> is the 1376×768 picture. Only a tile that contains THIS
// prompt and whose image URL was not on the page before the click is accepted (older thumbnails of the project load late).
import fs from 'node:fs';
import path from 'node:path';
import { attach, sleep, stamp } from './cdp.mjs';

const [src = 'prompts.json', out = 'flow/out'] = process.argv.slice(2);
const PACE = Number(process.env.PACE || 12000), WAIT = Number(process.env.WAIT || 150_000), QUEUE = Number(process.env.QUEUE || 20_000);
const prompts = JSON.parse(fs.readFileSync(src, 'utf8'));
fs.mkdirSync(out, { recursive: true });
const done = new Set(fs.readdirSync(out).filter(f => !/\.test\./.test(f)).map(f => f.replace(/\.(jpg|jpeg|png|webp)$/i, '')));
const todo = prompts.filter(p => !done.has(p.file));
console.log(`${stamp()} ${prompts.length} prompts, ${todo.length} to generate, pace ${PACE} ms`);

const { page } = await attach(); page.setDefaultTimeout(15_000);
const box = () => page.getByRole('textbox', { name: /Que voulez-vous créer|What do you want to create/i }).first();
const genButton = () => page.getByRole('button', { name: /Lancer la génération|^Generate$|Générer/i }).first();
const failed = () => page.getByText(/Échec|Failed|activité inhabituelle|unusual activity/i).first();
const bigImages = () => page.evaluate(() => [...document.querySelectorAll('main img')].filter(i => i.naturalWidth >= 512).map(i => i.src));

async function ensureDirectMode() {
  const agent = page.getByRole('button', { name: /^Agent$/ }).first();
  if (await agent.isVisible().catch(() => false) && (await agent.getAttribute('aria-pressed')) === 'true') { await agent.click(); await sleep(800); console.log(`${stamp()} Agent mode switched off (direct mode)`); }
  const trig = page.getByRole('button', { name: /Déclencheur des paramètres|Settings trigger/i }).first();
  const label = (await trig.innerText().catch(() => '')).replace(/\s+/g, ' ');
  if (!/x1/.test(label)) { await trig.click(); await sleep(800); await page.getByRole('radio', { name: /^Image$/ }).first().click({ force: true }).catch(() => {}); await page.getByRole('radio', { name: /^16:9$/ }).first().click({ force: true }).catch(() => {}); await page.getByRole('radio', { name: /^x1$/ }).first().click({ force: true }).catch(() => {}); await page.keyboard.press('Escape'); await sleep(500); console.log(`${stamp()} settings set to Image · 16:9 · x1 (was "${label}")`); }
}
async function tileFor(key) {  // the result group that carries this prompt
  return page.locator('main [role="group"]').filter({ hasText: key }).first();
}
async function download(srcUrl, file) {
  const { b64, type } = await page.evaluate(async (u) => {
    const r = await fetch(u); const buf = await r.arrayBuffer(); const bytes = new Uint8Array(buf); let s = '';
    for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    return { b64: btoa(s), type: r.headers.get('content-type') || '' };
  }, srcUrl);
  const ext = /png/.test(type) ? 'png' : /webp/.test(type) ? 'webp' : 'jpg';
  const dst = path.join(out, `${file}.${ext}`); fs.writeFileSync(dst, Buffer.from(b64, 'base64')); return dst;
}

await ensureDirectMode();
let ok = 0, skipped = 0;
for (const [k, p] of todo.entries()) {
  const key = p.prompt.slice(0, 60);
  try {
    const before = new Set(await bigImages());
    const b = box(); await b.click(); await b.fill(p.prompt); await sleep(300);
    const g = genButton();
    if (await g.isDisabled().catch(() => true)) { console.log(`${stamp()} ${p.file} SKIP: generate button disabled (no credits or empty prompt)`); skipped++; await sleep(PACE); continue; }
    await g.click();
    const q0 = Date.now(); let tile = null;
    while (Date.now() - q0 < QUEUE) { const t = await tileFor(key); if (await t.count()) { tile = t; break; } await sleep(1000); }
    if (!tile) { console.log(`${stamp()} ${p.file} NOT QUEUED (no result tile carries the prompt)`); skipped++; await sleep(PACE); continue; }
    const w0 = Date.now(); let got = false;
    while (Date.now() - w0 < WAIT) {
      if (await failed().isVisible().catch(() => false)) { console.log(`${stamp()} ${p.file} FAILED card shown: pausing 2 min`); await sleep(120_000); break; }
      const srcUrl = await tile.locator('img').first().evaluate(i => i.naturalWidth >= 512 ? i.src : '').catch(() => '');
      if (srcUrl && !before.has(srcUrl)) {
        await sleep(1500); const dst = await download(srcUrl, p.file); ok++; got = true;
        console.log(`${stamp()} ${p.file} ok -> ${dst} (${k + 1}/${todo.length}, ${Math.round((Date.now() - q0) / 1000)} s)`); break;
      }
      await sleep(2000);
    }
    if (!got) { console.log(`${stamp()} ${p.file} TIMEOUT after ${WAIT / 1000} s`); skipped++; }
  } catch (e) { console.log(`${stamp()} ${p.file} ERROR ${e.message.split('\n')[0]}`); skipped++; }
  await sleep(PACE);
}
console.log(`${stamp()} done: ${ok} downloaded, ${skipped} skipped or failed. Run the same command again to retry the missing ones.`);
process.exit(0);
