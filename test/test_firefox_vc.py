import os
import unittest
from bci.version_control.firefox_vc import FirefoxRepo, FirefoxRepoState


class TestFirefoxRepo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        cls.repo_path = os.path.join(curr_dir, "resources/repositories/mercurial")
        cls.repo = FirefoxRepo(cls.repo_path)
        assert os.path.isdir(cls.repo_path)

    @classmethod
    def tearDownClass(cls):
        cls.repo_path = None
        cls.repo = None

    def setUp(self):
        self.repo.checkout("tip")

    def test_is_repo(self):
        assert FirefoxRepo.is_repo(self.repo_path)
        assert FirefoxRepo.is_repo(".") is False

    def test_checkout(self):
        self.repo.checkout("init")
        files = os.listdir(self.repo_path)
        assert "hello_world" in files
        assert "other_file" not in files

        self.repo.checkout("tip")
        files = os.listdir(self.repo_path)
        assert "hello_world" in files
        assert "other_file" in files

        self.repo.checkout("27c")
        files = os.listdir(self.repo_path)
        assert "hello_world" in files
        assert "other_file" not in files

    def test_is_tag(self):
        assert self.repo.is_tag("init")
        assert self.repo.is_tag("tip")
        assert self.repo.is_tag("bogus") is False

    def test_get_tag_list(self):
        tag_list = self.repo.get_tag_list()
        assert len(tag_list) == 2
        assert "init" in tag_list
        assert "new-branch" in tag_list

    def test_get_changeset_id(self):
        assert self.repo.get_changeset_id("init") == "0f698eed46f1c249476548b630bb8639acaf0a13"
        assert self.repo.get_changeset_id("tip") == "f7bda02ad29caf767c4ec76d053439442e4cebb9"

    def test_get_changeset_parent_ids(self):
        parents = self.repo.get_changeset_parent_ids("tip")
        assert len(parents) == 1
        assert "03aaa52c94cc9225d178cebad41efdc0391efa18" in parents

        parents = self.repo.get_changeset_parent_ids("init")
        assert len(parents) == 0

    def test_get_changeset_child_ids(self):
        children = self.repo.get_changeset_child_ids("init")
        assert len(children) == 2
        assert "24623b066796782c7d178063b9d3849885286e62" in children
        assert "88638838a1d37d4f362283b49d705dcae64addc0" in children

        children = self.repo.get_changeset_child_ids("tip")
        assert len(children) == 0

    def test_get_state_lineage(self):
        state_lineage = self.repo.get_state_lineage_from_states(
            FirefoxRepoState("0f698eed46f1c249476548b630bb8639acaf0a13"),
            FirefoxRepoState("450c31e479eca6d09dce97a0a893042b000ef3fa"))

        assert state_lineage.length == 5
        assert state_lineage.ancestor_state.id == "0f698eed46f1c249476548b630bb8639acaf0a13"
        assert len(state_lineage.ancestor_state.parents) == 0
        assert state_lineage.descendant_state.id == "450c31e479eca6d09dce97a0a893042b000ef3fa"
        assert len(state_lineage.descendant_state.children) == 0

        assert len(state_lineage.ancestor_state.children) == 1
        assert state_lineage.ancestor_state.children[0].id == "24623b066796782c7d178063b9d3849885286e62"

        assert len(state_lineage.descendant_state.parents) == 1
        assert state_lineage.descendant_state.parents[0].id == "27cd824a247185fd5ee8fad9811572a6367637c2"

        assert state_lineage.ancestor_state.children[0].children[0].children[0].children[0] == state_lineage.descendant_state

        assert len(state_lineage.states) == 5
        assert state_lineage.states[0].id == "0f698eed46f1c249476548b630bb8639acaf0a13"
        assert state_lineage.states[1].id == "24623b066796782c7d178063b9d3849885286e62"
        assert state_lineage.states[2].id == "81d3e53a2fb38f2e23455b6b731f86f57a08e78d"
        assert state_lineage.states[3].id == "27cd824a247185fd5ee8fad9811572a6367637c2"
        assert state_lineage.states[4].id == "450c31e479eca6d09dce97a0a893042b000ef3fa"

    def test_get_changeset_lineage(self):
        lineage = self.repo.get_changeset_lineage("init", "tip")
        assert len(lineage) == 8

    # def test_is_descendant_of(self):
    #    assert self.repo.is_descendant_of("init", "tip")
    #    assert self.repo.is_descendant_of("tip", "init") is False
