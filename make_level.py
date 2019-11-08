import sys
import os

# Obtain input arguments
skill_name = sys.argv[1]
level_name = sys.argv[2]

cwd = os.getcwd()

if cwd[-7:] == "git-gud":
    skill_path = os.path.join("gitgud","skills","{}".format(skill_name))
    if not os.path.exists(skill_path):
        os.mkdir(skill_path)

    level_path = os.path.join(skill_path,"{}".format(level_name))
    if not os.path.exists(level_path):
        os.mkdir(level_path)

    inst_path = os.path.join(level_path,"instructions.txt")
    if not os.path.exists(inst_path):
        open(inst_path,'a').close()

    goal_path = os.path.join(goal_path,"instructions.txt")
    if not os.path.exists(goal_path):
        open(goal_path,'a').close()

    setup_path = os.path.join(level_path,"setup.spec")
    if not os.path.exists(inst_path):
        open(setup_path,'a').close()

    test_path = os.path.join(level_path,"test.spec")
    if not os.path.exists(test_path):
        open(test_path,'a').close()
else:
    print("Error: Execute this script in the git-gud directory.")




