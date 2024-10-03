import subprocess

from gitgud.util import level_builder
from gitgud.util import Skill

user_has_seen_messages = False


def bool_to_word(condition):
    if condition:
        return "Yes"
    else:
        return "No"


def existence_str(condition):
    if condition:
        return "Exists"
    else:
        return "Doesn't exist"


def start_marker():
    return '<' * 7


def end_marker():
    return '=' * 7


def separated(func):
    def new_func(*args, **kwargs):
        global user_has_seen_messages
        if 'separated' in kwargs and not kwargs['separated']:
            del kwargs['separated']
            func(*args, **kwargs)
        else:
            if user_has_seen_messages:
                print()
            else:
                user_has_seen_messages = True
            func(*args, **kwargs)
    return new_func


@separated
def cat_file(path):
    text = path.read_text().strip()

    for line in text.split('\n'):
        if line[:3] == '>>>':
            command = line[3:].strip()
            simulate_command(command, separated=False)
        else:
            print(line)


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


@separated
def force_initializing():
    print('Force initializing Git Gud.')


@separated
def cant_init_repo_not_empty():
    print('Current directory is nonempty. Initializing will delete all files.')  # noqa: E501
    print('Use "git gud init --force --prettyplease" to delete all files and initialize')  # noqa: E501


@separated
def deleting_and_initializing():
    print('Deleting all files.')
    print('Initializing Git Gud.')


def show_tree():
    simulate_command("git log --graph --oneline --all")


@separated
def help():
    print("Type \"git gud explain\" for an explanation of the level")
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


def rerun_with_confirm_for_solution(level):
    print('Are you sure you want to view the solution for "{}": "{}"?'.format(level.name, level.skill.name))  # noqa: E501
    print('If so, run "git gud solution --confirm"')


@separated
def handle_load_confirm():
    print("You haven't completed this level yet!")
    print('Run "git gud load next --force" to load the next level.')


def no_solutions_available():
    print("No solutions available for this level.")


@separated
def default_fail_no_reset():
    print('Level not complete, keep trying.')


def show_skill_tree(items, include_progress, show_human_names=True, show_code_names=True, expand_skills=False):  # noqa: E501
    middle_entry_bookend = '├──'
    last_entry_bookend = '└──'

    completion = {
        "unvisited": ' ',
        "visited": 'X',
        "partial": 'P',
        "complete": 'O'
    }

    format_string = "{index}. "
    if show_human_names and not show_code_names:
        format_string += "{name}"
    elif show_code_names and not show_human_names:
        format_string += "{code}"
    else:
        format_string += "{name} ({code})"

    def display_entry(index, human_name, code_name, indent):
        print(indent + format_string.format(
            index=index, name=human_name, code=code_name))

    if expand_skills:
        new_items = []
        for skill in items:
            assert isinstance(skill, Skill)
            new_items.append(skill)
            for level in skill:
                new_items.append(level)

        items = new_items

    for i, item in enumerate(items):
        if isinstance(item, Skill):
            display_entry(
                item.all_skills.index(item.name),
                human_name=item.readable_name,
                code_name=item.name,
                indent=""
            )
        else:
            assert isinstance(item, level_builder.Level)
            if i + 1 == len(items) or isinstance(items[i+1], Skill):
                indent = last_entry_bookend
            else:
                indent = middle_entry_bookend

            if include_progress:
                indent += completion[item.get_progress()]
            indent += " "

            display_entry(
                item.skill.index(item.name),
                human_name=item.readable_name,
                code_name=item.name,
                indent=indent
            )


def display_tree_content(header, content, content_order=None, show_content=True, num_files=2): # noqa E501
    if not content_order:
        content_order = list(content.keys())

    # Include all content, even if it's not in content_order
    for key in content:
        if key not in content_order:
            content_order.append(key)

    # Display info for at least num_files
    if len(content_order) < num_files:
        content_order += [None] * (num_files - len(content_order))

    print(header)
    for file_number, filepath in enumerate(content_order):
        file_name = f"File {file_number + 1}"

        if filepath in content:
            if show_content:
                file_name = filepath
                file_details = content[filepath]
            else:
                file_details = filepath
        else:
            file_details = existence_str(False)

        print("  {name}: {details}".format(
            name=file_name,
            details=file_details
        ))
