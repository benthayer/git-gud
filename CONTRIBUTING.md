## So, you want to be a contributor?
You're in luck! 
Git Gud was intentionally designed to make it easy for you to contribute! 
If the only thing you want to do is to make a level that tests to see if you can modify the tree in a simple way, then there's already the `BasicLevel` class to deal with that.
If you want to do something more complicated, just throw out the idea.
The easiest way to contribute is to open up an issue.
Even though you're not writing code, GitHub still counts issues as contributions!

Once you write your first issue, I'll respond and we can figure out how to design a skill, add your feature, or fix your problem.
If you want to end it there, you can, but I encourage you to continue. 
A Pull Request might just be a couple lines of code away, and I'll be happy to help you through any issues you encounter!  

If you feel like your issue is too complicated for you to solve, but you'd still like to write code, just say so. 
I can point you towards the files you need or other code that does something similar. 
If you're still not sure, then I'm happy to write some code to get you started.

Remember: Everyone, including me, was a noob at some point. 
Don't be worried about wasting my time because you're not. 
Contributing is called contributing because it is exactly that. 
Any code you write makes the project more complete and any issues you submit opens up the opportunity for others to contribute and to make the project better. 
I started this project because I wanted to help people learn git and programming. 
I am committed to that goal and more than happy to help to you learn to code and to submit a pull request.

## Download and Setup
```
git clone https://github.com/bthayer2365/git-gud
cd git-gud
pip install -e . # Installs in edit mode so we can change files without needing to reinstall
cd ..
mkdir test
cd test
git gud init # Initializes a git repository and lets us start using the git gud command from within this folder
```
Once you have the code downloaded, I would recommend having two terminals open at all times, one in the test directory you just created, and one in the git-gud directory. 
This allows you to both work with your code and test your code at the same time.

## Project Layout
#### `GitPython`
It's important to know that when you run `import git`, you're not actually importing git itself, you're importing Git Python, a library built to provide a way to access git from within Python. 
If you're writing something advanced, chances are you'll have to interact with that library. 
The project is located [here](https://github.com/gitpython-developers/GitPython) and the project's documentation can be found [here](https://gitpython.readthedocs.io/en/stable/).
#### The `gitgud` module
Git Gud is written in Python and structured like a Python module.
Python modules can be run and provide a good amount of flexibility. 
Python also comes with PyPi, a package manager. 
This makes it easy to install Git Gud, even if you aren't the most technical. 

In our case, `gitgud` is a Python module because it is simply a folder with an `__init__.py` file. 
A module is anything that can be imported by using Python's `import X` syntax. 
There are also modules within the `gitgud` module. 
Folders with an `__init__.py` file and standalone Python files can both be modules. 
The `gitgud` module also has modules inside it. 
These "sub-modules" can be imported by running `import gitgud.X` and come in both types: files and folders. 
Because `gitgud` has sub-modules, it's known as as a package, and therefore can be installed with the `pip` package manager.

#### The `git gud` alias
This project is not actually affiliated with Git, although we're able to run as a Git subcommand by creating what's known as an  alias within Git. 
If you were to do this from the command line, the command to run would be `git config --global alias.gud " ! python -m gitgud"`. 
This goes into the repository's `.git/` folder and finds the `.git/config` file. 
In that file, there's a section called "[alias]" that is created and lists our command as `gud = "! C:/path/to/python.exe -m gitgud"` on Windows or `gud = "! /path/to/python -m gitgud"` on Mac/Linux

#### `__main__.py`
As with any program, it starts with `main`. 
In our case, `main` is `gitgud\__main__.py`. 
When you run `python -m gitgud`, Python looks for a file that it can run. 
Specifically, it looks for `__main__.py`. 
If `__main__.py` isn't present, then Python can't run the module as if it were a command. 
Instead, it'll think of `gitgud` exclusively as a package that can be imported.

`gitgud\__main__.py` contains the `GitGud` class, which is loaded up with an argument parser and a bunch of methods to handle the different commands that Git Gud can be given. 
The argument parser is defined in `.__init__()`. 
It sets up all the commands that Git Gud is capable of handling, along with any sub-commands and additional arguments.
The parser is run using `.parse()`. 
The method will look for the command that was sent in and direct it to the appropriate handler. 
Each command has its own handler, and the handlers will process the arguments and perform the appropriate tasks.

#### Skills
Every skill in Git Gud exists as a Python module.
If I wanted to import the "basis" skill, I use `import gitgud.skills.basics`.
Each skill module exists to organize the levels within that skill.
The skill is always a folder with an `__init__.py` file so that it can organize the code to run the levels.
Levels can either be their own folder or their own python file, but they must follow the rule that the folder/file must be named `_level/` or `_level.py`.
This is Python's way of saying that those are meant to be used by the skill module only and aren't supposed to be imported by another package.

We access the levels through the skills module.
If you take a look in a skills' `__init__.py`, you'll see where all the levels are defined.
The code is fairly simple and is meant to be that way. 
All you are meant to do is instantiate the objects that you define elsewhere. 
For many of the levels, this is `gitgud.skills.util.BasicLevel`, and all that is needed is to supply the name of the subfolder.
Beyond that, you are simply creating an ordered dictionary to keep track of all the skills you've created and deleting everything other than the `all_levels` object.

The skills themselves are collected and given names through `gitgud/skills/__init__.py`
It is roughly the same procedure and a `Skill` object is simply instantiated with its' name and the levels that are part of that skill.

#### Levels
It should be noted that there currently isn't an example for a level that uses the `_level.py` system, but you should know that it is still possible.
`_level.py` should contain a class that extends `gitgud.skills.util.Level`, just as `gitgud.skills.util.BasicLevel` does.
The class you create should then be imported into `__init__.py` and instantiated with the proper information, including the name that you gave it.

Currently, the majority of levels are constructed using `gitgud.skills.util.BasicLevel`.
This is because  many of the levels are simple enough that they fall into the common structure of starting with a bunch of commits in a certain order and then in some way modifying the branches and ordering of those commits, or creating new ones.
If you're making your own level, you may want to consider using this class.

#### `.spec` files
`.spec` files are something I created in order to more easily specify a git tree. 
They exist to make creating a new skill extremely easy.
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
If you're looking for more details, check out the other spec files and `parse_spec` in `gitgud/skills/util.py`

#### `CONTRIBUTING.md`
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
I'm excited to get any contributions and look forward to seeing your code integrated into my repo and published on PyPi! 
Good luck!
