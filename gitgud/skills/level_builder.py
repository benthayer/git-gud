from importlib_resources import files

from .parsing import test_ancestry
from .parsing import level_json
from .parsing import parse_spec
from .parsing import name_from_map
from .parsing import get_non_merges
from .parsing import name_merges

from .user_messages import cat_file
from .user_messages import show_level_name
from .user_messages import show_tree
from .user_messages import default_fail
from .user_messages import level_complete
from .user_messages import skill_complete
from .user_messages import all_levels_complete
from .user_messages import solution_print_header
from .user_messages import no_solutions_available

from gitgud import operations


class Level:
    def __init__(self, readable_name, name):
        self.name = name
        self.readable_name = readable_name
        self.skill = None
        self.next_level = None
        self.prev_level = None

    def __repr__(self):
        return "<{class_name}: '{full_name}'>".format(
            class_name=type(self).__name__,
            full_name=self.full_name()
        )

    def full_name(self):
        return '{} {}'.format(self.skill.name, self.name)

    def _setup(self):
        pass

    def setup(self):
        self._setup()
        self.post_setup()

    def post_setup(self):
        show_level_name(self)

    def explain(self):
        pass

    def goal(self):
        pass

    def status(self):
        show_level_name(self)

    def has_ever_been_completed(self):
        return self._test()

    def _test(self):
        raise NotImplementedError

    def test(self):
        if self._test():
            self.test_passed()
        else:
            self.test_failed()

    def test_passed(self):
        if self.next_level is None:
            all_levels_complete()
        elif self.next_level.skill != self.skill:
            skill_complete(self)
        else:
            level_complete(self)

    def test_failed(self):
        default_fail()


class BasicLevel(Level):
    def __init__(self, readable_name, name, skill_package):
        super().__init__(readable_name, name)

        self.level_dir = files(skill_package).joinpath('_{}/'.format(name))

    def file(self, path):
        return self.level_dir.joinpath(path)

    def cat_file(self, path):
        cat_file(self.file(path))

    def _setup(self):
        file_operator = operations.get_operator(initialize_repo=True)
        commits, head = parse_spec(self.file('setup.spec'))
        file_operator.create_tree(commits, head)

        latest_commit = '0'
        for commit_name, _, _, _ in commits:
            try:
                if int(commit_name) > int(latest_commit):
                    latest_commit = commit_name
            except ValueError:
                pass  # Commit is merge and doesn't have number

        file_operator.write_last_commit(latest_commit)

    def post_setup(self):
        self.cat_file('goal.txt')
        show_tree()

    def explain(self):
        for line in self.file('explanation.txt') \
                .read_text().strip().split('\n'):
            if line[:3] == '>>>':
                input('>>>')
            else:
                print(line.strip())

    def goal(self):
        self.cat_file("goal.txt")

    def solution_list(self):
        solution_commands = []

        for command in self.file('solution.txt').read_text().split('\n'):
            if command and command.strip()[0] != "#":
                solution_commands.append(command)

        return solution_commands

    def solution(self):
        solution = self.solution_list()
        if not solution:
            no_solutions_available()
        else:
            solution_print_header(self)
            for command in solution:
                print(' '*4 + command)

    def _test(self):
        file_operator = operations.get_operator()
        commits, head = parse_spec(self.file('test.spec'))

        # Get commit trees
        test_tree = level_json(commits, head)
        level_tree = file_operator.get_current_tree()

        # Get commit info
        non_merges = get_non_merges(level_tree)

        # Name known commits
        known_commits = file_operator.get_known_commits()
        name_from_map(level_tree, known_commits)

        # Name rebases and cherrypicks
        known_non_merges = {commit_hash: name
                            for commit_hash, name in known_commits.items()
                            if name[:1] != 'M'}
        diff_map = file_operator.get_copy_mapping(non_merges, known_non_merges)
        name_from_map(level_tree, diff_map)

        # Name merges
        name_merges(level_tree, test_tree)

        # Test for similarity
        return test_ancestry(level_tree, test_tree)

    def test_passed(self):
        if self.file('passed.txt').exists():
            self.cat_file('passed.txt')
        else:
            super().test_passed()
