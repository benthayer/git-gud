# Git Gud

Git Gud is meant to be an extended and more lightweight version of [learngitbranching.js.org](learngitbranching.js.org).

The goal is to make this project contributor-friendly and able to support
 exercises for every git command out there with minimal additional effort on the contributor end. Specifically, we want to build a guide that anyone can understand, even if they are unfamiliar with coding concepts.
 
This repository is very much under development, and we want your help! One of the best ways to learn about git is to
actually contribute to a project, and what better project than this one!

Development install (Currently only option):
From the top level directory (with README.md and setup.py), run pip install -e .
This will install git gud as a python module.
In general, to run a python module, we run `python -m <module>`
For us, this will be `python -m gitgud`, but that will just 

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
* git gud progress
  * Takes you to the next challenge
* git gud levels
  * Displays all levels
* git gud load <level_name>
  * Begin the first challenge of the specified level
* git gud load <level_name> <challenge_name>
  * Begin the specified challenge

There will be several challenges within each level. Complete all of them to complete the level, or feel free to skip ahead!

* git gud load challenge 2 level2
* git gud commit <commit_name>
  * Simulate a commit (used in many of the challenges)
