# test the fuctions from the detection validator script 
import unittest
from tools.validators import has_index, has_table, has_stats, has_ttp, has_testing_data

class TestValidatorsEdgeCases(unittest.TestCase):

    def test_has_index_edges(self):
        cases = [
            ("index=main | stats count by user", True),
            (" index =  main | table _time user", True),
            ("search index=win | stats count", True),
            ("sourcetype=wineventlog | stats count", False),
            ("", False),
            (None, False),
        ]
        for spl, expect in cases:
            with self.subTest(spl=spl):
                self.assertIs(has_index(spl), expect)

    def test_has_stats_edges(self):
        cases = [
            ("index=main | stats count by user", True),
            ("index=main | tstats count where index=main by user", True),
            ("index=main | eventstats count", True),
            ("index=main | table _time user", False),
            ("index=main | fields keep _time user", False),
            ("index=main", False),
        ]
        for spl, expect in cases:
            with self.subTest(spl=spl):
                self.assertIs(has_stats(spl), expect)

    def test_has_table_edges(self):
        cases = [
            ("index=main | table _time user", True),
            ("index=main | stats count by user", False),
            ("index=main | TABLE host", True),
        ]
        for spl, expect in cases:
            with self.subTest(spl=spl):
                self.assertIs(has_table(spl), expect)

    def test_has_ttp_edges(self):
        cases = [
            ({"tags": {"mitre_attack": ["T1136"]}}, True),
            ({"tags": {"mitre_attack": []}}, False),
            ({"tags": {}}, False),
            ({}, False),
            ({"tags": {"mitre_attack": ["t1136", "T1068"]}}, True),
        ]
        for det, expect in cases:
            with self.subTest(det=det):
                self.assertIs(has_ttp(det), expect)

    def test_has_testing_data_edges(self):
        cases = [
            ({"testing": {"dataset": "win_4720.json"}}, True),
            ({"testing": {"generator": "attack_range"}}, True),
            ({"testing": {}}, False),
            ({}, False),
            ({"metadata": {"testing_data": "inline"}}, False),
        ]
        for det, expect in cases:
            with self.subTest(det=det):
                self.assertIs(has_testing_data(det), expect)

if __name__ == "__main__":
    unittest.main()
