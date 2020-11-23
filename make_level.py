import sys
from pathlib import Path
from shutil import copyfile


def register_skill_package(skill_name):
    # Read setup.py
    with open("setup.py", 'r') as fp:
        filedata = fp.read()

    # Register skill if not already registered.
    if not "gitgud.skills.{}".format(skill_name) in filedata:
        # Package
        replace1 = "\n".join([
            "        'gitgud.skills.{}',".format(skill_name),
            "    ],",
            "    package_data"
        ])

        # Data files
        replace2 = "\n".join([
            "        'gitgud.skills.{}': ['_*/*'],".format(skill_name),
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

        print('Registered package "{}" in setup.py'.format(skill_name))


def make_folders(level_name, skill_name):
    # Make skill folder
    skill_path = Path.cwd() / "gitgud" / "skills" / skill_name
    if not skill_path.exists():
        skill_path.mkdir()
        print("Created: {}".format(skill_path))
    else:
        print("Exists: {}".format(skill_path))

    # Make level folder
    level_path = skill_path / "_{}".format(level_name)
    if not level_path.exists():
        level_path.mkdir()
        print("Created: {}".format(level_path))
    else:
        print("Exists: {}".format(level_path))

    return level_path, skill_path


def make_skill(skill_name, skill_long_name, skill_path):
    # Fill out template for skills/<skill>/__init__.py
    with open("level_file_templates/__init__.py", 'r') as fp:
        skill_file = fp.read()

    skill_file = skill_file.replace("{name}", skill_name)
    skill_file = skill_file.replace("{long_name}", skill_long_name)

    with open(skill_path / "__init__.py", 'w') as fp:
        fp.write(skill_file)

    # Register skill to skills/__init__.py
    with open(Path.cwd() / "gitgud" / "skills" / "__init__.py", 'r') as fp:
        filedata = fp.read()

    # Add import statement into skills/__init__.py
    new_import = "\n".join([
        "from gitgud.skills.{0} import skill as {0}_skill".format(skill_name),  # noqa: E501
        "",
        "from gitgud.util import AllSkills"
    ])
    filedata = filedata.replace("\nfrom gitgud.util import AllSkills", new_import)  # noqa: E501

    # Add skill to AllSkills
    replace = ",\n    {}_skill\n]".format(skill_name)
    filedata = filedata.replace("\n]", replace)

    # Write to file
    filepath = Path.cwd() / "gitgud" / "skills" / "__init__.py"
    with open(filepath, 'w') as fp:
        fp.write(filedata)

    print('Registered skill "{}" in {}'.format(skill_name, filepath))


def make_level(level_name, level_long_name, skill_name, skill_path):
    # Add level to skills/<new_skill>/__init__.py
    filepath = skill_path / "__init__.py"
    with open(filepath, 'r') as fp:
        filedata = fp.read()

    basic_level_import_string = "from gitgud.util.level_builder import BasicLevel\n"  # noqa: E501
    if basic_level_import_string not in filedata:
        filedata = basic_level_import_string + filedata

    replace = ",\n        BasicLevel('{long_name}', '{name}', __name__)\n    ]".format(name=level_name, long_name=level_long_name)  # noqa: E501
    filedata = filedata.replace("\n    ]", replace)
    filedata = filedata.replace("[,", "[")

    with open(filepath, 'w') as fp:
        fp.write(filedata)

    print("Registered level \"{}\" in {}".format(level_name, filepath))


def write_test(skill_path):
    test_levels_path = skill_path / "test_levels.py"
    if not test_levels_path.exists():
        copyfile("level_file_templates/test_levels.py", test_levels_path)
        print('Created: {}'.format(test_levels_path))
    else:
        print('Exists: {}'.format(test_levels_path))


def create_level_file(level_path, filename):
    filepath = level_path / filename
    copyfile("level_file_templates/{}".format(filename), filepath)
    print("Created: {}".format(filepath))


def get_new_level_name_from_args():
    num_args = len(sys.argv) - 1
    if num_args == 3 or num_args == 4:
        level_name = sys.argv[1]
        level_long_name = sys.argv[2]
        skill_name = sys.argv[3]
        skill_long_name = sys.argv[4] if num_args == 4 else ""
        return level_name, level_long_name, skill_name, skill_long_name
    else:
        if num_args > 4:
            error_message = "Too many arguments: "
        else:
            error_message = "Too few arguments: "
        print(error_message + "Takes 3 or 4 arguments, but {} was given.".format(num_args))  # noqa: E501
        print('Usage: "python make_level.py [-y] <level_name> <level_long_name> <skill_name> [<skill_long_name>]"')  # noqa: E501
        exit(1)


def confirm_name(level_name, level_long_name, skill_name, skill_long_name):
    # Confirm choice to avoid making a mess
    choices = [
        "level_name: {}".format(level_name),
        "Level Name: {}".format(level_long_name),
        "skill_name: {}".format(skill_name) + (
            " (exists)" if skill_long_name is None else ""
        ),
    ]
    if skill_long_name:
        choices.append("Skill Name: {}".format(skill_long_name))

    print("\n".join(choices))
    print("Confirm[y/n] ", end="")

    choice = ''
    while choice != 'y':
        choice = input().lower()
        if choice == 'n':
            print("Aborting, no changes made.")
            exit(1)
        elif choice != 'y':
            print("Confirm[y/n] ", end='')


def get_valid_args():
    if len(sys.argv) != 1 and sys.argv[1] == '-y':
        should_confirm_name = False
        del sys.argv[1]
    else:
        should_confirm_name = True

    level_name, level_long_name, skill_name, skill_long_name = get_new_level_name_from_args()  # noqa: E501

    skill_path = Path.cwd() / "gitgud" / "skills" / skill_name

    # Check if current dir isn't ../gitgud directory. (i.e. dir of setup files)
    if not (Path.cwd() / 'gitgud').is_dir():
        print("Error: Script must be run in the git-gud directory.")
        exit(1)
    elif not level_long_name:
        print("Error: Level's long name must be specified in order to register a level.")  # noqa: E501
        exit(1)

    skill_already_exists = (skill_path / "__init__.py").exists()  # noqa: E501
    if not skill_already_exists and not skill_long_name:  # noqa: E501
        print("Error: Skill's long name must be specified if skill doesn't already exist.")  # noqa: E501
        exit(1)

    if should_confirm_name:
        confirm_name(
            level_name,
            level_long_name,
            skill_name,
            skill_long_name if skill_already_exists else None
        )
    print()

    return level_name, level_long_name, skill_name, skill_long_name


def main():
    level_name, level_long_name, skill_name, skill_long_name = get_valid_args()

    print("Registering package: {}".format(skill_name))
    register_skill_package(skill_name)
    print()

    print("Creating Folders:")
    level_path, skill_path = make_folders(level_name, skill_name)
    print()

    if skill_long_name:
        print("Registering Skill:")
        make_skill(skill_name, skill_long_name, skill_path)
        print()

    print("Registering Level:")
    make_level(level_name, level_long_name, skill_name, skill_path)
    print()

    print("Creating Test Case:")
    write_test(skill_path)
    print()

    print("Creating Files:")
    create_level_file(level_path, "explanation.txt")
    create_level_file(level_path, "goal.txt")
    create_level_file(level_path, "setup.spec")
    create_level_file(level_path, "test.spec")
    create_level_file(level_path, "details.yaml")
    create_level_file(level_path, "filename.txt")
    create_level_file(level_path, "solution.txt")
    print()

    print("Done.")


if __name__ == "__main__":
    main()
