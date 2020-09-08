from gitgud.skills.level_builder import BasicLevel
from gitgud.skills.util import Skill
from gitgud import operations
from gitgud.skills.user_messages import firstcommit_status


class FirstCommit(BasicLevel):
    def _setup(self):
        file_operator = operations.get_operator()
        file_operator.destroy_repo()
        file_operator.use_repo()

    def status(self):
        firstcommit_status(*self._get_state())

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
        try:
            file_operator.repo.head.commit
        except ValueError:
            committed = False

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
