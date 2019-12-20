import sys
import os
from shutil import copyfile

cwd = os.getcwd()


def write_init(skill_name, skill_path, level_name):
    # If skills/<new_skill>/__init__.py doesn't exist, create a basic version
    if not os.path.exists(os.path.join(skill_path, "__init__.py")):
        copyfile("ML_file_templates/__init__.py", skill_path + "/__init__.py")
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

        replace = ",\n        BasicLevel('{level_name}', pkg_resources.resource_filename(__name__, '_{level_name}/'))\n    ]".format(level_name=level_name)
        filedata = filedata.replace("\n    ]", replace)
        filedata = filedata.replace("[,", "[")

        with open(filepath, 'w') as fp:
            fp.write(filedata)
            print("Registered level \"{}\" in {}".format(level_name, filepath))


def write_test(skill_name, skill_path, level_name, level_path):
    if not os.path.exists(os.path.join(skill_path, "test_levels.py")):
        copyfile("ML_file_templates/test_levels.py", skill_path + "/test_levels.py")
        with open(os.path.join(skill_path, "test_levels.py"), 'r') as fp:
            new_test = fp.read()
            
        new_test = new_test.replace("skill[]", "skill['" + level_name + "']")
        
        with open(os.path.join(skill_path, "test_levels.py"), 'w') as fp:
            fp.write(new_test)
            print("Added entry for {}".format(level_path))
    else:
        with open(os.path.join(skill_path, "test_levels.py"), 'r') as fp:
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

        with open(os.path.join(skill_path, "test_levels.py"), 'w') as fp:
            fp.write(filedata)
            print("Added entry for {}".format(level_name))


def create_level_file(level_path, filename):
    filepath = os.path.join(level_path, filename)
    copyfile("ML_file_templates/{}".format(filename), "{}".format(filepath))
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
            return
        elif choice != 'y':
            print("Confirm[y/n] ", end='')

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
    ]), replace1)

    filedata = filedata.replace("\n".join([
        "    },",
        "    python_requires"
    ]), replace2)

    # Write new lines to file
    with open("setup.py", 'w') as fp:
        fp.write(filedata)
        print()
        print("Registered Package: {}".format(skill_name))
        print()

    print("Creating Folders:")
    # Make skill folder
    skill_path = os.path.join("gitgud", "skills", "{}".format(skill_name))
    if not os.path.exists(skill_path):
        os.mkdir(skill_path)
        print("Created: {}".format(skill_path))

    # Make level folder
    level_path = os.path.join(skill_path, "_{}".format(level_name))
    if not os.path.exists(level_path):
        os.mkdir(level_path)
        print("Created: {}".format(level_path))

    print()
    print("Registering Level: {} {}".format(skill_name, level_name))
    write_init(skill_name, skill_path, level_name)

    print()
    print("Creating Test Cases:")
    write_test(skill_name, skill_path, level_name, level_path)

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
