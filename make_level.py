import sys
import os
from shutil import copyfile

cwd = os.getcwd()

def register_skill_package(skill_name):
    # Read setup.py
    with open("setup.py", 'r') as fp:
        filedata = fp.read()

    # Register skill if not already registered.
    if not "gitgud.skills.{}".format(skill_name) in filedata:
        # Package
        replace1 = "\n".join([
            "        \'gitgud.skills.{}\',".format(skill_name),
            "    ],",
            "    package_data"
        ])

        # Data files
        replace2 = "\n".join([
            "        \'gitgud.skills.{}\': ['_*/*'],".format(skill_name),
            "    },",
            "    python_requires"
        ])

        # Register new skill to setup.py
        filedata = filedata.replace("\n".join([
            "    ],",
            "    package_data"
        ]), replace1)

        filedata = filedata.replace("\n".join([
            "    },",
            "    python_requires"
        ]), replace2)

        # Write new lines to file
        with open("setup.py", 'w') as fp:
            fp.write(filedata)
            print("Registered.".format(skill_name))
            print()


def make_folders(skill_name, level_name):
    # Make skill folder
    skill_path = os.path.join("gitgud", "skills", "{}".format(skill_name))
    if not os.path.exists(skill_path):
        os.mkdir(skill_path)
        print("Created: {}".format(skill_path))
    else:
        print("Exists: {}".format(skill_path))

    # Make level folder
    level_path = os.path.join(skill_path, "_{}".format(level_name))
    if not os.path.exists(level_path):
        os.mkdir(level_path)
        print("Created: {}".format(level_path))
    else:
        print("Exists: {}".format(level_path))

    return skill_path, level_path


def write_init(skill_name, skill_path, level_name):
    # If skills/<new_skill>/__init__.py doesn't exist, create a basic version
    if not os.path.exists(os.path.join(skill_path, "__init__.py")):
        copyfile("level_file_templates/__init__.py", skill_path + "/__init__.py")
        with open(os.path.join(skill_path, "__init__.py"), 'r') as fp:
            level_setup = fp.read()
            
        level_setup = level_setup.replace("{}", skill_name)
        
        with open(os.path.join(skill_path, "__init__.py"), 'w') as fp:
            fp.write(level_setup)

        # Read skills/__init__.py to add import statement, and add new skill to AllSkills
        with open(os.path.join("gitgud", "skills", "__init__.py"), 'r') as fp:
            filedata = fp.read()

        # Add import statement into skills/__init__.py
        new_import = "\n".join([
            "from gitgud.skills.{0} import skill as {0}_skill".format(skill_name),
            "",
            "from gitgud.skills.util import AllSkills"
        ])
        filedata = filedata.replace("\nfrom gitgud.skills.util import AllSkills", new_import)

        # Add skill to AllSkills
        replace = ",\n    {}_skill\n]".format(skill_name)
        filedata = filedata.replace("\n]", replace)

        # Write to file
        filepath = os.path.join("gitgud", "skills", "__init__.py")
        with open(filepath, 'w') as fp:
            fp.write(filedata)
            print("Registered skill \"{}\" in {}".format(skill_name, filepath))

        write_init(skill_name, skill_path, level_name)
    else:
        # Add level to skills/<new_skill>/__init__.py
        filepath = os.path.join(skill_path, "__init__.py")
        with open(filepath, 'r') as fp:
            filedata = fp.read()

        replace = ",\n        BasicLevel('{level_name}', __name__)\n    ]".format(level_name=level_name)
        filedata = filedata.replace("\n    ]", replace)
        filedata = filedata.replace("[,", "[")

        with open(filepath, 'w') as fp:
            fp.write(filedata)
            print("Registered level \"{}\" in {}".format(level_name, filepath))


def write_test(skill_path, level_name):
    test_levels_path = os.path.join(skill_path, "test_levels.py")
    if not os.path.exists(test_levels_path):
        copyfile("level_file_templates/test_levels.py", test_levels_path)
        with open(test_levels_path, 'r') as fp:
            new_test = fp.read()
            
        new_test = new_test.replace("{}", level_name)
        
        with open(test_levels_path, 'w') as fp:
            fp.write(new_test)
            print("Created file: {}".format(test_levels_path))
            print('Created test case "{}" in {}'.format(level_name, test_levels_path))
    else:
        with open(test_levels_path, 'r') as fp:
            filedata = fp.read()

        replace = "\n".join([
            "    ), (",
            "        skill[\'{}\'], [".format(level_name),
            "            \'git gud commit\',  # Examples, change to solution for your level",
            "            \'git merge example\'",
            "        ]",
            "    )",
            "]"
        ])

        filedata = filedata.replace("\n".join([
            "    )",
            "]"
        ]), replace)

        with open(test_levels_path, 'w') as fp:
            fp.write(filedata)
            print('Created test case "{}" in {}'.format(level_name, test_levels_path))


def create_level_file(level_path, filename):
    filepath = os.path.join(level_path, filename)
    copyfile("level_file_templates/{}".format(filename), "{}".format(filepath))
    print("Created: {}".format(filepath))


def get_new_level_name_from_args():
    num_args = len(sys.argv) - 1
    if num_args == 2:
        skill_name = sys.argv[1]
        level_name = sys.argv[2]
        return skill_name, level_name
    else:
        if num_args > 3:
            error_message = "Too many arguments: "
        else:
            error_message = "Too few arguments: "
        print(error_message + "Takes 2 arguments, but {} was given.".format(num_args))
        print("Usage: \"python make_level.py <skill_name> <level_name>\"")
        exit(1)


def confirm_name(skill_name, level_name):
    # Confirm choice to avoid making a mess
    print("\n".join([
        "skill_name: {}".format(skill_name),
        "level_name: {}".format(level_name),
        "Confirm[y/n] "
    ]), end='')
    
    choice = ''
    while choice != 'y':
        choice = input().lower()
        if choice == 'n':
            print("Aborting, no changes made.")
            exit(1)
        elif choice != 'y':
            print("Confirm[y/n] ", end='')


def main():
    skill_name, level_name = get_new_level_name_from_args()
        
    # Check if current dir isn't ../gitgud directory. (i.e. dir of setup files)
    if not os.path.isdir(os.path.join(cwd, 'gitgud')):
        print("Error: Script must be run in the git-gud directory.")
        exit(1)
    
    confirm_name(skill_name, level_name)
    print()
    
    print("Registering package: {}".format(skill_name))
    register_skill_package(skill_name)
    print()
    
    print("Creating Folders:")
    skill_path, level_path = make_folders(skill_name, level_name)
    print()

    print("Registering Level: {} {}".format(skill_name, level_name))
    write_init(skill_name, skill_path, level_name)
    print()

    print("Creating Test Case:")
    write_test(skill_path, level_name)
    print()

    print("Creating Files:")
    create_level_file(level_path, "instructions.txt")
    create_level_file(level_path, "goal.txt")
    create_level_file(level_path, "setup.spec")
    create_level_file(level_path, "test.spec")
    print()

    print("Done.")


if __name__ == "__main__":
    main()

