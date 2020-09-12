from gitgud import operations

from gitgud.skills.level_builder import BasicLevel
from gitgud.skills.util import Skill

from gitgud.skills.user_messages import simulate_command


class SentenceLevel(BasicLevel):
    def post_setup(self):
        self.goal()
        self.status()

    def status(self):
        simulate_command('git log --reverse --oneline')


class Truth(SentenceLevel):
    def _test(self):
        if not super()._test():
            return False

        file_operator = operations.get_operator()

        for branch in file_operator.repo.branches:
            if branch.commit == file_operator.repo.head.commit:
                return True

        return False


skill = Skill(
    'Rewriting History',
    'rewriting',
    [
        Truth('The Truth', 'truth', __name__)
    ]
)
