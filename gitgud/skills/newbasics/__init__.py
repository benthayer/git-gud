from gitgud.skills.level_builder import BasicLevel
from gitgud.skills.util import Skill
from gitgud import operations
from gitgud.skills.user_messages import separated

class FirstCommit(BasicLevel):
    def _setup(self):
        file_operator = operations.get_operator()
        file_operator.destroy_repo()
        file_operator.use_repo()

    @separated
    def status(self):
        created, added, committed = self._get_state()
        print("Created:", bool_to_word(created))
        print("Added:", bool_to_word(added))
        print("Committed:", bool_to_word(committed))

    def _get_state(self):
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

        return created, added, committed

    def _test(self):
        return all(self._get_state())


skill = Skill(
    'New Basics',
    'newbasics',
    [
        FirstCommit('First Commit', 'firstcommit', __name__)
    ]
)
