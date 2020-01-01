import sys

from gitgud.operations import get_operator


if sys.argv[1] == ".git/COMMIT_EDITMSG":
    pass
elif sys.argv[1] == ".git/MERGE_MSG":
    # Count the number of merges that already exist.
    file_operator = get_operator()
    tree = file_operator.get_current_tree()
    num_merges = 0
    for key in tree['commits']:
        if "M" in key:
            num_merges = num_merges + 1
    
    # Set the name of the merge commit in the making.
    with open (sys.argv[1], 'w') as fp:
        fp.write("M" + str(num_merges + 1))
