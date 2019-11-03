import pkg_resources

from gitgud.levels.util import BasicChallenge
from gitgud.levels.util import Level

level = Level(
    'intro',
    [
        BasicChallenge('committing', pkg_resources.resource_filename(__name__, '_committing/')),
        BasicChallenge('branching', pkg_resources.resource_filename(__name__, '_branching/')),
        BasicChallenge('merging', pkg_resources.resource_filename(__name__, '_merging/')),
        BasicChallenge('rebasing', pkg_resources.resource_filename(__name__, '_rebasing/'))
    ]
)