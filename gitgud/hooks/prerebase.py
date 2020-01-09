import sys
import json
import subprocess

from gitgud.operations import get_operator

file_operator = get_operator()
rebase_to_arg = sys.argv[1]     # Name/hash of the destination branch/commit

# Need the commit belonging to the HEAD (rebase reference)
# And need the commit belonging to the destination.
head_commit = file_operator.repo.head.commit
rebase_to_commit = ""           # Placeholder Instantiation

# If destination is a branch name, finding the rebase_to commit is easy:
for branch in file_operator.repo.branches:
    if str(branch) == rebase_to_arg:
        rebase_to_commit = branch.commit

# If destination is a commit hash,
# need to compare against all commit hashes to find object.

testing_commits = set()     # Commits being processed.
tree_commits = set()        # Holds all the commit objects in the tree.

# First, add all branch commits.
for branch in file_operator.repo.branches:
    testing_commits.add(branch.commit)
    
# Second, add detached head commit.
# Branch commits + (possible) Detached HEAD commit = All possible leaf nodes.
if file_operator.repo.head.is_detached:
    testing_commits.add(file_operator.repo.head.commit)
    
# Add all internal nodes to tree_commits set.
while len(testing_commits) > 0:
    test_commit = testing_commits.pop()
    for parent in test_commit.parents:
        if parent not in tree_commits:
            testing_commits.add(parent)
    tree_commits.add(test_commit)

# Search tree for matching destination hash.
if rebase_to_commit == "":
    for commit in tree_commits:
        if rebase_to_arg in str(commit)[:(len(rebase_to_arg) - 1)]:
            rebase_to_commit = commit
            break

# Now, use these two commits to find the set of rebased commit objects.
rebasing_const = set()          # Set used to construct rebasing_commits.
rebasing_commits = set()        # Commits referenced by rebased branch.
rebase_to_const = set()         # Set used to construct rebasing_to_commits.
rebase_to_commits = set()       # Commits referenced by destination branch.

# Record all commits in the rebase_to branch.
rebase_to_const.add(rebase_to_commit)
while len(rebase_to_const) > 0:
    testing = rebase_to_const.pop()
    for parent in testing.parents:
        if parent not in rebase_to_commits:
            rebase_to_const.add(parent)
    rebase_to_commits.add(testing)

# Record all commits that were rebased.
rebasing_const.add(head_commit)
while len(rebasing_const) > 0:
    testing = rebasing_const.pop()
    for parent in testing.parents:
        if parent not in rebasing_commits and parent not in rebase_to_commits:
            rebasing_const.add(parent)
    rebasing_commits.add(testing)

# Store cmd line name of rebase ref and destination ref.
rebase_info = {}
if file_operator.repo.head.is_detached:
    # Detached Commit Hash
    rebase_info['rebased'] = str(file_operator.repo.head.commit)
elif file_operator.repo.head.ref.name in file_operator.repo.branches:
    # Branch Name
    rebase_info['rebased'] = file_operator.repo.head.ref.name
rebase_info['rebase_to'] = rebase_to_arg    # Can be hash or branch name.

# For each commit that is rebased:
#   - Store {(message:hash)}
for commit in rebasing_commits:
    rebase_info[commit.message.strip()] = str(commit)

# Store rebase_info into json file for use by postrewrite.py.
with open(file_operator.rebase_info_path, 'w') as fp:
    json.dump(rebase_info, fp)

# Upon exiting this python script, the shell script will abort the user's rebase.
# It is essentially being replaced by ours below.
# TODO: Parse user-selected options.
print("Cancelling user rebase and replacing with simulation.")
print("Simulating 'git rebase':")
cmd = 'git commit --amend --no-post-rewrite --quiet -m"$(git log -n1 --format=%s)\'"'
subprocess.call(["git", "rebase", rebase_to_arg, "--no-verify", "-x", cmd])


