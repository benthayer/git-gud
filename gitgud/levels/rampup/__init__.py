from collections import OrderedDict

import pkg_resources

from gitgud.levels.util import BasicChallenge

all_challenges = OrderedDict()
all_challenges['reversing'] = BasicChallenge('reversing', pkg_resources.resource_filename(__name__, '_reversing/'))
