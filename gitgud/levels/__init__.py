from collections import OrderedDict

from gitgud.levels.intro import all_challenges as intro_challenges
from gitgud.levels.merging import all_challenges as merging_challenges

from gitgud.levels.util import Level


all_levels = OrderedDict()

all_levels['intro'] = Level('intro', intro_challenges)
all_levels['merging'] = Level('merging', merging_challenges)

last_challenge = None
for level in all_levels[1:]:
    for challenge in level.challenges:
        if last_challenge is not None:
            last_challenge.next_challenge = challenge
        last_challenge = challenge

try:
    del level
except NameError:
    pass

try:
    del challenge
except NameError:
    pass


del Level