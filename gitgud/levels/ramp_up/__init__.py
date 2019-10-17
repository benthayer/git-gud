from collections import OrderedDict

import pkg_resources

from gitgud.levels.util import BasicChallenge

all_challenges = OrderedDict()
all_challenges['detaching'] = BasicChallenge('detaching', pkg_resources.resource_filename(__name__, '_detaching/'))
all_challenges['rel refs 1'] = BasicChallenge('rel_refs_1', pkg_resources.resource_filename(__name__, '_rel_refs1/'))
all_challenges['rel refs 2'] = BasicChallenge('rel_refs_2', pkg_resources.resource_filename(__name__, '_rel_refs2/'))
all_challenges['reversing'] = BasicChallenge('reversing', pkg_resources.resource_filename(__name__, '_reversing/'))
