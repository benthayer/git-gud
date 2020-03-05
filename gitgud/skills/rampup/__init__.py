from gitgud.skills.util import BasicLevel
from gitgud.skills.util import Skill

skill = Skill(
    'rampup',
    [
        BasicLevel(level_name, __name__) for level_name in ['detaching', 'relrefs1', 'relrefs2', 'reversing']
    ]
)
