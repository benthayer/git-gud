from gitgud.skills.util import BasicLevel
from gitgud.skills.util import Skill

skill = Skill(
    'basics',
    [
        BasicLevel(level_name, __name__) for level_name in ['committing', 'branching', 'merging', 'rebasing']
    ]
)
