import unittest
import os
from bci.browser_build.firefox_build import FirefoxRepo


class TestFirefoxBuild(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.repo_path = "resources/repositories/mercurial"
        cls.repo = FirefoxRepo(cls.repo_path)
        assert os.path.isdir(cls.repo_path)

    @classmethod
    def tearDownClass(cls):
        cls.repo_path = None
        cls.repo = None
