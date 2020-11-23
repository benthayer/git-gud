from gitgud.util import Skill
from gitgud.util.level_builder import BasicLevel

skill = Skill(
    'Rampup',
    'rampup',
    [
        BasicLevel("Detaching HEAD", 'detaching', __name__),
        BasicLevel("Relative References I: Using (^)", 'relrefs1', __name__),
        BasicLevel("Relative References II: Using (~)", 'relrefs2', __name__),
        BasicLevel("Reversing Changes in Git", 'reversing', __name__)
    ]
)
