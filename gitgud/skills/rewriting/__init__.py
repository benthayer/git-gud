from gitgud.util.level_builder import BasicLevel
from gitgud.util import Skill

from gitgud.util import operations
from gitgud.user_messages import simulate_command


class SentenceLevel(BasicLevel):
    def post_setup(self):
        self.goal()
        self.status()

    def status(self):
        simulate_command('git log --reverse --oneline')


class Easy(SentenceLevel):
    def solution(self):
        commit = operations.get_operator().repo.head.commit

        commits = []
        commit_dict = {}
        while commit:
            commits.append((commit.hexsha[:7], commit.message))
            commit_dict[commit.message] = commit.hexsha[:7]
            if commit.parents:
                commit = commit.parents[0]
            else:
                commit = None

        # Chronological order
        commits = list(reversed(commits))

        this_hash = commit_dict['This']
        print('Run: "git rebase -i {}"'.format(this_hash))
        print('"{}" is the hash of the commit with the message "This"'
              .format(this_hash))
        print()
        print("You will see this: ")

        for sha, msg in commits[1:]:
            print(4*" " + "pick {} {}".format(sha, msg))
        print()

        print("Change it to this:")
        for msg in 'is an easy level'.split():
            sha = commit_dict[msg]
            print(4*" " + "pick {} {}".format(sha, msg))

        print()
        print('The order of commits will now be "This is an easy level"')


skill = Skill(
    'Rewriting History',
    'rewriting',
    [
        Easy('An Easy Level', 'easy', __name__)
    ]
)
