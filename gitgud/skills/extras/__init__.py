from gitgud.skills.util import Skill
from gitgud.skills.level_builder import BasicLevel

skill = Skill(
    'extras',
    [
        BasicLevel('octopus', __name__, 'The Octopus Merge')
    ]
)
