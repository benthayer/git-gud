from gitgud.levels.intro import level as intro_level
from gitgud.levels.merging import level as merging_level

from gitgud.levels.util import Level
from gitgud.levels.util import AllLevels

all_levels = AllLevels(
    [
        intro_level,
        merging_level
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
