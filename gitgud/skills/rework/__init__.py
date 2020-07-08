from gitgud.skills.level_builder import BasicLevel
from gitgud.skills.util import Skill

skill = Skill(
    'Rework',
    'rework',
    [
        BasicLevel('Cherrypicking', 'cherrypicking', __name__),
        BasicLevel('Interactive Rebase', 'irebase', __name__)
    ]
)
