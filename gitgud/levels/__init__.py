from gitgud.levels.intro import level as intro_level
from gitgud.levels.rampup import level as rampup_level
from gitgud.levels.extras import level as extras_level

from gitgud.levels.util import AllLevels

all_levels = AllLevels([
    intro_level,
    rampup_level,
    extras_level
])
