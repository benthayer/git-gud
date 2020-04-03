import subprocess

user_has_seen_messages = False

def separated(func):
    def new_func(*args, **kwargs):
        if user_has_seen_message:
            print()
            user_has_seen_message = True

        func(*args, **kwargs)
    return new_func

def print_user_message(message):
    print(message)


def show_level_name(level):
    print('Level: "{}"'.format(level.full_name()))


def print_goal(level):
    print(level.goal_str())


def simulate_goal(level):
    print("Simulating: git gud goal")
    level.goal()


def show_tree():
    print("Simulating: git log --graph --oneline --all ")
    subprocess.call(["git", "log", "--graph", "--oneline", "--all"])


def help():
    print("Type \"git gud instructions\" to view full instructions")
    print("Type \"git gud test\" to test for level completion")
    print("Type \"git gud help\" for more help")


def level_complete(level):
    print('Level complete! "git gud load next" to advance to the next level')
    print('Next level is: {}'.format(level.next_level.full_name()))


def skill_complete(level):
    print("Level complete, you've completed all levels in this skill!")
    print('"git gud load next" to advance to the next skill')
    print("Next skill is: {}".format(level.next_level.skill.name))


def all_levels_complete():
    print("Wow! You've complete every level, congratulations!")

    print("If you want to keep learning git, why not try contributing"
          " to git-gud by forking the project at https://github.com/benthayer/git-gud/")

    print("We're always looking for contributions and are more than"
          " happy to accept both pull requests and suggestions!")

def default_fail():
    print('Level not complete, keep trying. "git gud reset" to start from scratch.')

