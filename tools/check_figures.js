#!/usr/bin/env node
/**
 * Figure regression check.
 *
 * Extracts the inline figure script from every page, runs it twice against a
 * stubbed Plotly and DOM, and compares what it drew. Two things are asserted:
 *
 *   1. the script runs at all (catches IIFE/scoping mistakes from migration);
 *   2. it draws the SAME numbers both times.
 *
 * (2) is the point. Before Phase 1 these scripts pulled from an unseeded
 * Math.random() at 28 call sites, so every reload showed different data --
 * unacceptable in a reference work, and it silently invalidated any figure a
 * reader tried to check by hand.
 *
 * Usage:  node tools/check_figures.js
 * Exit 0 = all deterministic, 1 = something drifted or threw.
 */
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const vm = require("vm");

const ROOT = path.join(__dirname, "..");

/* Mirrors XAI.rng / XAI.randn in assets/book.js. */
function makeXAI() {
  const rng = (seed) => {
    let a = seed >>> 0;
    return () => {
      a = (a + 0x6d2b79f5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  };
  const randn = (rand) => {
    let u = 0, v = 0;
    while (u === 0) u = rand();
    while (v === 0) v = rand();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  };
  return { rng, randn, CFG: {}, AXIS: {} };
}

function extract(file) {
  const html = fs.readFileSync(file, "utf8");
  let found = null;
  const re = /<script>([\s\S]*?)<\/script>/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (m[1].includes("Plotly.newPlot") || m[1].includes("innerHTML")) found = m[1];
  }
  return found;
}

function run(src, file) {
  const drawn = [];
  const ctx = {
    XAI: makeXAI(),
    Plotly: { newPlot: (id, traces, layout) => drawn.push([id, traces, layout]) },
    document: {
      getElementById: (id) => ({
        set innerHTML(v) { drawn.push([id, v]); },
        style: {},
        appendChild() {},
      }),
    },
    console, Math, JSON, Array, Object, Number, String,
    isFinite, parseFloat, parseInt, Date,
  };
  ctx.window = ctx;
  vm.createContext(ctx);
  vm.runInContext(src, ctx, { filename: file, timeout: 15000 });
  return crypto.createHash("sha256").update(JSON.stringify(drawn)).digest("hex").slice(0, 16);
}

let bad = 0, checked = 0;
for (const name of fs.readdirSync(ROOT).filter((f) => f.endsWith(".html")).sort()) {
  const src = extract(path.join(ROOT, name));
  if (!src) continue;
  checked++;
  try {
    const a = run(src, name);
    const b = run(src, name);
    if (a === b) {
      console.log(`  ok             ${name.padEnd(32)} ${a}`);
    } else {
      bad++;
      console.log(`  NONDETERMINISTIC ${name.padEnd(32)} ${a} != ${b}`);
    }
  } catch (e) {
    bad++;
    console.log(`  RUNTIME ERROR  ${name.padEnd(32)} ${String(e.message).split("\n")[0]}`);
  }
}

console.log(
  bad
    ? `\n${bad} of ${checked} page(s) with problems`
    : `\n${checked} page(s): all figure scripts run clean and reproduce identically`
);
process.exit(bad ? 1 : 0);
