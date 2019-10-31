from collections import OrderedDict

import pkg_resources

from gitgud.levels.util import BasicChallenge

all_challenges = OrderedDict()
all_challenges['cherrypick'] = BasicChallenge('cherrypick', pkg_resources.resource_filename(__name__, '_cherrypick/'))