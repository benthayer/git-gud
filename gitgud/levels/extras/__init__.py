import pkg_resources

from gitgud.levels.util import BasicChallenge
from gitgud.levels.util import Level

level = Level(
    'merging',
    [
        BasicChallenge('octopus', pkg_resources.resource_filename(__name__, '_octopus/'))
    ]
)