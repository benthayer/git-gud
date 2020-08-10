from gitgud.skills.level_builder import BasicLevel
from gitgud.skills.util import Skill

from gitgud.skills.user_messages import simulate_command


class SentenceLevel(BasicLevel):
    def post_setup(self):
        self.goal()
        self.status()

    def status(self):
        simulate_command('git log --reverse --oneline')


class Easy(SentenceLevel):
    pass


skill = Skill(
    'Rewriting History',
    'rewriting',
    [
        Easy('An Easy Level', 'easy', __name__)
    ]
)
