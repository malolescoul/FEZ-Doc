// Render Doxygen formula spans at generation time. No CDN or browser JS needed.
import {readFile, writeFile, readdir} from 'node:fs/promises';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';
import katex from '../assets/vendor/katex/dist/katex.mjs';

const base = dirname(fileURLToPath(import.meta.url));
const branch = process.argv[2];
if (!['master', 'prod', 'pre_amr'].includes(branch)) throw new Error('Invalid branch');
const root = join(base, branch, 'html');
const decode = value => value.replace(/&#(x[\da-f]+|\d+);/gi, (_, n) => String.fromCodePoint(n[0].toLowerCase() === 'x' ? parseInt(n.slice(1), 16) : +n)).replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&apos;|&#39;/g, "'").replace(/&amp;/g, '&');
const escape = value => value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const report = {branch, renderer: `KaTeX ${katex.version}`, offline: true, pages: [], failures: []};
for (const name of await readdir(root)) {
  if (!name.endsWith('.html')) continue;
  const path = join(root, name);
  const original = await readFile(path, 'utf8');
  let count = 0;
  let text = original.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, script => /mathjax/i.test(script) ? '' : script);
  // Doxygen 1.18 emits inline MathJax delimiters directly in text nodes,
  // without a formulaInl wrapper. Do not touch source listings or code blocks.
  if (!name.endsWith('_source.html')) {
    const stack = [];
    text = text.split(/(<[^>]+>)/g).map(part => {
      if (part.startsWith('<')) {
        const tag = /^<\s*(\/)?([a-z0-9]+)/i.exec(part);
        if (tag) {
          const key = tag[2].toLowerCase();
          if (tag[1]) {
            const index = stack.lastIndexOf(key);
            if (index >= 0) stack.length = index;
          } else if (!/^(?:area|base|br|col|embed|hr|img|input|link|meta|source|track|wbr)$/.test(key) && !part.endsWith('/>')) stack.push(key);
        }
        return part;
      }
      if (stack.some(tag => ['script', 'style', 'pre', 'code', 'math', 'textarea'].includes(tag))) return part;
      return part.replace(/\\\(([\s\S]*?)\\\)/g, (_, formula) => `<span class="formulaInl">\\(${formula}\\)</span>`);
    }).join('');
  }
  text = text.replace(/<(p|span)\b([^>]*\bclass="formula(?:Dsp|Inl)"[^>]*)>([\s\S]*?)<\/\1>/g, (_, tag, attrs, body) => {
    const displayMode = attrs.includes('formulaDsp');
    const raw = decode(body).trim();
    const formula = raw.replace(/^\\[\[(]/, '').replace(/\\[\])]$/, '').trim();
    count++;
    try {
      const rendered = katex.renderToString(formula, {displayMode, throwOnError: true, strict: 'ignore', trust: false, output: 'htmlAndMathml'});
      return `<${tag}${attrs} data-fez-math="katex">${rendered}</${tag}>`;
    } catch (error) {
      report.failures.push({page: name, formula, error: String(error)});
      return `<${tag}${attrs} data-fez-math="fallback"><code>${escape(formula)}</code></${tag}>`;
    }
  });
  // USE_MATHJAX makes Doxygen preserve TeX; the static renderer replaces it.
  if (count) {
    text = text.replace('</head>', '<link rel="stylesheet" href="../../../assets/vendor/katex/dist/katex.min.css">\n<style>.formulaDsp{overflow-x:auto;padding:.4em 0}.formulaInl{white-space:normal}.katex{font-size:1.05em}</style>\n</head>');
    report.pages.push({page: name, formulaCount: count});
  }
  if (text !== original) await writeFile(path, text, 'utf8');
}
report.formulaCount = report.pages.reduce((sum, page) => sum + page.formulaCount, 0);
await writeFile(join(base, 'logs', `${branch}-math.json`), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({branch, formulas: report.formulaCount, failures: report.failures.length}));
if (report.failures.some(failure => failure.page.startsWith('fez_'))) process.exitCode = 1;
