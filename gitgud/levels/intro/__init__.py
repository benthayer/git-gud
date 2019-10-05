from collections import OrderedDict

import pkg_resources

from gitgud.levels.util import BasicChallenge

all_challenges = OrderedDict()
all_challenges['commits'] = BasicChallenge('commits', pkg_resources.resource_filename(__name__, '_commits/'))

del pkg_resources
del BasicChallenge