import pkg_resources

from gitgud.levels.util import BasicChallenge
from gitgud.levels.util import NamedList

all_challenges = NamedList([
    ('committing', BasicChallenge('committing', pkg_resources.resource_filename(__name__, '_committing/'))),
    ('branching', BasicChallenge('branching', pkg_resources.resource_filename(__name__, '_branching/'))),
    ('merging', BasicChallenge('merging', pkg_resources.resource_filename(__name__, '_merging/'))),
    ('rebasing', BasicChallenge('rebasing', pkg_resources.resource_filename(__name__, '_rebasing/')))
])
