from gitgud.skills.intro import skill as intro_skill
from gitgud.skills.basics import skill as basics_skill
from gitgud.skills.rampup import skill as rampup_skill
from gitgud.skills.rework import skill as rework_skill
from gitgud.skills.mixedbag import skill as mixedbag_skill
from gitgud.skills.extras import skill as extras_skill
from gitgud.skills.rewriting import skill as rewriting_skill
from gitgud.skills.newbasics import skill as newbasics_skill

from gitgud.util import AllSkills

all_skills = AllSkills([
    intro_skill,
    basics_skill,
    rampup_skill,
    rework_skill,
    mixedbag_skill,
    extras_skill,
    rewriting_skill,
    newbasics_skill
])

all_levels = []

for skill in all_skills:
    for level in skill:
        all_levels.append(level)
