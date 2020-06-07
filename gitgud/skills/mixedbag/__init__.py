from gitgud.skills.level_builder import BasicLevel
from gitgud.skills.util import Skill

skill = Skill(
    'mixedbag',
    [
        BasicLevel('jugglecommits1', __name__)
    ]
)
