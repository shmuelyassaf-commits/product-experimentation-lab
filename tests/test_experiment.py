import unittest

from src.demo_data import make_demo_data
from src.experiment import analyze, data_quality_report, validate_schema


class ExperimentTests(unittest.TestCase):
    def setUp(self):
        self.data = make_demo_data(users=1000)

    def test_demo_has_required_schema(self):
        validate_schema(self.data)

    def test_quality_report_has_no_duplicate_users(self):
        self.assertEqual(data_quality_report(self.data)["duplicate_user_ids"], 0)

    def test_analysis_returns_decision(self):
        results = analyze(self.data)
        self.assertIn(results["decision"]["recommendation"], {"ROLL OUT", "DO NOT ROLL OUT", "RUN FOLLOW-UP TEST"})


if __name__ == "__main__":
    unittest.main()

