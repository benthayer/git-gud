from gitgud.skills.util import Skill
from gitgud.skills.level_builder import BasicLevel

skill = Skill(
    'rampup',
    [
        BasicLevel('detaching', __name__),
        BasicLevel('relrefs1', __name__),
        BasicLevel('relrefs2', __name__),
        BasicLevel('reversing', __name__)
    ]
)
