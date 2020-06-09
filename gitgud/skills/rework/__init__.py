from gitgud.skills.level_builder import BasicLevel
from gitgud.skills.util import Skill

skill = Skill(
    'rework',
    [
        BasicLevel('cherrypicking', __name__)
    ],
    'Rework'
)
