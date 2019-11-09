import sys
import os

cwd = os.getcwd()

def write_init(skill_name, skill_path, level_name):
    # If skills/skill/__init__.py doesn't exist, create a basic version (no levels)
    if not os.path.exists(os.path.join(skill_path,"__init__.py")):
        with open(os.path.join(skill_path,"__init__.py"), 'w+') as fp:
            level_setup = "\n".join([
                "import pkg_resources\n",
                "from gitgud.skills.util import BasicLevel",
                "from gitgud.skills.util import Skill\n"
                "skill = Skill(",
                "    '{}',".format(skill_name),
                "    [",
                "    ]",
                ")\n",
                ])
            fp.write(level_setup)
    
        
        # Read file
        with open(os.path.join(os.path.join("gitgud","skills"),"__init__.py"), 'r') as fp:
            filedata = fp.read()

        # Add import statement
        replace = "from gitgud.skills.{0} import skill as {0}_skill\n\nfrom gitgud.skills.u".format(skill_name)
        filedata = filedata.replace("\nfrom gitgud.skills.u", replace)
        
        # Add to input array of Skill
        replace = ",\n    {}_skill\n]".format(skill_name)
        filedata = filedata.replace("\n]", replace)

        # Write to file
        filepath = os.path.join(os.path.join("gitgud","skills"),"__init__.py")
        with open(filepath, 'w') as fp:
            fp.write(filedata)
            print("Modified: Added skill to {}".format(filepath))
        
        write_init(skill_name, skill_path, level_name)
        return
    else:
        # Populate file with BasicLevel
        with open(os.path.join(skill_path,"__init__.py"), 'r') as fp:
            filedata = fp.read()

        replace = ",\n        BasicLevel('{0}', pkg_resources.resource_filename(__name__, '_{0}/'))\n    ]".format(level_name)
        filedata = filedata.replace("\n    ]", replace)
        filedata = filedata.replace("[,","[")
        
        filepath = os.path.join(skill_path,"__init__.py")
        with open(filepath, 'w') as fp:
            fp.write(filedata)
            print("Modified: Added level to {}".format(filepath))
    return

def create_file(level_path,filename):
    with open(os.path.join(level_path,filename),'a+'):
        pass
    print("Created: {}".format(filename))
    return

def main():
    # Obtain input arguments
    skill_name = sys.argv[1]
    level_name = sys.argv[2]
    
    # Check if cwd is gitgud folder
    if os.path.isdir(os.path.join(cwd, 'gitgud')):
            # Confirm choice to avoid making a mess
            print ("\n".join([
                            "skill_name: {}".format(skill_name),
                            "level_name: {}".format(level_name),
                            "Confirm[y/n] "
                            ]),
                        end = '')
            choice = input().lower()
            if choice == 'n':
                return
            
            print("\nCreating Folders:")
            # Make skill folder
            skill_path = os.path.join("gitgud","skills","{}".format(skill_name))
            if not os.path.exists(skill_path):
                os.mkdir(skill_path)
                print("Created: {}".format(skill_name))
                  
                  
            # Make level folder
            level_path = os.path.join(skill_path,"_{}".format(level_name))
            if not os.path.exists(level_path):
                os.mkdir(level_path)
                print("Created: {}".format(level_name))
            
            print("\nModifying Init Files:")
            write_init(skill_name,skill_path,level_name)
            
            print("\nCreating Files:")
            # Make instruction file
            create_file(level_path, "instructions.txt")
            
            # Make goal file
            create_file(level_path, "goal.txt")

            # Make setup file
            create_file(level_path, "setup.txt")
                
            # Make test file
            create_file(level_path, "test.txt")
    else:
        print("Error: Execute this script in the git-gud directory.")


if __name__ == "__main__":
    main()


