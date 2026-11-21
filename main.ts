// Entry program for make.fun news-image-20261121 (Node 22, stdlib only).
//
// The picture itself is entry.png beside this file: a one-page newspaper
// front page drawn at build time by generate.py (Pillow + DejaVu fonts,
// every scene drawn from shapes -- no photos, no copied art). This program
// only copies it to the output directory, so both grading runs produce
// byte-identical output.
//
// Run locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
