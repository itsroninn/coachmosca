import { mkdir, rm, copyFile, readFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const outputDir = join(root, "public");
const sourceIndex = join(root, "index.html");
const outputIndex = join(outputDir, "index.html");

const requiredAssets = [
  "IMAGENS/AOM STANDARDjpg.jpg",
  "IMAGENS/discord-white-icon.png",
  "IMAGENS/LOGO MOSCA.jpg",
  "IMAGENS/luquipedia logo 2017.png",
  "IMAGENS/simbolo-do-youtube-white.png",
  "IMAGENS/twitch-white-icon.png",
];

await rm(outputDir, { recursive: true, force: true });
await mkdir(outputDir, { recursive: true });

const indexHtml = await readFile(sourceIndex, "utf8");

if (!indexHtml.includes('name="lead-mosca"') || !indexHtml.includes("data-netlify")) {
  throw new Error("Netlify Forms marker for lead-mosca was not found in index.html.");
}

await copyFile(sourceIndex, outputIndex);

for (const asset of requiredAssets) {
  const source = join(root, asset);
  const target = join(outputDir, asset);
  await mkdir(dirname(target), { recursive: true });
  await copyFile(source, target);
}

console.log(`Prepared Netlify publish directory with ${requiredAssets.length + 1} files.`);
