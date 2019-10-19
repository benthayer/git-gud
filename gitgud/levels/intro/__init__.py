from collections import OrderedDict

import pkg_resources

from gitgud.levels.util import BasicChallenge

all_challenges = OrderedDict()
all_challenges['committing'] = BasicChallenge('committing', pkg_resources.resource_filename(__name__, '_committing/'))
all_challenges['branching'] = BasicChallenge('branching', pkg_resources.resource_filename(__name__, '_branching/'))
all_challenges['merging'] = BasicChallenge('merging', pkg_resources.resource_filename(__name__, '_merging/'))
all_challenges['rebasing'] = BasicChallenge('rebasing', pkg_resources.resource_filename(__name__, '_rebasing/'))
