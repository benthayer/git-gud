import sys
import os



def main():
    # Obtain input arguments
    skill_name = sys.argv[1]
    level_name = sys.argv[2]
    
    path = os.path
    
    # Check if cwd is git-gud folder
    if cwd[-7:] == "git-gud":
            # Confirm choice to avoid making a mess
            print ("Confirm[y/n]: skill_name = \"{}\" & level_name = \"{}\"".format(skill_name,level_name))
            choice = input().lower()
            if choice == 'n':
                return
            
            # Make skill folder
            init_path = path.join("gitgud","skills","{}".format(skill_name))
            if not path.exists(skill_path):
                os.mkdir(skill_path)
    
            inst_path = path.join(level_path,"instructions.txt")
            if not path.exists(inst_path):
                open(inst_path,'a').close()
    
            # Make level folder
            level_path = path.join(skill_path,"_{}".format(level_name))
            if not path.exists(level_path):
                os.mkdir(level_path)
            
            # Make instruction file
            inst_path = path.join(level_path,"instructions.txt")
            if not path.exists(inst_path):
                open(inst_path,'a').close()
            
            # Make goal file
            goal_path = path.join(level_path,"goal.txt")
            if not path.exists(goal_path):
                open(goal_path,'a').close()
            
            # Make setup file
            setup_path = path.join(level_path,"setup.spec")
            if not path.exists(setup_path):
                open(setup_path,'a').close()
    
            # Make test file
            test_path = path.join(level_path,"test.spec")
            if not path.exists(test_path):
                open(test_path,'a').close()
    else:
        print("Error: Execute this script in the git-gud directory.")


if __name__ == "__main__":
    main()


