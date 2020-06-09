from gitgud.skills.util import Skill
from gitgud.skills.level_builder import BasicLevel

skill = Skill(
    'basics',
    [
        BasicLevel('committing', __name__, 'Introduction to Commits'),
        BasicLevel('branching', __name__, 'Branching in Git'),
        BasicLevel('merging', __name__, 'Merging in Git'),
        BasicLevel('rebasing', __name__, 'Introduction to Rebasing')
    ],
    'Basics'
)
