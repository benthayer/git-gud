import os
import json

from gitgud.operations import get_operator

file_operator = get_operator()
commit_obj = file_operator.repo.head.commit

# Count the number of merge commits that already exist.
tree = file_operator.get_current_tree()
num_merges = 0
for key in tree['commits']:
    if "M" in key:
        num_merges = num_merges + 1

new_merge = "M" + str(num_merges)
if os.path.exists(file_operator.commits_json_path):
    with open(file_operator.commits_json_path) as fp:
        commit_dict = json.load(fp)

        commit_dict[new_merge] = commit_obj.hexsha[:7]
        
    with open(file_operator.commits_json_path, 'w') as fp:
        json.dump(commit_dict, fp)
else:
    print("ERROR: Commit tracker does not exist!")




