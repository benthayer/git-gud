from gitgud.skills.level_builder import BasicLevel
from gitgud.skills.util import Skill

skill = Skill(
    'mixedbag',
    [
        BasicLevel('onecommit', __name__)
    ]
)
