import pkg_resources

from gitgud.levels.util import BasicChallenge
from gitgud.levels.util import Level

all_challenges = Level(
    'level',
    [
        BasicChallenge('octopus', pkg_resources.resource_filename(__name__, '_octopus/'))
    ]
)