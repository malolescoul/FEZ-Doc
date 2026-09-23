"""Cross-check the documentary ledger against its Git parent structure."""
from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
H=json.loads((ROOT/'data/history-ledger.json').read_text(encoding='utf-8'))
D=json.loads((ROOT/'data/atlas.json').read_text(encoding='utf-8'))
class HistoryEvidence(unittest.TestCase):
    def test_snapshot_is_direct_parent_of_new_amr(self):
        self.assertEqual(H['baseline']['nextCommitMetadata']['parents'],[H['baseline']['sha']])
        self.assertEqual(H['entries'][-1]['sha'],H['baseline']['sha'])
        self.assertEqual(H['entries'][0]['parents'],[H['origin']['sha']])
        snapshot=next(b for b in D['branches'] if b['name']=='pre-amr')
        self.assertEqual(snapshot['sha'],H['baseline']['sha'])
        self.assertEqual(snapshot['kind'],'historical-snapshot')
    def test_ledger_preserves_all_commits_without_double_counting_master(self):
        self.assertEqual(len(H['entries']),61)
        self.assertEqual(len(H['masterImports']),13)
        own={e['sha'] for e in H['entries']}
        upstream={e['sha'] for e in H['masterImports']}
        self.assertEqual(len(own),61)
        self.assertEqual(len(upstream),13)
        self.assertFalse(own & upstream)
        self.assertEqual(sum(len(e['parents'])>1 for e in H['entries']),5)
    def test_order_respects_parents_and_proofs_name_existing_changed_files(self):
        all_known={e['sha'] for e in H['entries']+H['masterImports']}|{H['origin']['sha']}
        for entries in [H['entries'],H['masterImports']]:
            positions={e['sha']:i for i,e in enumerate(entries)}
            for i,e in enumerate(entries):
                self.assertEqual(e['index'],i+1)
                self.assertTrue(e['summary'])
                self.assertTrue(e['evidence']['method'])
                for p in e['parents']:
                    self.assertIn(p,all_known)
                    if p in positions:self.assertLess(positions[p],i)
                paths={f['path'] for f in e['files']}
                for p in e['evidence']['reviewedPaths']:self.assertIn(p,paths)
                for proof in e['evidence']['proofs']:
                    self.assertIn(proof['path'],paths)
                    self.assertNotEqual(proof['patchStatus'],'absent_content')
    def test_browser_uses_the_same_canonical_ledger(self):
        self.assertEqual(D['history'],H)
        self.assertEqual(json.loads((ROOT/'assets/data.js').read_text(encoding='utf-8').removeprefix('window.FEZ_DATA = ').strip().removesuffix(';')),D)
    def test_math_is_rendered_in_physics_pages(self):
        for suffix in ['features/chns-models-pre-amr.md','patterns/mobility-corrections-timestep.md']:
            doc=next(d for d in D['documents'] if d['path'].endswith(suffix))
            self.assertIn('<math',doc['html'])
            self.assertNotIn('katex-error',doc['html'])
if __name__=='__main__':unittest.main(verbosity=2)
