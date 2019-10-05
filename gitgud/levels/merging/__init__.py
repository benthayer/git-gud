import pkg_resources

from gitgud.levels.util import BasicChallenge

octopus = BasicChallenge('octopus', pkg_resources.resource_filename(__name__, '_octopus/'))

all_challenges = [
    octopus
]

del pkg_resources
del BasicChallenge