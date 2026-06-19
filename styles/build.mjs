import { execSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const stylesDir = dirname(fileURLToPath(import.meta.url));
const outDir = join(stylesDir, "../src/marimo_utils/ui/static");
const outFile = join(outDir, "dr.css");

mkdirSync(outDir, { recursive: true });

const tailwindOut = execSync(
  "npx tailwindcss -i ./input.css -c ./tailwind.config.js --minify",
  { cwd: stylesDir, encoding: "utf8" },
);

const shadcn = readFileSync(join(stylesDir, "shadcn.css"), "utf8");
writeFileSync(outFile, `${tailwindOut}\n${shadcn}`);
console.log(`Wrote ${outFile}`);
