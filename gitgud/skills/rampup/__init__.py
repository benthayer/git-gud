import pkg_resources

from gitgud.skills.util import BasicLevel
from gitgud.skills.util import Skill

skill = Skill(
    'rampup',
    [
        BasicLevel('detaching', pkg_resources.resource_filename(__name__, '_detaching/')),
        BasicLevel('relrefs1', pkg_resources.resource_filename(__name__, '_relrefs1/')),
        BasicLevel('relrefs2', pkg_resources.resource_filename(__name__, '_relrefs2/')),
        BasicLevel('reversing', pkg_resources.resource_filename(__name__, '_reversing/'))
    ]
)
