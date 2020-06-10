## So, you want to be a contributor?
You're in luck! 
Git Gud was intentionally designed to make it easy for you to contribute! If you have an idea or an issue, add an issue and we can get to work.

If you want to get to work on a level, take a look at the existing levels and you should get a feel for how we create levels.

## Download and Setup
```
git clone https://github.com/benthayer/git-gud
cd git-gud
pip3 install -e . # Installs in edit mode so we can change files without needing to reinstall
cd ..
mkdir test
cd test
git gud init # Initializes a git repository and lets us start using the git gud command from within this folder
```
Once you have the code downloaded, I would recommend having two terminals open at all times, one in the test directory you just created, and one in the git-gud directory. 
This allows you to both work with your code and test your code at the same time.

## Testing (pytest)
Our tests make sure that each of the levels can be properly solved and that various other things work as expected.
If you're fixing a bug, you should probably add a test that fails if that bug is present.
#### To run tests:
Please make sure you are running tests for the gitgud subdirectory
```
pytest gitgud
```
or
```
cd gitgud
pytest .
```
Pytest will search for files that start with `test_` and will run methods starting with `test_` as tests.The search ir run for all subdirectories, so all tests defined will automatically be found and don't need to be registered.

#### CircleCI
Once you push and make a pull request, CircleCI will run tests and will show the results directly on GitHub. 
Sometimes tests will pass locally but fail on CircleCI, if that happens, either try to resolve the issue yourself or tag @benthayer for help.

## Project Layout
### `GitPython`
It's important to know that when you run `import git`, you're not actually importing git itself, you're importing Git Python, a library built to provide a way to access git from within Python. 
If you're writing something advanced, chances are you'll have to interact with that library. 
The project is located [here](https://github.com/gitpython-developers/GitPython) and the project's documentation can be found [here](https://gitpython.readthedocs.io/en/stable/).
### The `gitgud` module
Git Gud is written in Python and structured like a Python module.
Python modules can be run and provide a good amount of flexibility. 
Python also comes with PyPI, a package manager. 
This makes it easy to install Git Gud, even if you aren't the most technical. 

In our case, `gitgud` is a Python module because it is simply a folder with an `__init__.py` file. 
A module is anything that can be imported by using Python's `import X` syntax. 
There are also modules within the `gitgud` module. 
Folders with an `__init__.py` file and standalone Python files can both be modules. 
The `gitgud` module also has modules inside it. 
These "sub-modules" can be imported by running `import gitgud.X` and come in both types: files and folders. 
Because `gitgud` has sub-modules, it's known as as a package, and therefore can be installed with the `pip` package manager.

### The `git-gud` entrypoint
This project is not affiliated with Git, although we're able to run as a Git subcommand by adding an entrypoint that Git will be able to look for an run.
When installing Git Gud, it creates an executable called `git-gud` in Python's bin folder that can be run directly by typing in `git-gud`.
Because of the name, you can also type in `git gud` and Git will be able to find the executable and act as if Git Gud is a valid Git subcommand.
The entrypoint is defined in `setup.py` and specifies a function for Python to run.
The function we specify "is" the program.
It is defined in `gitgud/__main__.py`

### `__main__.py`
As with any program, it starts with `main`. 
In our case, `main` is `gitgud\__main__.py`. 
When you run `python3 -m gitgud`, Python looks for a file that it can run. 
Specifically, it looks for `__main__.py`. 
If `__main__.py` isn't present, then Python can't run the module as if it were a command. 
Instead, it'll think of `gitgud` exclusively as a package that can be imported.

`gitgud\__main__.py` contains the `GitGud` class, which is loaded up with an argument parser and a bunch of methods to handle the different commands that Git Gud can be given. 
The argument parser is defined in `.__init__()`. 
It sets up all the commands that Git Gud is capable of handling, along with any sub-commands and additional arguments.
The parser is run using `.parse()`. 
The method will look for the command that was sent in and direct it to the appropriate handler. 
Each command has its own handler, and the handlers will process the arguments and perform the appropriate tasks.

### Making a new level
Each level belongs to a skill, so you need to specify a skill name and a level name. 
In each skill, there is a file called `__init__.py` which instantiates the skill and registers its levels.

If your file needs files, you should place them in their own directory within the appropriate skill folder. For example, the level files for `intro branching` are placed in `skills/intro/_branching/`

#### BasicLevel
Currently, most levels are subclasses of `gitgud.skills.level_builder.BasicLevel`.
`BasicLevel` has a bunch of automatic behavior to help set up and test levels via `.spec` files (see below).
It also implements some generic output.

To make a custom level, you can extend `level_builder.BasicLevel` or you can extend `level_builder.Level`.
There are examples in various skills already, in their `__init__.py` files.
If you want to get more complicated and you're not sure what to do, add an issue or comment on a pull request or existin issue.


#### Creating a skill/level with `make_level.py`

`make_level.py` is a useful script that can help you make a new level without forgetting to do anything. 

The usage of the script is as follows: "python3 make_level.py <skill_name> <level_name>". 

The script will register the new skill/level to `setup.py`, the `__init__.py` for the skill it is in.
It creates `__init__.py` if it doesn't already exist. 
Additionally, it will create tubehe skill/level directory and template files.
The logging of the script should be helpful.

The template files are:
 - skills/test_levels.py
 - skills/<skill_name>/<level_name>/goal.txt
 - skills/<skill_name>/<level_name>/instructions.txt
 - skills/<skill_name>/<level_name>/setup.spec
 - skills/<skill_name>/<level_name>/test.spec
 
_The script overwrites existing files, so be careful_

See other levels for examples of what to do.

#### `.spec` files
`.spec` files are something I created in order to specify a git tree. 
The format is a list of commits. 
Each commit is assigned a number that corresponds to an empty file that is created and committed when setting up a skill.
If it's a merge commit, it's denoted by an "M" followed by a number. 
We do this because no files are created during a merge, and we want the file numbers to be sequential. 
Each line follows this format: `commit_name : parent1 parent2... (branch1, branch2..., tag:tag1, tag:tag2...)`. 
Several parts can be left out though. 
For example, many lines only have `commit_name` present. 
In this case, the parser knows that the previous commit is the parent and that there are no branches/tags that point to that commit. 
In the case of branches, the first commit on a branch will have a parent that is not the previous commit. 
Instead, you'll need to include the colon and specify the parent commit. 
Likewise, if a branch head or a tag points to a commit, then we must include the parenthesis, otherwise, we can leave it out. 
The most complete example of a spec file is `gitgud/skills/extras/_octopus/test.spec`.
If you're looking for more details, check out the other spec files and `parse_spec` in `gitgud/skills/parsing.py`

## `CONTRIBUTING.md`
The purpose of `CONTRIBUTING.md` is to serve as a starting point for new developers. 
It exists mainly to cover the "why", not the "what". 
To see the specifics of how to implement something, you're encouraged to look through the source code and see for yourself what everything does. 
If something isn't self-explanatory, comment on whatever issue you're working on or post a new issue.
I'll be happy to respond there and to update this document. 

## Submitting Your Changes
This project works off of the master branch. 
When working on your own changes, fork this repository, create a branch and submit a pull request from your forks branch to my master branch. 
Give the pull request any name you like and submit it. 
If there's already an open issue for your pull request, link it by including the line `fixes #[issue_id]` in the body of the pull request. 
If you're not sure what to say, don't feel obligated to write more than you think you need to. 
I'll be able to see the code and tell what issue you're trying to solve. 
I'm excited to get any contributions and look forward to seeing your code integrated into my repo and published on PyPI! 
Good luck!
