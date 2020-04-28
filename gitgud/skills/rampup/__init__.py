from gitgud.skills.util import Skill
from gitgud.skills.level_builder import BasicLevel

skill = Skill(
    'rampup',
    [
        BasicLevel('detaching', __name__, "Detaching HEAD"),
        BasicLevel('relrefs1', __name__, "Relative References I: Using (^)"),
        BasicLevel('relrefs2', __name__, "Relative References II: Using (~)"),
        BasicLevel('reversing', __name__, "Reversing Changes in Git")
    ]
)
