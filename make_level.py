import sys
import os
from shutil import copyfile

cwd = os.getcwd()

def write_init(skill_name, skill_path, level_name):
    # If skills/skill/__init__.py doesn't exist, create a basic version (no levels)
    if not os.path.exists(os.path.join(skill_path,"__init__.py")):
        with open(os.path.join(skill_path,"__init__.py"), 'w+') as fp:
            level_setup = "\n".join([
                "import pkg_resources\n",
                "from gitgud.skills.util import BasicLevel",
                "from gitgud.skills.util import Skill",
                "",
                "skill = Skill(",
                "    '{}',".format(skill_name),
                "    [",
                "    ]",
                ")",
                ""
                ])
            fp.write(level_setup)
    
        
        # Read file
        with open(os.path.join("gitgud","skills","__init__.py"), 'r') as fp:
            filedata = fp.read()

        # Add import statement
        replace = "\n".join([
                            "from gitgud.skills.{0} import skill as {0}_skill".format(skill_name),
                            "",
                            "",
                            "from gitgud.skills.u"
                            ])
        filedata = filedata.replace("\nfrom gitgud.skills.u", replace)
        
        # Add to input array of Skill
        replace = ",\n    {}_skill\n]".format(skill_name)
        filedata = filedata.replace("\n]", replace)

        # Write to file
        filepath = os.path.join("gitgud","skills","__init__.py")
        with open(filepath, 'w') as fp:
            fp.write(filedata)
            print("Registered skill \"{}\" in {}".format(skill_name, filepath))
        
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
            print("Registered level \"{}\" in {}".format(level_name, filepath))
    return

def create_level_file(level_path,filename):
    filepath = os.path.join(level_path,filename)
    copyfile("level_file_temp/{}".format(filename), "{}".format(filepath))
    print("Created: {}".format(filepath))

def main():
    # Obtain input arguments
    try:
        skill_name = sys.argv[1]
        level_name = sys.argv[2]
    except:
        print("Usage: \"python make_level.py <skill_name> <level_name>\"")
        return
        
    # Check if current dir isn't ../gitgud directory. (i.e. dir of setup files)
    if not os.path.isdir(os.path.join(cwd, 'gitgud')):
        print("Error: Execute this script in the git-gud directory.")
        return
    
    # Register package
    
    # Read setup.py
    with open("setup.py", 'r') as fp:
        filedata = fp.read()
    
    # Update desired lines
    replace1 = "\n".join([
                          "        \'gitgud.skills.{}\',".format(skill_name),
                          "    ],",
                          "    package_data"
                        ])
    replace2 = "\n".join([
                          "        \'gitgud.skills.{}\': ['_*/*'],".format(skill_name),
                          "    },",
                          "    python_requires"
                        ])
    filedata = filedata.replace("\n".join([
                                           "    ],",
                                           "    package_data"
                                          ])
                                , replace1)
    filedata = filedata.replace("\n".join([
                                           "    },",
                                           "    python_requires"
                                          ])
                                , replace2)
    
    # Write new lines to file
    with open("setup.py",'w') as fp:
        fp.write(filedata)
    
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
            
    print()
    print("Creating Folders:")
    print()
    # Make skill folder
    skill_path = os.path.join("gitgud","skills","{}".format(skill_name))
    if not os.path.exists(skill_path):
        os.mkdir(skill_path)
        print("Created: {}".format(skill_path))
          
          
    # Make level folder
    level_path = os.path.join(skill_path,"_{}".format(level_name))
    if not os.path.exists(level_path):
        os.mkdir(level_path)
        print("Created: {}".format(level_path))
            
    print()
    print("Registering Level: {} {}".format(skill_name, level_name))
    print()
    write_init(skill_name,skill_path,level_name)
            
    print()
    print("Creating Files:")
    print()
    # Make instruction file
    create_level_file(level_path, "instructions.txt")
            
    # Make goal file
    create_level_file(level_path, "goal.txt")

    # Make setup file
    create_level_file(level_path, "setup.spec")
        
    # Make test file
    create_level_file(level_path, "test.spec")
    
    print()
    print("Done.")

if __name__ == "__main__":
    main()


