from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from datetime import datetime, timezone
import hashlib
import json
import re

base = Path(__file__).resolve().parent
refs = {'master': 'ccf20caa0745cc2fe640f879d34acf2bf3855e6c', 'prod': '35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858', 'pre_amr': 'cc8dace141900b82e5790fa878e39d9c54898784'}

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.headings = []
        self.heading = None
        self.math_count = 0
        self.math_fallback_count = 0
        self.remote_scripts = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if re.fullmatch(r'h[1-6]', tag):
            self.heading = []
        if a.get('data-fez-math'):
            self.math_count += 1
            self.math_fallback_count += a['data-fez-math'] == 'fallback'
        if tag == 'script' and re.match(r'(?:https?:)?//', a.get('src', '')):
            self.remote_scripts.append(a['src'])
        for key in ('href', 'src'):
            if a.get(key):
                self.links.append(a[key])
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'a' and a.get('name'):
            self.ids.add(a['name'])
    def handle_data(self, data):
        if self.heading is not None:
            self.heading.append(data)
    def handle_endtag(self, tag):
        if re.fullmatch(r'h[1-6]', tag) and self.heading is not None:
            self.headings.append(' '.join(''.join(self.heading).split()))
            self.heading = None

def prepare_guide(source, label):
    text = re.sub(r'^(# .+?)(?:\r)?$', lambda m: m[1] + ' {#' + label + '}', source, count=1, flags=re.M)
    text = text.replace(r'\(', r'\f$').replace(r'\)', r'\f$').replace(r'\[', r'\f[').replace(r'\]', r'\f]')
    text = text.replace('(../patterns/distributed-state-transfer.md)', '(../../prod/html/fez_prod_distributed_state_transfer.html)')
    text = text.replace('(distributed-state-transfer.md)', '(../../prod/html/fez_prod_distributed_state_transfer.html)')
    text = re.sub(r'\[([^\]]+)\]\(\.\./\.\./pedagogie/([^\)]+)\)', r'<a href="../../../pedagogie/\2">\1</a>', text)
    return text + f'\n\n<span id="fez-guide-end-{label}"></span>\n'

manifest = {
    'generatedAt': datetime.now(timezone.utc).isoformat(),
    'generator': 'Doxygen 1.18.0 (8e760943e5d9581a444cf327f43a0b4d20d29482)',
    'archiveSha256': 'e84f54cfd49ef06b0b16536056dbec0c496323de28abcce53a4269463de35eaf',
    'archiveHashVerifiedBeforeExecution': True,
    'downloadUrl': 'https://github.com/doxygen/doxygen/releases/download/Release_1_18_0/doxygen-1.18.0.windows.x64.bin.zip',
    'hashSource': 'https://www.doxygen.nl/download.html',
    'scope': 'Snapshots partiels séparés, lecture GitHub. Aucun build FEZ ni test numérique.',
    'graphviz': False,
    'portablePageNames': True,
    'postprocessing': 'Guide copies receive stable labels, protected Doxygen math delimiters, explicit cross-document links and an end marker. render-math.mjs renders formulas as static KaTeX HTML/MathML with local CSS/fonts and removes MathJax scripts. fix-index-anchors.ps1 normalizes missing index anchors. Canonical knowledge Markdown and C++ snapshot contents are unchanged.',
    'mathRenderer': {'name': 'KaTeX', 'version': '0.18.7', 'offline': True, 'browserJavaScriptRequired': False},
    'branches': {},
}
all_errors = []
math_css = base.parent / 'assets/vendor/katex/dist/katex.min.css'
font_urls = re.findall(r'url\(([^)]+)\)', math_css.read_text(encoding='utf-8'))
font_urls = [url.strip('\"\'') for url in font_urls]
missing_math_assets = [url for url in font_urls if urlsplit(url).scheme or urlsplit(url).netloc or not (math_css.parent / url).is_file()]
manifest['mathRenderer']['fontAssetCount'] = len(set(font_urls))
manifest['mathRenderer']['missingOrRemoteAssets'] = missing_math_assets
all_errors.extend({'mathAssetError': url} for url in missing_math_assets)
for branch, sha in refs.items():
    root = base / branch / 'html'
    pages = {}
    for path in root.rglob('*.html'):
        parsed = Links()
        parsed.feed(path.read_text(encoding='utf-8'))
        pages[path.resolve()] = parsed
    missing_files, missing_anchors = [], []
    remote_scripts = []
    for path, parsed in pages.items():
        remote_scripts.extend({'page': path.name, 'src': src} for src in parsed.remote_scripts)
        for link in parsed.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not target.is_file():
                missing_files.append({'page': path.name, 'link': link})
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                missing_anchors.append({'page': path.name, 'link': link})
    snapshot = base / 'snapshots' / branch
    files = []
    for path in sorted(snapshot.rglob('*')):
        if path.is_file():
            relative = path.relative_to(snapshot).as_posix()
            files.append({'path': relative, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sourceUrl': f'https://github.com/arthurbawin/fez/blob/{sha}/{relative}', 'inApiInput': not relative.startswith('tests/')})
    warnings = (base / 'logs' / f'{branch}-warnings.log').read_text(encoding='utf-8')
    warning_count = warnings.count('warning:')
    guide_warnings = [line for line in warnings.splitlines() if 'warning:' in line and line.startswith('guides/')]
    generation_path = base / 'logs' / f'{branch}-generation.json'
    generation = json.loads(generation_path.read_text(encoding='utf-8')) if generation_path.is_file() else {}
    math_path = base / 'logs' / f'{branch}-math.json'
    math_report = json.loads(math_path.read_text(encoding='utf-8')) if math_path.is_file() else {}
    if not math_report or math_report.get('failures'):
        all_errors.append({'mathRenderReportError': branch, 'failures': math_report.get('failures')})
    if generation.get('doxygenExitCode') != 0 or generation.get('mathRenderExitCode') != 0:
        all_errors.append({'missingSuccessfulGenerationRecord': branch})
    guides = []
    for p in sorted((base / 'guides' / branch).rglob('*.md')):
        guide = {'path': str(p.relative_to(base)).replace('\\', '/'), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
        relative = p.relative_to(base / 'guides' / branch)
        knowledge_source = base.parent / 'knowledge' / relative
        if relative.name != 'index.md' and knowledge_source.is_file():
            source_text = knowledge_source.read_text(encoding='utf-8')
            guide_text = p.read_text(encoding='utf-8')
            label_match = re.search(r'^# .+? \{#(fez_[a-z_]+)\}$', guide_text, flags=re.M)
            label = label_match[1] if label_match else ''
            expected_text = prepare_guide(source_text, label)
            parsed_page = pages.get((root / (label + '.html')).resolve())
            headings = [' '.join(re.sub(r'[`*]', '', h).split()) for h in re.findall(r'^#{2,6} (.+)$', source_text, re.M)]
            missing_headings = [h for h in headings if not parsed_page or h not in parsed_page.headings]
            expected_math = len(re.findall(r'\\\(|\\\[', source_text))
            complete = parsed_page is not None and f'fez-guide-end-{label}' in parsed_page.ids and not missing_headings
            guide.update({'knowledgeSource': '../knowledge/' + relative.as_posix(), 'knowledgeSha256': hashlib.sha256(knowledge_source.read_bytes()).hexdigest(), 'matchesKnowledgeAfterDocumentedTransforms': guide_text == expected_text, 'renderedPage': label + '.html', 'complete': complete, 'missingHeadings': missing_headings, 'expectedFormulaCount': expected_math, 'renderedFormulaCount': parsed_page.math_count if parsed_page else 0})
            if guide_text != expected_text:
                all_errors.append({'outdatedGuide': relative.as_posix(), 'branch': branch})
            if not complete or parsed_page.math_count != expected_math or parsed_page.math_fallback_count:
                all_errors.append({'guideRenderingError': relative.as_posix(), 'branch': branch, 'missingHeadings': missing_headings, 'expectedMath': expected_math, 'actualMath': parsed_page.math_count if parsed_page else None})
        guides.append(guide)
    machine_path_filenames = [p.name for p in pages if re.search(r'(?:_c_1_2_users_|malol)', p.name, re.I)]
    manifest['branches'][branch] = {
        'gitBranch': 'master' if branch == 'master' else 'chns-ding-horriche-master-form',
        'commit': sha,
        'doxygenExitCode': generation.get('doxygenExitCode'),
        'generationRecord': generation,
        'entryPoint': f'{branch}/html/index.html',
        'snapshotFileCount': len(files),
        'apiSourceFileCount': sum(f['inApiInput'] for f in files),
        'htmlFileCount': len(pages),
        'xmlFileCount': len(list((base / branch / 'xml').glob('*.xml'))),
        'warningCount': warning_count,
        'guideWarningCount': len(guide_warnings),
        'warningSummary': 'Avertissements conservés dans le journal, issus des commentaires C++ et des limites des snapshots partiels. Les copies de guides sont contrôlées séparément ; leur compteur doit être nul.',
        'math': math_report,
        'remoteScripts': remote_scripts,
        'guides': guides,
        'machinePathFilenames': machine_path_filenames,
        'missingFileLinks': missing_files,
        'missingFragmentLinks': missing_anchors,
        'sources': files,
    }
    all_errors.extend(missing_files + missing_anchors)
    all_errors.extend(machine_path_filenames)
    all_errors.extend(remote_scripts + guide_warnings)
    print(json.dumps({'branch': branch, 'snapshotFiles': len(files), 'htmlFiles': len(pages), 'warningCount': warning_count, 'missingFiles': len(missing_files), 'missingAnchors': len(missing_anchors)}, ensure_ascii=False))
    if missing_files or missing_anchors:
        print(json.dumps((missing_files + missing_anchors)[:20], ensure_ascii=False))
(base / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
if all_errors:
    print(json.dumps({'errors': all_errors[:30]}, ensure_ascii=False, indent=2))
    raise SystemExit(1)
