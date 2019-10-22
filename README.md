# Git Gud
## What is it?
Git Gud is a command line tool to help you learn how to use git. It is intentionally structured like a game to make the learning experience more fun. It contains a series of challenges, which are structured into levels. If you complete all the challenges in a level, then you've completed the level. It's as simple as that. Each level has a common theme. The first level is called `intro` and it'll introduce you to the fundamental concepts of git. The first four challenges are called `commits`, `branching`, `merging`, and `rebasing`.

The goal is to make this project contributor-friendly and to support many different levels. The more, the better. We want you to be able to learn everything you'll ever need to know by using Git Gud. If there's something Git Gud doesn't teach you, we encourage you to open an issue and we'll try to make a level that teaches that concept/command. If you're interested in contributing, the project is intentionally structured in a way that makes it easy for you to get your first pull request. Don't forget, the best way to learn about Git (or anything) is to actually use it! For more information, check out the [contributors file](https://github.com/bthayer2365/git-gud/blob/master/CONTRIBUTING.md). 

There is also another project we recommend trying out. It is called ["Learn Git Branching"](https://learngitbranching.js.org), and it can teach you some of the things Git Gud teaches, and with a nice visual interface. Git Gud differentiates itself by (eventually) having more levels and the ability to test you on all the concepts there are.

## How do I use it?
First, no matter what, you'll need Python 3. We'll use python to install Git Gud. Depending on which way you want to install, we'll either do a "User install" by downloading the `git-gud` package from PyPi, which is handled by pip, or we'll do an edit-mode (development) install, which also uses pip, but in a different way. Once it's installed, we make an empty directory and switch into it. We need to do this because Git Gud acts as if we're in a git repository and modifies the files to set up different "challenges". If we were in another directory, it would delete all our files! But don't worry, there's a built in failsafe, so Git Gud will warn us before it does anything like that.

Recap:

1. Make sure we're using Python 3
2. Install Git Gud
3. Create and change into an empty directory for Git Gud to load the levels into
4. Run `git gud start`
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
git gud start # Initializes a git repository and lets us start using git gud from within this folder
```

### Development install:  
Use this method if you'd like to contribute to this repository.  
Open up a command line and type the following in. Make sure you're in the directory you want your local copy of Git Gud to be in.
```
git clone https://github.com/bthayer2365/git-gud
cd git-gud
python --version # Must say Python 3, any minor version
python -m pip install -e . # NB: Do not overlook the `.` after the -e option! Installs in edit mode so we can change files without needing to reinstall
cd ..
mkdir test
cd test
git gud start # Initializes a git repository and lets us start using git gud from within this folder
```

Once it's installed, you can access all the features that Git Gud has to offer. If you just want to get started, type in `git gud instructions`. The first level is already loaded for you, and all you just have to do is follow the instructions and it'll guide you through the challenges. Once you think you're done with a level, run `git gud test` to see of you've completed the challenge. If you've solved it, run `git gud load next` to move on to the next challenge! Look at the full command list below for a complete command list.

There will be several challenges within each level. Complete all of them to complete the level, or feel free to skip ahead!


### Full command list
Some commands you'll want to learn and what they do:
* python -m gitgud start 
  * Creates a git repoitory and gets you started on the first challenge!
  * Lets you use `git gud <command>` instead of `python -m gitgud <command>`
* git gud status
  * Shows the challenge you are currently working on
* git gud instructions
  * This the very helpful command that will make you git gud! It displays the instructions for the current challenge, which will show you how to commit, branch and everything else!
* git gud reset
  * Will reset the current challenge in case you mess up
* git gud test
  * Tests to see if the current challenge is complete. If it congratulates you, you've successfully completed the challenge and you can move on! (You can also move on anyways)
* git gud levels
  * Displays all levels
* git gud challenges
  * Displays all challenges in the current level
* git gud challenges <level_name>
  * Displays all challenges in the specified level
* git gud load <level_name>
  * Begin the first challenge of the specified level
* git gud load <level_name> <challenge_name>
  * Begin the specified challenge (it is optional to specify the challenge)
* git gud load next
  * Takes you to the next challenge
* git gud commit
  * Commit an empty file with a unique name
* git gud commit <name>
  * Commit an empty file with the specified name
* git gud goal
  * Consicely prints out what is needed to complete the challenge
* git gud show-tree
  * Visualizes the current git tree
