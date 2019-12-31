import os
import json

from gitgud.operations import get_operator

file_operator = get_operator()
commit_obj = file_operator.repo.head.commit

if os.path.exists(os.path.join(file_operator.git_path, "gud", "commits.json")):
    with open(os.path.join(file_operator.git_path, "gud", "commits.json")) as fp:
        commit_dict = json.load(fp)

        commit_dict["M"] = commit_obj.hexsha[:7]
        
    with open(os.path.join(file_operator.git_path, "gud", "commits.json"), 'w') as fp:
        json.dump(commit_dict, fp)
else:
    print("ERROR: Commit tracker does not exist!")


RENAME MERGE COMMIT PRIOR TO TRACKING, THEN USE NAME IN DICT.
