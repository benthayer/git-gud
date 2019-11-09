import pkg_resources

from gitgud.skills.util import BasicLevel
from gitgud.skills.util import Skill

skill = Skill(
    'basics',
    [
        BasicLevel('committing', pkg_resources.resource_filename(__name__, '_committing/')),
        BasicLevel('branching', pkg_resources.resource_filename(__name__, '_branching/')),
        BasicLevel('merging', pkg_resources.resource_filename(__name__, '_merging/')),
        BasicLevel('rebasing', pkg_resources.resource_filename(__name__, '_rebasing/'))
    ]
)
