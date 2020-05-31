from gitgud.skills.util import Skill
from gitgud.skills.level_builder import BasicLevel


class Intro(BasicLevel):
    def __init__(self):
        super().__init__('intro', __name__)

    def setup(self, file_operator):
        self._setup(file_operator)
        self.goal()

    def _test(self, file_operator):
        return True


skill = Skill(
    'intro',
    [
        Intro()
    ]
)
