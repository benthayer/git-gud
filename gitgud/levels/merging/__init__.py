from collections import OrderedDict

import pkg_resources

from gitgud.levels.util import BasicChallenge

all_challenges = OrderedDict()
all_challenges['octopus'] = BasicChallenge('octopus', pkg_resources.resource_filename(__name__, '_octopus/'))

del OrderedDict
del pkg_resources
del BasicChallenge