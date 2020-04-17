import sys

from gitgud.operations import get_operator

operator = get_operator()

for i, line in enumerate(sys.stdin):
    old_hash, new_hash = line.split()
    operator.track_rewrite(old_hash, new_hash, sys.argv[1])

