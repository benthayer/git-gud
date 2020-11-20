from gitgud.skills.level_builder import BasicLevel
from gitgud.skills.util import Skill
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

    def status(self):
        display_repo_files()



skill = Skill(
    'New Basics',
    'newbasics',
    [
        FirstCommit('First Commit', 'firstcommit', __name__),
        BasicLevel('Two Commits', 'two', __name__)
    ]
)
