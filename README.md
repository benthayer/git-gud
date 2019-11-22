# Git Gud
## What is it?
Git Gud is a command line tool to help you learn how to use git.
It is structured like a game to make the learning experience more fun.
It contains a series of levels, which are sorted by skills.
If you complete all the levels in a skill, then you've completed the skill.
It's as simple as that. Each skill has a common theme.
The first skill covers the basics and introduces you to a few of the fundamental concepts of git, namely commits, branches, and merging/rebasing. Subsequent skills get more advanced.

The goal is to make this project contributor-friendly and to have levels covering every git skill.
If there's something Git Gud doesn't teach you, we encourage you to open an issue and we'll try to make levels that teach that concept/command.
If you're interested in contributing, the project is intentionally structured in a way that makes it easy for you to get your first pull request.
Don't forget, the best way to learn about Git (or anything) is to actually use it! For more information, check out the [contributors file](https://github.com/bthayer2365/git-gud/blob/master/CONTRIBUTING.md).

There is also another project we recommend trying out.
It is called ["Learn Git Branching"](https://learngitbranching.js.org), and it can teach you some of the things Git Gud teaches, and with a nice visual interface.
Git Gud differentiates itself by (eventually) having more skills and the ability to test you on all the concepts there are.

## How do I use it?
First, no matter what, you'll need Python 3.
We'll use python to install Git Gud.
Depending on which way you want to install, we'll either do a "User install" by downloading the `git-gud` package from PyPi, which is handled by pip, or we'll do an edit-mode (development) install, which also uses pip, but in a different way.
Once it's installed, we make an empty directory and switch into it. We need to do this because Git Gud acts as if we're in a git repository and modifies the files to set up different "levels".
If we were in another directory, it would delete all our files! But don't worry, there's a built in failsafe, so Git Gud will warn us before it does anything like that.

Recap:

1. Make sure we're using Python 3
2. Install Git Gud
3. Create and change into an empty directory for Git Gud to load the skills into
4. Run `git gud init`
5. Follow the instructions to git gud!

For specific instructions, see below.

### User install:
Use this method if all you're looking to do is to use Git Gud.
Open up a command line and type the following in.
```
python --version # Must say Python 3, any minor version
python -m  pip install git-gud
mkdir test
cd test
git gud init # Initializes a git repository and lets us start using git gud from within this folder
```

### Development install:  
Use this method if you'd like to contribute to this repository.  
Open up a command line and type the following in. Make sure you're in the directory you want your local copy of Git Gud to be in.
```
git clone https://github.com/bthayer2365/git-gud
cd git-gud
python --version # Must say Python 3, any minor version
python -m pip install -e . # Installs in edit mode so we can change files without needing to reinstall
cd ..
mkdir test
cd test
git gud init # Initializes a git repository and lets us start using git gud from within this folder
```

Once it's installed, you can access all the features that Git Gud has to offer.
If you just want to get started, type in `git gud instructions`.
The first skill is already loaded for you, and all you just have to do is follow the instructions and it'll guide you through the levels.
Once you think you're done with a skill, run `git gud test` to see of you've completed the level.
If you've solved it, run `git gud progress` to move on to the next level! Look at the full command list below for a complete command list.

There will be several levels within each skill. Complete all of them to complete the skill, or feel free to skip ahead!


### Full command list
Some commands you'll want to learn and what they do:
* python -m gitgud start 
  * Creates a git repository and gets you started on the first level!
  * Lets you use `git gud <command>` instead of `python -m gitgud <command>`
* git gud status
  * Shows the level you are currently working on
* git gud instructions
  * This the very helpful command that will make you git gud! It displays the instructions for the current level, which will show you how to commit, branch and everything else!
* git gud reset
  * Will reset the current level in case you mess up
* git gud test
  * Tests to see if the current level is complete. If it congratulates you, you've successfully completed the level and you can move on! (You can also move on anyways)
* git gud progress
  * Takes you to the next level
* git gud skills
  * Displays all skills
* git gud levels
  * Displays all levels in the current skill
* git gud levels <skill_name>
  * Displays all levels in the specified skill
* git gud load <skill_name>
  * Begin the first level of the specified skill
* git gud load -<level_name>
  * Begin the specified level of the current skill
* git gud load <skill_name> <level_name>
  * Begin the specified level (specifying the level is optional)
  * A hyphen can be used instead of a space between <skill_name> and <level_name> (specifying the skill is optional)
* git gud commit
  * Commit an empty file with a unique name
* git gud commit <commit_name>
  * Commit an empty file with the specified name
* git gud goal
  * Concisely prints out what is needed to complete the level
* git gud show-tree
  * Visualizes the current git tree
