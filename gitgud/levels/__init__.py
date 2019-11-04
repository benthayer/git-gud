from gitgud.levels.intro import level as intro_level
from gitgud.levels.merging import level as merging_level

from gitgud.levels.util import AllLevels

all_levels = AllLevels([
        intro_level,
        merging_level
])

all_levels._add_next_challenges()