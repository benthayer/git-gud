from gitgud.levels.intro import all_challenges as intro_challenges
from gitgud.levels.merging import all_challenges as merging_challenges

from gitgud.levels.util import Level


levels = [
    Level('Intro', intro_challenges),
    Level('Merging', merging_challenges),
]