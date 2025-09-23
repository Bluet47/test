# tests/unit/test_validators_edge_cases_unittest.py
import unittest
from tools.validators import has_index, has_table, has_stats, has_ttp, has_testing_data

class TestValidatorsEdgeCases(unittest.TestCase):

    def test_has_stats_edges(self):
        cases = [
            ("index=main | stats count by user", True),
            ("index=main | tstats count where index=main by user", True),
            ("index=main | eventstats count", False),
            ("index=main | table _time user", False),
            ("index=main | fields keep _time user", False),
            ("index=main", False),
        ]
        for spl, expect in cases:
            with self.subTest(spl=spl):
                self.assertIs(has_stats(spl), expect)

    def test_has_testing_data_edges(self):
        cases = [
            ({"testing": {"dataset": "win_4720.json"}}, False),
            ({"testing": {"generator": "attack_range"}}, False),
            ({"testing": {}}, False),
            ({}, False),
            ({"metadata": {"testing_data": "inline"}}, False),
        ]
        for det, expect in cases:
            with self.subTest(det=det):
                self.assertIs(has_testing_data(det), expect)

