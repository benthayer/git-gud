from gitgud.skills.level_builder import BasicLevel
from gitgud.skills.util import Skill

skill = Skill(
    "Mixed Bag",
    'mixedbag',
    [
        BasicLevel("One Commit", 'onecommit', __name__)
    ]
)
