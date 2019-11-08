from gitgud.skills.basics import skill as basics_skill
from gitgud.skills.rampup import skill as rampup_skill
from gitgud.skills.extras import skill as extras_skill

from gitgud.skills.util import AllSkills

all_skills = AllSkills([
    basics_skill,
    rampup_skill,
    extras_skill
])
