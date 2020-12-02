import sys

from gitgud.util.operations import get_operator

operator = get_operator()

for i, line in enumerate(sys.stdin):
    old_hash, new_hash = line.split()
    operator.track_rebase(old_hash, new_hash)
