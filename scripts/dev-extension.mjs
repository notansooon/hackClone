import esbuild from 'esbuild';
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const outdir = resolve('extension', 'dist');
mkdirSync(outdir, { recursive: true });

const ctx = await esbuild.context({
  bundle: true,
  sourcemap: true,
  target: 'es2022',
  format: 'iife',
  outdir,
  logLevel: 'info',
  entryPoints: [
    'extension/src/background.ts',
    'extension/src/content/content-script.ts',
    'extension/src/options/options.ts',
  ],
});

await ctx.watch();
console.log('Watching for changes…');

