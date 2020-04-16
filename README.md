# Git Gud

![Demonstration](./preview.gif)

## What is it?
Welcome to Git Gud, a command line game designed to help you learn how to use the popular version control system known as Git!
As levels progress, you will know more and more about git, and eventually become a git grandmaster!

If something's missing feel free to add an issue, or if you're interested, view the [contributors file](https://github.com/benthayer/git-gud/blob/master/CONTRIBUTING.md) and add something yourself! The project is intentially structured to make it very easy to add new levels!

If you're more of a visual learner, you should start with ["Learn Git Branching"](https://learngitbranching.js.org), and and then give Git Gud a try. Learn Git Branching is more visual, but with Git Gud, you're actually using git to complete the levels.

## How do I use it?
First, you'll need to be using a version of Python>=3.6.
We'll use python to install Git Gud.
Depending on which way you want to install, we'll either do a "User install" by downloading the `git-gud` package from PyPi, which is handled by pip, or we'll do an edit-mode (development) install, which also uses pip, but in a different way.
Once it's installed, we make an empty directory and switch into it. We need to do this because Git Gud acts as if we're in a git repository and modifies the files to set up different "levels".
If we were in another directory, it would delete all our files! But don't worry, there's a built in failsafe, so Git Gud will warn us before it does anything like that.

Recap:

1. Install Git Gud using Python>=3.6
2. Create and change into an empty directory for Git Gud to load the skills into
3. Run `git gud init`
4. Follow the instructions to git gud!

For specific instructions, see below.

### User install:
Use this method if all you're looking to do is to use Git Gud.
Open up a command line and type the following in.
```
pip3 install git-gud
mkdir test
cd test
git gud init # Initializes a git repository and lets us start using git gud from within this folder
```

### Development install:  
Use this method if you'd like to contribute to this repository.  
Open up a command line and type the following in. Make sure you're in the directory you want your local copy of Git Gud to be in.
```
git clone https://github.com/benthayer/git-gud
cd git-gud
pip3 install -e . # Installs in edit mode so we can change files without needing to reinstall
cd ..
mkdir test
cd test
git gud init # Initializes a git repository and lets us start using git gud from within this folder
```

Once it's installed, you can access all the features that Git Gud has to offer.
If you just want to get started, type in `git gud instructions`.
The first skill is already loaded for you, and all you just have to do is follow the instructions and it'll guide you through the levels.
Once you think you're done with a skill, run `git gud test` to see of you've completed the level.
If you've solved it, run `git gud load next` to move on to the next level! Look at the full command list below for a complete command list.

There will be several levels within each skill. Complete all of them to complete the skill, or feel free to skip ahead!


### Full command list
Some commands you'll want to learn and what they do:
* python -m gitgud start 
  * Creates a git repository and gets you started on the first level!
  * Lets you use `git gud <command>` instead of `python3 -m gitgud <command>`
* git gud status
  * Shows the level you are currently working on
* git gud instructions
  * This the very helpful command that will make you git gud! It displays the instructions for the current level, which will show you how to commit, branch and everything else!
* git gud reset
  * Will reset the current level in case you mess up
* git gud test
  * Tests to see if the current level is complete. If it congratulates you, you've successfully completed the level and you can move on! (You can also move on anyways)
* git gud skills
  * Displays all skills
* git gud levels
  * Displays all levels in the current skill
* git gud levels <skill_name>
  * Displays all levels in the specified skill
* git gud load next
  * Takes you to the next level
* git gud load prev
  * Takes you to the previous level
* git gud load <skill_name>
  * Begin the first level of the specified skill
* git gud load -<level_name>
  * Begin the specified level of the current skill
* git gud load <skill_name> <level_name>
  * Begin the specified level of a skill
  * A hyphen can be used instead of a space between <skill_name> and <level_name>
* git gud commit
  * Commit an empty file with a unique name
* git gud commit <commit_name>
  * Commit an empty file with the specified name
* git gud goal
  * Concisely prints out what is needed to complete the level
* git gud show-tree
  * Visualizes the current git tree
