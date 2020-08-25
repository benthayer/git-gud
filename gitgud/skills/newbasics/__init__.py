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
        created = False
        added = False
        committed = False
        file_operator = operations.get_operator()
        created_files = file_operator.get_working_directory_content()
        if created_files:
            created = True
        added_files = file_operator.get_staging_content()
        if added_files:
            added = True
        try:
            committed_files = file_operator.get_commit_content("HEAD")
            if committed_files:
                committed = True
        except:
            pass
        firstcommit_status(created, added, committed)
        
skill = Skill(
    'New Basics',
    'newbasics',
    [
        FirstCommit('First Commit', 'firstcommit', __name__)
    ]
)
