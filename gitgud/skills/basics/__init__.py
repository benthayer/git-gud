from gitgud.skills.util import Skill
from gitgud.skills.level_builder import BasicLevel

skill = Skill(
    'basics',
    [
        BasicLevel('committing', __name__),
        BasicLevel('branching', __name__),
        BasicLevel('merging', __name__),
        BasicLevel('rebasing', __name__)
    ]
)
