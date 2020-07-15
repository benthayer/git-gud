from gitgud.skills.level_builder import BasicLevel
from gitgud.skills.util import Skill
from gitgud.operations import get_operator

class FirstCommit(BasicLevel):
    def _setup(self):
        get_operator().repo.git.checkout('--orphan', 'master')

    def post_setup(self):
        self.display_message('post-setup.txt')

    def _test(self):
        # As long as there's one commit, it doesn't matter what's in it
        # Use the existing setup so that any commit matches the first one
        # Test branches
        pass



skill = Skill(
    'Making and Saving Changes',
    'changes',
    [
        FirstCommit('Your First Commit', 'first', __name__),
        BasicLevel('One by One', 'onexone', __name__)
    ]
)
