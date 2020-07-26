# Required Environments Variables:
#	DEMO_MAGIC_PATH: Path to demo-magic.sh
#	GITGUD_REPO: Path to the git gud repo

# ===== Configure demo-magic.sh
. $DEMO_MAGIC_PATH
PROMPT_TIMEOUT=1
TYPE_SPEED=15
DEMO_PROMPT="${GREEN}➜ ${CYAN}\W${RED}\$ "

# ===== Configure Shell 
OLD_HOME=$(pwd)
 
# We want to exit if any command doesn't work, or if
# an undefined variable is used.
set -euo pipefail

cd /tmp
clear

# ===== Begin presentation 
p "pip3 install git-gud"
pip install ${GITGUD_REPO}

p "We'll first make an empty directory for git gud."
pe "mkdir my-git-gud"
pe "cd my-git-gud"
pe "git gud init"
wait

pe "git gud load 0 3"
pe "git gud status"
pe "git init"
pe "git gud status"
pe "git gud test"
pe "git gud load 1 1"

pe "git gud commit"
pe "git gud commit"
pe "git gud show tree"

pe "git gud test"
pe "git gud load next"
pe "git branch bugFix"
pe "git checkout bugFix"
pe "git gud commit"
pe "git gud test"
pe "git gud levels --all"
pe "git gud load 3-octopus"
pe "git merge feature1 feature2"
p ""

# ===== Cleanup
rm -rf /tmp/my-git-gud
cd $OLD_HOME 
