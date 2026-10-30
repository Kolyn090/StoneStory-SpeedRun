"""Synthetic CSV fixtures; no private save or game installation access."""
import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    'gear_references', Path(__file__).resolve().parents[1] / 'tools/validate_gear_references.py')
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)


class GearReferenceTests(unittest.TestCase):
    def test_owner_confirmed_shield_nickname_is_not_compound(self):
        self.assertEqual(V.family('FastGenShl'), 'towering shield')
        self.assertNotEqual(V.family('FastGenShl'), V.family('Compound Shield'))

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.gears = self.root / 'data/gears'
        self.gears.mkdir(parents=True)
        self.attr = dict.fromkeys(V.SCHEMAS['gear_attributes.csv'].split(','), '')
        self.attr.update(gear_id='screenshot_0001', name='Fire Shield', upgrade_display='+21/21',
                         armor_per_sec='0.7', armor='7', evade='30%',
                         source_image='cropped/page_001/item_0001.png',
                         review_status='visual_transcription_review_recommended')
        self.effect = dict(gear_id='screenshot_0001', effect_order='1', effect_text='Unknown conditional effect 109%',
                           source_image=self.attr['source_image'], review_status=self.attr['review_status'])
        self.tables = {key: [] for key in V.SCHEMAS}
        self.tables['gear_attributes.csv'] = [self.attr]
        self.tables['gear_effects.csv'] = [self.effect]

    def run_audit(self):
        for filename, rows in self.tables.items():
            with (self.gears / filename).open('w', encoding='utf-8-sig', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=V.SCHEMAS[filename].split(','))
                writer.writeheader()
                writer.writerows(rows)
        return V.audit(self.root)

    def test_preserves_unknown_text_and_blank_and_deterministic(self):
        result = self.run_audit()
        self.assertEqual([], result['errors'])
        self.assertEqual('', result['equipment'][0]['raw']['damage'])
        self.assertEqual(self.effect['effect_text'], result['equipment'][0]['effects'][0]['effect_text'])
        self.assertEqual(json.dumps(result, sort_keys=True), json.dumps(V.audit(self.root), sort_keys=True))

    def test_percent_is_explicit_and_blank_is_not_zero(self):
        self.assertEqual(V.number('0.3'), V.number('30%', percent=True))
        self.assertIsNone(V.number(''))
        self.assertNotEqual(V.number(''), V.number('0'))
        for bad in ('NaN', 'Infinity', '-1', '1x', '30%'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                V.number(bad)

    def test_duplicate_item_id_rejected(self):
        self.tables['gear_attributes.csv'].append(dict(self.attr))
        self.assertTrue(any('duplicate gear_id' in e for e in self.run_audit()['errors']))

    def test_duplicate_names_and_profiles_retained(self):
        second = dict(self.attr, gear_id='screenshot_0002', source_image='cropped/page_001/item_0002.png')
        self.tables['gear_attributes.csv'].append(second)
        self.tables['gear_effects.csv'].append(dict(self.effect, gear_id=second['gear_id'], source_image=second['source_image']))
        result = self.run_audit()
        self.assertEqual([], result['errors'])
        self.assertEqual(2, len(result['summary']['duplicate_names']['Fire Shield']))
        self.assertEqual(2, len(result['equipment']))

    def test_orphan_and_duplicate_effect_keys_rejected(self):
        self.tables['gear_effects.csv'].extend([dict(self.effect), dict(self.effect, gear_id='screenshot_0999')])
        errors = self.run_audit()['errors']
        self.assertTrue(any('duplicate effect key' in e for e in errors))
        self.assertTrue(any('orphan effect' in e for e in errors))

    def test_missing_effect_order_and_metadata_mismatch(self):
        self.effect.update(effect_order='2', source_image='cropped/other.png')
        errors = self.run_audit()['errors']
        self.assertTrue(any('noncontiguous' in e for e in errors))
        self.assertTrue(any('metadata mismatch' in e for e in errors))

    def test_bad_numbers_and_missing_fields(self):
        self.attr.update(name='', armor='not-a-number')
        self.assertTrue(self.run_audit()['errors'])

    def test_changed_schema_and_malformed_csv(self):
        self.run_audit()
        path = self.gears / 'gear_attributes.csv'
        path.write_text('gear_id,unexpected\n1,2\n', encoding='utf-8')
        self.assertTrue(any('schema changed' in e for e in V.audit(self.root)['errors']))
        path.write_text(V.SCHEMAS['gear_attributes.csv'] + '\n"unterminated', encoding='utf-8')
        self.assertTrue(V.audit(self.root)['errors'])

    def test_ragged_rows(self):
        self.run_audit()
        with (self.gears / 'gear_effects.csv').open('a', encoding='utf-8') as stream:
            stream.write('only_one_field\n')
        self.assertTrue(any('column count' in e for e in V.audit(self.root)['errors']))

    def test_unsafe_image_path(self):
        self.attr['source_image'] = '../outside.png'
        self.effect['source_image'] = self.attr['source_image']
        self.assertTrue(any('image reference' in e for e in self.run_audit()['errors']))

    def test_many_to_many_numeric_match_not_first_variant(self):
        attrs = [dict(self.attr, armor='7'), dict(self.attr, gear_id='screenshot_0002', armor='8')]
        rows = V.comparisons(attrs, [{'name': 'Fire Shield 1', 'armor': '8', 'evade': '0.3'}], {'armor': 'armor', 'evade': 'evade'})
        self.assertEqual(['screenshot_0002'], rows[0]['matching_ids'])
        self.assertEqual(2, len(rows[0]['candidates']))
        self.assertEqual('numeric_profile_match', rows[0]['status'])


if __name__ == '__main__':
    unittest.main()
