import pkg_resources

from gitgud.levels.util import BasicChallenge
from gitgud.levels.util import NamedList

all_challenges = NamedList([
    ('octopus', BasicChallenge('octopus', pkg_resources.resource_filename(__name__, '_octopus/')))
])