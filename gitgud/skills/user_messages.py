import subprocess

user_has_seen_messages = False


def start_marker():
    return '<' * 7


def end_marker():
    return '=' * 7


def separated(func):
    def new_func(*args, **kwargs):
        global user_has_seen_messages
        if user_has_seen_messages:
            print()
        else:
            user_has_seen_messages = True
        func(*args, **kwargs)
    return new_func


@separated
def print_user_file(path):
    print(path.read_text().strip())


@separated
def print_user_message(message):
    print(message)


@separated
def show_level_name(level):
    print('Level: "{}"'.format(level.full_name()))


def print_info(message):
    print("[INFO]: {}".format(message))


def mock_simulate(command):
    print(end_marker(), "Simulating: {}".format(command))


@separated
def simulate_command(command):
    print(start_marker(), "Simulating: {}".format(command))
    subprocess.call(command, shell=True)
    print(end_marker())


def show_tree():
    simulate_command("git log --graph --oneline --all")


@separated
def help():
    print("Type \"git gud instructions\" to view full instructions")
    print("Type \"git gud test\" to test for level completion")
    print("Type \"git gud help\" for more help")


@separated
def level_complete(level):
    print('Level complete! "git gud load next" to advance to the next level')
    print('Next level is: {}'.format(level.next_level.full_name()))


@separated
def skill_complete(level):
    print("Level complete, you've completed all levels in this skill!")
    print('"git gud load next" to advance to the next skill')
    print("Next skill is: {}".format(level.next_level.skill.name))


@separated
def all_levels_complete():
    print("Wow! You've complete every level, congratulations!")

    print("If you want to keep learning git, why not try contributing"
          " to git-gud by forking the project at "
          "https://github.com/benthayer/git-gud/")

    print("We're always looking for contributions and are more than"
          " happy to accept both pull requests and suggestions!")


@separated
def default_fail():
    print('Level not complete, keep trying. "git gud reset" to start from scratch.')  # noqa: E501


def handle_solution_confirmation(level):
    print('Are you sure you want to view the solution for "{}": "{}"?'.format(level.name, level.skill.name))  # noqa: E501
    print('If so, run `git gud solution --confirm`')


def no_solutions_available():
    print("No solutions available for this level.")


def solution_print_header(level):
    print('Solution for the current level "{}" in the skill "{}":'.format(level.name, level.skill.name))  # noqa: E501


@separated
def default_fail_no_reset():
    print('Level not complete, keep trying.')


def skills_levels_tree(focus_level, all_skills, short=False, display_focus_only=False, display_levels=True, display_other_skills=False):
    middle_entry_bookend = '├── '
    last_entry_bookend = '└── '
    root_skill = focus_level.skill if focus_level else None
    if display_focus_only or not display_other_skills and root_skill is not None:
        skills_to_show = [root_skill]
    else:
        skills_to_show = [skill for skill in all_skills]
    for skill in skills_to_show:
        skill_index = all_skills.get_index(skill.name)
        print("{}. {}".format(skill_index, skill.name if short else skill.readable_name))
        if display_focus_only and focus_level is not None:
            print("{}{}. {}".format(
                    last_entry_bookend, 
                    skill.get_index(focus_level.name), 
                    focus_level.name if short else focus_level.readable_name
                )
            )
            break
        if display_levels:
            for level in skill:
                skill_length = str(len(skill))
                level_index = skill.get_index(level.name)
                print("{}{}. {}".format(
                        middle_entry_bookend if level_index != skill_length else last_entry_bookend,
                        level_index,
                        level.name if short else level.readable_name
                    )
                )
