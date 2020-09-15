from gitgud.skills.level_builder import BasicLevel
from gitgud.skills.util import Skill
from gitgud import operations
from gitgud.skills.user_messages import separated, bool_to_word


class FirstCommit(BasicLevel):
    def _setup(self):
        file_operator = operations.get_operator()
        file_operator.destroy_repo()
        file_operator.use_repo()

    @separated
    def status(self):
        created, added, committed = self.get_solved_state()
        print("Created:", bool_to_word(created))
        print("Added:", bool_to_word(added))
        print("Committed:", bool_to_word(committed))

    def get_solved_state(self):
        created = False
        added = False
        committed = True
        file_operator = operations.get_operator()
        created_files = file_operator.get_working_directory_content()
        if created_files:
            created = True
        added_files = file_operator.get_staging_content()
        if added_files:
            added = True
        committed = file_operator.repo.head.is_valid()

        return bool(created), bool(added), bool(committed)

    def _test(self):
        created, added, committed = self.get_solved_state()
        return created and added and committed

    def post_setup(self):
        self.cat_file("post-setup.txt")


skill = Skill(
    'New Basics',
    'newbasics',
    [
        FirstCommit('First Commit', 'firstcommit', __name__)
    ]
)
