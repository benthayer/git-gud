from gitgud.util.level_builder import BasicLevel
from gitgud.util import Skill

skill = Skill(
    'Rework',
    'rework',
    [
        BasicLevel('Cherrypicking', 'cherrypicking', __name__),
        BasicLevel('Interactive Rebase', 'irebase', __name__)
    ]
)
