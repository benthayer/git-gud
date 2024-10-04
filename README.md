# Git Gud

![Demonstration](./preview.gif)

## What is it?
Welcome to Git Gud, a command line game designed to help you learn how to use the popular version control system known as Git!
As levels progress, you will know more and more about git, and eventually become a git grandmaster!

If something's missing feel free to add an issue, or if you're interested, view the [contributors file](https://github.com/benthayer/git-gud/blob/main/CONTRIBUTING.md) and add something yourself! The project is intentionally structured to make it very easy to add new levels!

If you're more of a visual learner, you should start with ["Learn Git Branching"](https://learngitbranching.js.org), and and then give Git Gud a try. Learn Git Branching is more visual, but with Git Gud, you're actually using git to complete the levels.

## How do I use it?
For install instructions, see below.

Once Git Gud is installed, typing "git gud" will produce output and will start telling you what to do.
Git Gud is meant to be like a game, and like a game, it has levels.
The levels are divided up into skills, each of which will introduce you to a new topic in Git.
It start off, assuming you have zero knowledge, and then builds up.
For each level, it will give you a goal and will explain what's going on.
Ideally, the game will teach you everything you need to know to beat it, but you're still encouraged to use other resources to learn as much as you want.

The beginning levels of the game start by getting you accustomed to the Git Gud interface, but later on, the training wheels come off, and you'll have to remember to type in the commands.
If you ever forget which commands there are, or if you want to start on a later level, you can always run "git gud help"
The most important commands are `git gud goal`, `git gud status`, `git gud explain` `git gud test`, and `git gud load next`.
Other commands are also useful, but the output of those commands should be enough to guide you through the level.

To get started, you need to initialize Git Gud in an empty directory.
Once Git Gud is initialized, it'll have full control over that directory, and it will start adding/removing commits and files.
There will normally be multiple branches, and you'll be expected to use Git commands to solve each level.
The levels range in difficulty, and require you to do different things.
Some levels are really easy and only require you to read the explanation, but others just give you a situation and you'll need to use what you've learned to solve the level.


### How to install
Git Gud is written in Python 3.
You'll need to have Python >=3.6 installed in your system for Git Gud to work.
I prefer using [Anaconda](https://docs.anaconda.com/anaconda/install/) to make sure everything works correctly, but you can also install with pip if you now what you're doing.

Once your environment is set up with Python >=3.6, installing is simple:
```
pip3 install git-gud
```
Getting started is also simple:
```
git gud
```
Git Gud will guide you through what to do

If either of those command don't work, there are various things you can try:
 - Use `pip` instead of `pip3`
 - Make sure your PATH variable includes Python executables
 - User install: `pip3 install --user git-gud`
 - Use Anaconda
