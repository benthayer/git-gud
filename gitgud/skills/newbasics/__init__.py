from gitgud.util.level_builder import BasicLevel
from gitgud.util import Skill
from gitgud import operations
from gitgud.user_messages import separated, bool_to_word
from gitgud.user_messages.stateful import display_repo_files


class FirstCommit(BasicLevel):
    def _setup(self):
        file_operator = operations.get_operator()
        file_operator.destroy_repo()
        file_operator.use_repo()

    @separated
    def status(self):
        created, added, committed = self.get_state()
        print("Created:", bool_to_word(created))
        print("Added:", bool_to_word(added))
        print("Committed:", bool_to_word(committed))

    def get_state(self):
        file_operator = operations.get_operator()

        created = bool(file_operator.get_working_directory_content())
        added = bool(file_operator.get_staging_content())
        committed = file_operator.repo.head.is_valid() \
            and bool(file_operator.get_commit_content('HEAD'))

        return created, added, committed

    def _test(self):
        created, added, committed = self.get_state()
        return created and added and committed

    def post_setup(self):
        self.cat_file("post-setup.txt")


class TwoCommits(BasicLevel):
    def _setup(self):
        file_operator = operations.get_operator()
        file_operator.destroy_repo()
        file_operator.use_repo()

    def post_setup(self):
        self.goal()

    def status(self):
        display_repo_files()

    def _test(self):
        # There are two commits
        # The first commit has one file
        # The second commit has two files
        # The file from the first commit is in the second commit
        # The first file is unchanged
        # Working Directory, Staging Area and Commit 2 are the same

        file_operator = operations.get_operator()

        if len(file_operator.get_all_commits()) != 2:
            return False

        content1 = file_operator.get_commit_content('HEAD~')
        if len(content1.keys()) != 1:
            return False

        content2 = file_operator.get_commit_content('HEAD')
        if len(content2.keys()) != 2:
            return False

        file1_name = next(iter(content1.keys()))
        if file1_name not in content2:
            return False

        if content1[file1_name] != content2[file1_name]:
            return False

        content_wd = file_operator.get_working_directory_content()
        content_sa = file_operator.get_staging_content()
        if not (content2 == content_wd == content_sa):
            return False

        return True


skill = Skill(
    'New Basics',
    'newbasics',
    [
        FirstCommit('First Commit', 'firstcommit', __name__),
        TwoCommits('Two Commits', 'two', __name__)
    ]
)
