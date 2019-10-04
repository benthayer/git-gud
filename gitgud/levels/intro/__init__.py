import pkg_resources

from gitgud.levels.util import BasicChallenge

commits = BasicChallenge(pkg_resources.resource_filename(__name__, '_commits/'))

all_challenges = [
    commits
]

del pkg_resources
del BasicChallenge