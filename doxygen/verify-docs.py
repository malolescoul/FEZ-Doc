from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from datetime import datetime, timezone
import hashlib
import json
import re

base = Path(__file__).resolve().parent
refs = {'master': 'ccf20caa0745cc2fe640f879d34acf2bf3855e6c', 'prod': '35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858'}

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ('href', 'src'):
            if a.get(key):
                self.links.append(a[key])
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'a' and a.get('name'):
            self.ids.add(a['name'])

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
    'postprocessing': 'fix-index-anchors.ps1 normalizes only the missing alphabet and destructor index anchors emitted by Doxygen 1.18.0. API text and source snapshots are unchanged.',
    'branches': {},
}
all_errors = []
for branch, sha in refs.items():
    root = base / branch / 'html'
    pages = {}
    for path in root.rglob('*.html'):
        parsed = Links()
        parsed.feed(path.read_text(encoding='utf-8'))
        pages[path.resolve()] = parsed
    missing_files, missing_anchors = [], []
    for path, parsed in pages.items():
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
    guides = []
    for p in sorted((base / 'guides' / branch).rglob('*.md')):
        guide = {'path': str(p.relative_to(base)).replace('\\', '/'), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
        relative = p.relative_to(base / 'guides' / branch)
        knowledge_source = base.parent / 'knowledge' / relative
        if relative.name != 'index.md' and knowledge_source.is_file():
            source_text = knowledge_source.read_text(encoding='utf-8')
            guide_text = re.sub(r'^(# .+?) \{#fez_[a-z_]+\}$', r'\1', p.read_text(encoding='utf-8'), count=1, flags=re.M)
            guide.update({'knowledgeSource': '../knowledge/' + relative.as_posix(), 'knowledgeSha256': hashlib.sha256(knowledge_source.read_bytes()).hexdigest(), 'matchesKnowledgeExceptPageLabel': guide_text == source_text})
            if guide_text != source_text:
                all_errors.append({'outdatedGuide': relative.as_posix(), 'branch': branch})
        guides.append(guide)
    machine_path_filenames = [p.name for p in pages if re.search(r'(?:_c_1_2_users_|malol)', p.name, re.I)]
    manifest['branches'][branch] = {
        'gitBranch': 'master' if branch == 'master' else 'chns-ding-horriche-master-form',
        'commit': sha,
        'doxygenExitCode': 0,
        'entryPoint': f'{branch}/html/index.html',
        'snapshotFileCount': len(files),
        'apiSourceFileCount': sum(f['inApiInput'] for f in files),
        'htmlFileCount': len(pages),
        'xmlFileCount': len(list((base / branch / 'xml').glob('*.xml'))),
        'warningCount': warning_count,
        'warningSummary': 'Commandes LaTeX non encadrées par les délimiteurs Doxygen dans des commentaires source existants. Les snapshots originaux sont conservés sans correction.',
        'guides': guides,
        'machinePathFilenames': machine_path_filenames,
        'missingFileLinks': missing_files,
        'missingFragmentLinks': missing_anchors,
        'sources': files,
    }
    all_errors.extend(missing_files + missing_anchors)
    all_errors.extend(machine_path_filenames)
    print(json.dumps({'branch': branch, 'snapshotFiles': len(files), 'htmlFiles': len(pages), 'warningCount': warning_count, 'missingFiles': len(missing_files), 'missingAnchors': len(missing_anchors)}, ensure_ascii=False))
    if missing_files or missing_anchors:
        print(json.dumps((missing_files + missing_anchors)[:20], ensure_ascii=False))
(base / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
if all_errors:
    raise SystemExit(1)
