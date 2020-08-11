from gitgud.skills.level_builder import BasicLevel
from gitgud.skills.util import Skill
from gitgud import operations

class FirstCommit(BasicLevel):
    def post_setup(self):
        self.cat_file('post-setup.txt')


    def is_one_commit(self):
        pass

    def status(self):

        op = operations.get_operator()
        from pathlib import Path
        has_file = len(list(Path(op.path).iterdir())) >= 2  # git directory == 1
        try:
            op.repo.head.commit
            has_commit = True
        except ValueError:
            has_commit = False
        print('Created file?     {}'.format(has_file))
        print('Created commit?   {}'.format(has_commit))

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
