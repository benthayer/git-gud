import subprocess

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


def all_levels_complete():
    print("Wow! You've complete every level, congratulations!")

    print("If you want to keep learning git, why not try contributing"
          " to git-gud by forking the project at https://github.com/benthayer/git-gud/")

    print("We're always looking for contributions and are more than"
          " happy to accept both pull requests and suggestions!")

def default_fail():
    print('Level not complete, keep trying. "git gud reset" to start from scratch.')
