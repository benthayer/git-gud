import pkg_resources

from gitgud.skills.util import BasicLevel
from gitgud.skills.util import Skill

skill = Skill(
    'extras',
    [
        BasicLevel('octopus', pkg_resources.resource_filename(__name__, '_octopus/'))
    ]
)