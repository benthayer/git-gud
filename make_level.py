import sys
import os

path = os.path
join = os.path.join
cwd = os.getcwd()

def writeInit(skill_name, skill_path, level_name):
    # If skills/skill/__init__.py doesn't exist, create a basic version (no levels)
    if not path.exists(join(skill_path,"__init__.py")):
        with open(join(skill_path,"__init__.py"), 'w+') as fp:
            level_setup = "import pkg_resources\nfrom gitgud.skills.util import BasicLevel\nfrom gitgud.skills.util import Skill\n\nskill = Skill(\n\t'{}',\n\t[\n\t]\n)".format(skill_name)
            fp.write(level_setup)
        fp.close()
        
        # Read file
        with open(join(join("gitgud","skills"),"__init__.py"), 'r') as fp:
            filedata = fp.read()
        fp.close()

        # Add import statement
        replace = "from gitgud.skills.{0} import skill as {0}_skill\n\nfrom gitgud.skills.u".format(skill_name)
        filedata = filedata.replace("\nfrom gitgud.skills.u", replace)
        
        # Add to input array of Skill
        replace = ",\n\t{}_skill\n]".format(skill_name)
        filedata = filedata.replace("\n]", replace)
          
        # Write to file
        with open(join(join("gitgud","skills"),"__init__.py"), 'w') as fp:
            fp.write(filedata)
        fp.close()
        
        writeInit(skill_name, skill_path, level_name)
        print(fp.closed) #for debug, delete
        return
    else:
        # Populate file with BasicLevel
        with open(join(skill_path,"__init__.py"), 'r') as fp:
            filedata = fp.read()
        fp.close()

        replace = ",\n\t\tBasicLevel('{0}', pkg_resources.resource_filename(__name__, '_{0}/'))\n\t]".format(level_name)
        filedata = filedata.replace("\n\t]", replace)
        filedata = filedata.replace("[,","[")

        with open(join(skill_path,"__init__.py"), 'w') as fp:
            fp.write(filedata)
        fp.close()
        print(fp.closed) #for debug, delete
    return

def main():
    # Obtain input arguments
    skill_name = sys.argv[1]
    level_name = sys.argv[2]
    
    # Check if cwd is git-gud folder
    if cwd[-7:] == "git-gud":
            # Confirm choice to avoid making a mess
            print ("Confirm[y/n]: skill_name = \"{}\" & level_name = \"{}\"".format(skill_name,level_name))
            choice = input().lower()
            if choice == 'n':
                return
            
            # Make skill folder
            skill_path = join("gitgud","skills","{}".format(skill_name))
            if not path.exists(skill_path):
                os.mkdir(skill_path)
    
            # Make level folder
            level_path = join(skill_path,"_{}".format(level_name))
            if not path.exists(level_path):
                os.mkdir(level_path)
            
            writeInit(skill_name,skill_path,level_name)
            
            # Make instruction file
            inst_path = join(level_path,"instructions.txt")
            if not path.exists(inst_path):
                open(inst_path,'a').close()
            
            # Make goal file
            goal_path = join(level_path,"goal.txt")
            if not path.exists(goal_path):
                open(goal_path,'a').close()
            
            # Make setup file
            setup_path = join(level_path,"setup.spec")
            if not path.exists(setup_path):
                open(setup_path,'a').close()
    
            # Make test file
            test_path = join(level_path,"test.spec")
            if not path.exists(test_path):
                open(test_path,'a').close()
    else:
        print("Error: Execute this script in the git-gud directory.")


if __name__ == "__main__":
    main()


