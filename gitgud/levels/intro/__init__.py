import pkg_resources

from gitgud.levels.util import BasicChallenge

print(__file__)
DIR = pkg_resources.resource_filename('gitgud.levels.intro', 'commits/')

commits = BasicChallenge('commits')

all_challenges = [
    commits
]
