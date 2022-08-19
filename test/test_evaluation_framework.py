import unittest
import os
from bci.evaluations.samesite.samesite_evaluation import SameSiteEvaluationFramework


class TestEvaluationFramework(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        cls.data_path = os.path.join(curr_dir, "resources/csv_output")
        cls.evaluation_framework = SameSiteEvaluationFramework()

    def test_get_data_in_json(self):
        json_data = self.evaluation_framework.get_data_in_json(self.data_path, "pdf")
        assert json_data
        assert len(json_data.keys()) == 2
        assert "pdf-iframe-submitForm" in json_data
        assert json_data["pdf-iframe-submitForm"] == "false"
        assert "pdf-redirect-submitForm" in json_data
        assert json_data["pdf-redirect-submitForm"] == "true (2) [ ]"

    def test_is_dirty_evaluation(self):
        assert self.evaluation_framework.is_dirty_evaluation(self.data_path, "static")
        assert not self.evaluation_framework.is_dirty_evaluation(self.data_path, "pdf")
