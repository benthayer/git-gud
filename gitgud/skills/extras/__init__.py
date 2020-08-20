from gitgud.skills.util import Skill
from gitgud.skills.level_builder import BasicLevel

skill = Skill(
    'Extras',
    'extras',
    [
        BasicLevel('The Octopus Merge', 'octopus', __name__)
    ]
)
