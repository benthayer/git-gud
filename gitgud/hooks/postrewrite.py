import sys

# TODO Git hooks should not actually do any logging
# TODO Keep track of rebased commits
print(sys.argv[1])

for i, line in enumerate(sys.stdin):
    old_hash, new_hash = line.split()
    print('Change {}'.format(i + 1))
    print('Old hash: ', old_hash)
    print('New hash: ', new_hash)
