import sys
from gitgud.operations import get_operator

file_operator = get_operator()
rebase_to_branch = sys.argv[1]

"""
if file_operator.repo.head.is_detached:
    head_name = file_operator.repo.commit('HEAD').message.strip()
    print(head_name)
else:
    head_name = file_operator.repo.head.ref.name
    print(head_name)
    for branch in file_operator.repo.branches:
        if (branch == head_name):
            commits.add(branch.commit)
            commit_name = branch.commit.message.strip()
            print(commits)
    print(head_name)"""
    

rebasing_commits = set()        # Commits referenced by rebased branch.
rebasing_const = set()          # Set used to construct rebasing_commits.
rebase_to_commits = set()       # Commits referenced by destination branch.
rebase_to_const = set()         # Set used to construct rebasing_to_commits.
rebased_commits = set()         # Commits that were rebased.

# TODO: Add detached head option.
head_name = file_operator.repo.head.ref.name
for branch in file_operator.repo.branches:
    if (str(branch) == head_name):
        rebasing_const.add(branch.commit)
        while len(rebasing_const) > 0:
            testing = rebasing_const.pop()
            for parent in testing.parents:
                if parent not in rebasing_const:
                    rebasing_const.add(parent)
            rebasing_commits.add(testing)
    elif (str(branch) == rebase_to_branch):
        rebase_to_const.add(branch.commit)
        while len(rebase_to_const) > 0:
            testing = rebase_to_const.pop()
            for parent in testing.parents:
                if parent not in rebase_to_const:
                    rebase_to_const.add(parent)
            rebase_to_commits.add(testing)

while len(rebasing_commits) > 0:
    cur_commit = rebasing_commits.pop()
    if cur_commit not in rebase_to_commits:
        rebased_commits.add(cur_commit)

print("Rebased commits:")
for commit in rebased_commits:
    commit.message = commit.message.strip() + "'"
    print(commit.message.strip())
