import pkg_resources

from gitgud.levels.util import BasicChallenge
from gitgud.levels.util import Level

level = Level(
    'rampup',
    [
        BasicChallenge('detaching', pkg_resources.resource_filename(__name__, '_detaching/')),
        BasicChallenge('relrefs1', pkg_resources.resource_filename(__name__, '_relrefs1/')),
        BasicChallenge('relrefs2', pkg_resources.resource_filename(__name__, '_relrefs2/'))
    ]
)