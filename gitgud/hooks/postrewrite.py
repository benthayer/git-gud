import sys
import json
import subprocess

from gitgud.operations import get_operator


file_operator = get_operator()
with open(file_operator.rebase_info_path) as fp:
    rebase_info = json.load(fp)

# Create Tree
tree_dict = {}
testing_commits = set()     # Commits being processed.
tree_commits = set()        # Holds all the commit objects in the tree.

# First, add all branch commits.
for branch in file_operator.repo.branches:
    testing_commits.add(branch.commit)

# Second, add detached head commits.
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
    tree_dict[test_commit.message.strip()] = str(test_commit)

# TODO: Git hooks should not actually do any logging
# TODO: Keep track of rebased commits

with open(file_operator.commits_json_path) as fp:
    commits_json = json.load(fp)

print()
if "rebase" in sys.argv:
    print("Logging for Rebase:")
    for key in rebase_info:
        if key != 'rebased' and key != 'rebase_to':
            print("Changes for Commit: " + key)
            print("    Old Hash: " + rebase_info[key])
            print("    New Hash: " + tree_dict[key + "'"])
            # Does not delete old commit info.
            commits_json[key + "'"] = [rebase_info[key][:7], tree_dict[key + "'"][:7]]
    print()
elif "amend" in sys.argv:
    print("Logging for Amended Commit:")
    for i, line in enumerate(sys.stdin):
        old_hash, new_hash = line.split()
        print('Change #{}:'.format(i + 1))
        print('    Old hash: ', old_hash)
        print('    New hash: ', new_hash)

with open(file_operator.commits_json_path, 'w') as fp:
    json.dump(commits_json, fp)
