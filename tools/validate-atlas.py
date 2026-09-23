import json, re, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data/atlas.json').read_text(encoding='utf-8'))
class AtlasEvidence(unittest.TestCase):
    def test_node_details_are_paragraphs_not_a_character_stream(self):
        for graph in DATA['graphs']:
            for node in graph['nodes']:
                self.assertIsInstance(node.get('details',[]),list,node['id'])
                self.assertTrue(all(isinstance(p,str) for p in node.get('details',[])))
    def test_all_relations_have_endpoints_and_known_types(self):
        for graph in DATA['graphs']:
            ids=[n['id'] for n in graph['nodes']]
            self.assertEqual(len(ids),len(set(ids)))
            for edge in graph['edges']:
                self.assertIn(edge['from'],ids)
                self.assertIn(edge['to'],ids)
                self.assertIn(edge['kind'],['call','data','uses','inheritance','flow'])
                self.assertIn(edge['status'],['confirmed','inference'])
    def test_every_source_is_pinned_to_its_branch_and_has_valid_lines(self):
        for graph in DATA['graphs']:
            branch=next(b for b in DATA['branches'] if b['name']==graph['branch'])
            for item in graph['nodes']+graph['edges']:
                self.assertIn('/blob/'+branch['sha']+'/',item['sourceUrl'])
                self.assertIn(item['path']+'#L'+str(item['start']),item['sourceUrl'])
                lines=(ROOT/'doxygen/snapshots'/branch['key']/item['path']).read_text(encoding='utf-8').splitlines()
                self.assertGreaterEqual(item['start'],1)
                self.assertLessEqual(item['end'],len(lines)+1)
                self.assertLessEqual(item['start'],item['end'])
                self.assertTrue(item['snippet'])
    def test_drill_graphs_exist_and_do_not_cross_branches(self):
        for graph in DATA['graphs']:
            for node in graph['nodes']:
                for graph_id in node.get('expandGraphs',[]):
                    target=next(g for g in DATA['graphs'] if g['id']==graph_id)
                    self.assertEqual(target['branch'],graph['branch'])
                if 'drillGraph' in node:
                    target=next(g for g in DATA['graphs'] if g['id']==node['drillGraph'])
                    self.assertEqual(target['branch'],graph['branch'])
    def test_local_document_targets_exist(self):
        for doc in DATA['documents']:
            for href in re.findall(r'href="([^"]+)"',doc['html']):
                if href.startswith(('https:','http:','mailto:','#')): continue
                self.assertTrue((ROOT/href.split('#')[0]).exists(),(doc['path'],href))
    def test_quizzes_have_real_sources_and_valid_answers(self):
        self.assertEqual(len(DATA['quizzes']),4)
        for q in DATA['quizzes']:
            self.assertIn(q['answer'],range(len(q['options'])))
            self.assertIn(DATA['branches'][0]['sha'],q['sourceUrl'])
    def test_doxygen_outputs_are_real_and_separate(self):
        for b in DATA['branches']:
            content=(ROOT/'doxygen'/b['key']/'html/index.html').read_text(encoding='utf-8')
            self.assertIn('Doxygen',content)
            self.assertIn(b['sha'][:8],content)
if __name__=='__main__': unittest.main(verbosity=2)
