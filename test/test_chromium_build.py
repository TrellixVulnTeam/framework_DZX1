import unittest
import os
import shutil
from bci.browser_build.chromium_build import ChromiumBuild


class TestChromiumBuild(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        cls.repo_path = os.path.join(curr_dir, "resources/repositories/git")
        cls.bin_folder_path = os.path.join(curr_dir, "resources/bin_folder")
        cls.artisanal_bin_folder_path = os.path.join(cls.bin_folder_path, "artisanal")
        cls.data_folder_path = os.path.join(curr_dir, "resources/data_folder")
        cls.driver_folder_path = os.path.join(curr_dir, "resources/driver_folder")
        # Tests are run by GitHub automation, which I don't want to give access to the MongoDB database
        # MongoDB.connect()
        assert os.path.isdir(cls.repo_path)

    @classmethod
    def tearDownClass(cls):
        cls.repo_path = None
        cls.bin_folder_path = None
        cls.data_folder_path = None
        cls.build = None
        # MongoDB.disconnect()

    def setUp(self):
        if os.path.isdir(self.bin_folder_path):
            shutil.rmtree(self.bin_folder_path)
        os.makedirs(self.bin_folder_path)
        os.makedirs(self.artisanal_bin_folder_path)
        meta_file_path = os.path.join(self.artisanal_bin_folder_path, "meta.json")
        with open(meta_file_path, "w") as file:
            file.write("[]")
        if os.path.isdir(self.data_folder_path):
            shutil.rmtree(self.data_folder_path)
        os.makedirs(self.data_folder_path)
        self.build = ChromiumBuild(self.repo_path, self.bin_folder_path, self.data_folder_path, self.driver_folder_path)

    def tearDown(self):
        if os.path.isdir(self.bin_folder_path):
            shutil.rmtree(self.bin_folder_path)
        if os.path.isdir(self.data_folder_path):
            shutil.rmtree(self.data_folder_path)

    def test_has_available_snapshot_locally(self):
        assert self.build.has_available_snapshot_locally("370050") is False
        assert self.build.has_available_snapshot_locally(370050) is False
        assert self.build.has_available_snapshot_locally("372561") is False
        assert self.build.has_available_snapshot_locally(372561) is False

        self.build.download_snapshot(370050)

        assert self.build.has_available_snapshot_locally("370050")
        assert self.build.has_available_snapshot_locally(370050)
        assert self.build.has_available_snapshot_locally("372561") is False
        assert self.build.has_available_snapshot_locally(372561) is False

        shutil.rmtree(self.build.bin_folder_path)

    def test_has_available_snapshot_online(self):
        pass
        # Skip test because it requires access to the MongoDB database
        # assert self.build.has_available_snapshot_online("370050")
        # assert self.build.has_available_snapshot_online("372561")

    def test_get_commit_pos_lineage(self):
        commit_pos_lineage = self.build.get_commit_pos_lineage(370050, 370261)
        if self.build.os_name == "Mac":
            assert len(commit_pos_lineage) == 57
        if self.build.os_name == "Linux":
            assert len(commit_pos_lineage) == 65
