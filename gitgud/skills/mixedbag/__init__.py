from gitgud.util.level_builder import BasicLevel
from gitgud.util import Skill

skill = Skill(
    "Mixed Bag",
    'mixedbag',
    [
        BasicLevel("One Commit", 'onecommit', __name__)
    ]
)
