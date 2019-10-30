from gitgud.levels.intro import all_challenges as intro_challenges
from gitgud.levels.merging import all_challenges as merging_challenges

from gitgud.levels.util import Level
from gitgud.levels.util import AllLevels

all_levels = AllLevels(
    [
        Level('intro', intro_challenges),
        Level('merging', merging_challenges)
    ]
)

def _add_next_challenges():
    last_challenge = None
    for level in all_levels:
        for challenge in level:
            if last_challenge is not None:
                last_challenge.next_challenge = challenge
            last_challenge = challenge

_add_next_challenges()
