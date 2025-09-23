# tests/unit/test_validators_edge_cases_unittest.py
import unittest
from tools.validators import has_index, has_table, has_stats, has_ttp, has_testing_data

class TestValidatorsEdgeCases(unittest.TestCase):

    def test_has_stats_edges(self):
        cases = [
            ("index=main | stats count by user", True),
            ("index=main | tstats count where index=main by user", True),
            ("index=main | eventstats count", False),   # per your current policy
            ("index=main | table _time user", False),
            ("index=main | fields keep _time user", False),
            ("index=main", False),
        ]
        for i, (spl, expect) in enumerate(cases, start=1):
            with self.subTest(case=i, spl=spl):
                got = has_stats(spl)
                print(f"[has_stats][case {i}] expect={expect} got={got} spl={spl!r}")
                self.assertIs(got, expect)

    def test_has_testing_data_edges(self):
        cases = [
            ({"testing": {"dataset": "win_4720.json"}}, False),   # per your current policy
            ({"testing": {"generator": "attack_range"}}, False),  # per your current policy
            ({"testing": {}}, False),
            ({}, False),
            ({"metadata": {"testing_data": "inline"}}, False),
        ]
        for i, (det, expect) in enumerate(cases, start=1):
            with self.subTest(case=i, det=det):
                got = has_testing_data(det)
                print(f"[has_testing_data][case {i}] expect={expect} got={got} det={det}")
                self.assertIs(got, expect)

if __name__ == "__main__":
    unittest.main(verbosity=2)


