from collections import OrderedDict

from gitgud.levels.intro import all_challenges as intro_challenges
from gitgud.levels.rampup import all_challenges as ramp_up_challenges
from gitgud.levels.extras import all_challenges as merging_challenges

from gitgud.levels.util import Level

all_levels = OrderedDict()

all_levels['intro'] = Level('intro', intro_challenges)
all_levels['rampup'] = Level('rampup', ramp_up_challenges)
all_levels['extras'] = Level('extras', merging_challenges)


def _add_next_challenges():
    last_challenge = None
    for level in all_levels.values():
        for challenge in level.challenges.values():
            if last_challenge is not None:
                last_challenge.next_challenge = challenge
            last_challenge = challenge


_add_next_challenges()
