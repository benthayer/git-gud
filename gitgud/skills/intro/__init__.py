from gitgud.skills.util import Skill
from gitgud.skills.level_builder import BasicLevel
from gitgud.skills.user_messages import simulate_goal
from gitgud.skills.user_messages import show_tree

class Intro(BasicLevel):
    def __init__(self):
        super().__init__('intro' , __name__)

    def setup(self, file_operator):
        self._setup(file_operator)
        self.goal()

skill = Skill(
    'intro',
    [
        Intro()
    ]
)
