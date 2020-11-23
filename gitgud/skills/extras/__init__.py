from gitgud.util import Skill
from gitgud.util.level_builder import BasicLevel

skill = Skill(
    'Extras',
    'extras',
    [
        BasicLevel('The Octopus Merge', 'octopus', __name__)
    ]
)
