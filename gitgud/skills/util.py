import os

from copy import deepcopy


# TODO GitPython topology
def get_topology(tree):
    tree['topology'] = None
    raise NotImplementedError


def parse_spec(file_name):
    # The purpose of this method is to get a more computer-readable commit tree
    with open(file_name) as spec_file:
        spec = spec_file.read()

    commits = []  # List of (commit_name, [parents], [branches], [tags])
    all_branches = set()
    all_tags = set()

    for line in spec.split('\n'):
        if len(line) == 0 or line[0] == '#':
            # Last line or comment
            continue
        line = line.replace('  ', '')

        if '(' in line:
            commit_str = line[:line.find('(')].strip()
            ref_str = line[line.find('(')+1:-1].strip().replace(' ', '')
        else:
            commit_str = line.strip()
            ref_str = ''

        if ':' not in commit_str:
            # Implicit parent, use previous commit
            if len(commits) == 0:
                parents = []
            else:
                parents = [commits[len(commits)-1][0]]
            commit_name = commit_str
        else:
            # Find parent
            commit_name, parent_str = commit_str.split(':')
            commit_name = commit_name.strip()
            parent_str = parent_str.strip()

            if parent_str:
                parents = parent_str.split(' ')
            else:
                parents = []

        # We know the commit name and parents now

        assert ' ' not in commit_name  # There should never be more than one change or a space in a name

        # Process references
        if ref_str:
            refs = ref_str.split(',')
        else:
            refs = []
        branches = []
        tags = []
        for ref in refs:
            if ref[:4] == 'tag:':
                tag = ref[4:]
                assert tag not in all_tags
                tags.append(tag)
                all_tags.add(tag)
            else:
                branch = ref
                assert branch not in all_branches
                branches.append(branch)
                all_branches.add(branch)
        commits.append((commit_name, parents, branches, tags))

    head = commits[-1][0]
    del commits[-1]

    return commits, head


def level_json(commits, head):
    # We've formally replicated the input string in memory

    level = {
        'topology': [],
        'branches': {},
        'tags': {},
        'commits': {},
        'HEAD': {},
    }

    all_branches = []
    all_tags = []
    for commit_name, parents, branches_here, tags_here in commits:
        level['topology'].append(commit_name)
        level['commits'][commit_name] = {
            'parents': parents,
            'id': commit_name
        }

        all_branches.extend(branches_here)
        all_tags.extend(tags_here)

        for branch in branches_here:
            level['branches'][branch] = {
                'target': commit_name,
                'id': branch
            }

        for tag in tags_here:
            level['tags'][tag] = {
                'target': commit_name,
                'id': tag
            }

    level['HEAD'] = {
        'target': head,
        'id': 'HEAD'
    }

    return level


def test_skill(skill, test):
    # We don't know the names of merges, so we match them with their test names
    # TODO Only works when merges don't have other merges as parents
    # TODO Topological sort merge commits
    skill = deepcopy(skill)
    merge_name_map = {}
    for commit_name in skill['commits']:
        skill_commit = skill['commits'][commit_name]
        if len(skill_commit['parents']) >= 2:  # TODO Stop here to get list of merges
            for test_commit_name in test['commits']:  # TODO Do this iteration in an intelligent manner
                test_commit = test['commits'][test_commit_name]
                parents_equal = True
                skill_parents = skill_commit['parents']
                test_parents = test_commit['parents']

                for skill_parent, test_parent in zip(skill_parents, test_parents):
                    if skill_parent != test_parent:
                        parents_equal = False
                        break
                if len(skill_parents) == len(test_parents) and parents_equal:
                    merge_name_map[test_commit_name] = commit_name

    # TODO Update parents to reference merge commits by new name

    # Check commits
    if len(test['commits']) != len(skill['commits']):
        return False
    for commit_name in test['commits']:
        test_commit = test['commits'][commit_name]
        if commit_name not in skill['commits']:
            if merge_name_map[commit_name] in skill['commits']:
                # It's a known merge
                skill_commit = skill['commits'][merge_name_map[commit_name]]
            else:
                return False
        else:
            skill_commit = skill['commits'][commit_name]

        # Commits must have the same number of parents and be in the same order
        if len(skill_commit['parents']) != len(test_commit['parents']):
            return False
        for skill_parent, test_parent in zip(skill_commit['parents'], test_commit['parents']):
            if skill_parent != test_parent:
                return False

    # Check branches
    if len(test['branches']) != len(skill['branches']):
        return False
    for branch_name in test['branches']:
        if branch_name not in skill['branches']:
            return False
        if skill['branches'][branch_name]['target'] != test['branches'][branch_name]['target']:
            if merge_name_map[test['branches'][branch_name]['target']] != skill['branches'][branch_name]['target']:
                return False  # It's also not a known merge

    # Check tags
    if len(test['tags']) != len(skill['tags']):
        return False
    for tag_name in test['tags']:
        if tag_name not in skill['tags']:
            return False
        if skill['tags'][tag_name]['target'] != test['tags'][tag_name]['target']:
            return False

    # Check HEAD
    if skill['HEAD']['target'] != test['HEAD']['target']:
        return False

    return True


class NamedList:
    # names is a list populated with type str, items is a list populated with any type 
    def __init__(self, names, items):
        assert len(names) == len(items)
        self._name_dict = {name:index for index, name in enumerate(names)}
        self._items = items
    
    def __getitem__(self, query):
        if isinstance(query, int):
            return self._items[query]
        elif isinstance(query, str):
            return self._items[self._name_dict[query]]
        else:
            raise ValueError('Bad key type.')

    def __iter__(self):
        return self._items.__iter__()

    def __len__(self):
        return len(self._items)

    def __setitem__(self, key, item):
        if isinstance(key, str):
            self._name_dict[key] = len(self._items)
            self._items.append(item)
        else:
            raise TypeError

    def __contains__(self, key):
        if isinstance(key, str):
            return key in self._name_dict.keys()
        else:
            return key in self._items()

    def values(self):
        return self._items
    
    def keys(self):
        return self._name_dict.keys()


class AllSkills(NamedList):
    def __init__(self, skills):
        self._name_dict = {skill.name: index for index, skill in enumerate(skills)}
        self._items = skills
        last_level = None
        for skill in self:
            for level in skill:
                if last_level is not None:
                    last_level.next_level = level
                last_level = level


class Skill(NamedList):
    def __init__(self, name, levels):
        self.name = name
        self._name_dict = {level.name:index for index, level in enumerate(levels)}
        self._items = levels

        for level in levels:
            level.skill = self


class Level:
    def __init__(self, name):
        self.name = name
        self.skill = None
        self.next_level = None

    def __repr__(self):
        return "<{class_name}: '{full_name}'>".format(
            class_name=type(self).__name__,
            full_name=self.full_name()
        )

    def full_name(self):
        return '{} {}'.format(self.skill.name, self.name)

    def setup(self, file_operator):
        pass

    def instructions(self):
        pass

    def goal(self):
        pass

    def test(self, file_operator):
        pass


def print_all_complete():
    print("Wow! You've complete every level, congratulations!")

    print("If you want to keep learning git, why not try contributing"
          " to git-gud by forking the project at https://github.com/bthayer2365/git-gud/")

    print("We're always looking for contributions and are more than"
          " happy to accept both pull requests and suggestions!")


class BasicLevel(Level):
    def __init__(self, name, path):
        super().__init__(name)
        self.path = path
        self.setup_spec_path = os.path.join(self.path, 'setup.spec')
        self.instructions_path = os.path.join(self.path, 'instructions.txt')
        self.goal_path = os.path.join(self.path, 'goal.txt')
        self.test_spec_path = os.path.join(self.path, 'test.spec')

    def _setup(self, file_operator):
        commits, head = parse_spec(self.setup_spec_path)
        file_operator.create_tree(commits, head)

        latest_commit = '0'
        for commit_name, _, _, _ in commits:
            try:
                if int(commit_name) > int(latest_commit):
                    latest_commit = commit_name
            except ValueError:
                pass  # Commit is merge and doesn't have number

        file_operator.write_last_commit(latest_commit)

    def setup(self, file_operator):
        print('Setting up level: "{}"'.format(self.full_name()))

        self._setup(file_operator)

        print("Setup complete")
        print()
        print("Goal:")
        self.goal()
        print()
        print("Type \"git gud instructions\" to view full instructions")
        print("Type \"git gud help\" for more help")
        print()

    def instructions(self):
        print('Printing instructions for level: "{}"'.format(self.full_name()))
        print()

        with open(self.instructions_path) as instructions_file:
            for line in instructions_file:
                if line[:3] == '>>>':
                    input(">>>")
                else:
                    print(line.strip())

    def goal_str(self):
        with open(self.goal_path) as goal_file:
            return goal_file.read()

    def goal(self):
        print(self.goal_str())

    def _test(self, file_operator):
        commits, head = parse_spec(self.test_spec_path)
        test_tree = level_json(commits, head)
        level_tree = file_operator.get_current_tree()
        return test_skill(level_tree, test_tree)

    def test(self, file_operator):
        print('Testing completion for level: "{}"'.format(self.full_name()))
        print()

        if self._test(file_operator):
            try:
                if self.next_level.skill != self.skill:
                    print("Level complete, you've completed all levels in this skill! `git gud progress` to advance to the next skill")
                    print("Next skill is: {}".format(self.next_level.skill.name))
                else:
                    print("Level complete! `git gud progress` to advance to the next level")
                    print("Next level is: {}".format(self.next_level.full_name()))
            except AttributeError:
                print_all_complete()
        else:
            print("Level not complete, keep trying. `git gud reset` to start from scratch.")
