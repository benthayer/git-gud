import sys
import os

# Obtain input arguments
skill_name = sys.argv[1]
level_name = sys.argv[2]

cwd = os.getcwd()

if cwd[-7:] == "git-gud":
    path = os.path.join("gitgud","skills","{}".format(skill_name))
    if not os.path.exists(path):
        os.path.mkdir(path)




