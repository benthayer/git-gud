from collections import OrderedDict

import pkg_resources

from gitgud.levels.util import BasicChallenge

all_challenges = OrderedDict()
all_challenges['relrefs2'] = BasicChallenge('relrefs2', pkg_resources.resource_filename(__name__, '_relrefs2/'))
