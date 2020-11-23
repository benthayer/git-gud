from gitgud.util import Skill
from gitgud.util.level_builder import BasicLevel

skill = Skill(
    'Basics',
    'basics',
    [
        BasicLevel('Introduction to Commits', 'committing', __name__),
        BasicLevel('Branching in Git', 'branching', __name__),
        BasicLevel('Merging in Git', 'merging', __name__),
        BasicLevel('Introduction to Rebasing', 'rebasing', __name__)
    ]
)
