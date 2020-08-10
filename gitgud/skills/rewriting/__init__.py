from gitgud.skills.level_builder import BasicLevel
from gitgud.skills.util import Skill

from gitgud import operations
from gitgud.skills.user_messages import simulate_command


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
        commits = reversed(commits)

        print('Run: "git rebase -i master~4"')
        print("You will see this: ")
        print()

        for sha, msg in commits:
            print("pick {} {}".format(sha, msg))
        print()

        print("Change it to this:")
        for msg in 'This is an easy level'.split():
            sha = commit_dict[msg]
            print("pick {} {}".format(sha, msg))


skill = Skill(
    'Rewriting History',
    'rewriting',
    [
        Easy('An Easy Level', 'easy', __name__)
    ]
)
