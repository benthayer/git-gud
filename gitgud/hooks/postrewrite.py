import sys
import os
import subprocess

# TODO Git hooks should not actually do any logging
# TODO Keep track of rebased commits
subprocess.call(["GIT_EDITOR=" + os.path.join(file_operator.hooks_path, "rebasehandler.sh"), "git", "rebase", "-i", "--no-verify",  commit.message.strip() + "'"])

"""
print()
if "rebase" in sys.argv:
    print("Logging for Rebase:")
elif "amend" in sys.argv:
    print("Logging for Amended Commit:")

for i, line in enumerate(sys.stdin):
    old_hash, new_hash = line.split()
    print('Change #{}:'.format(i + 1))
    print('    Old hash: ', old_hash)
    print('    New hash: ', new_hash)
"""
