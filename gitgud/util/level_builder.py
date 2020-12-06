import sys

from importlib_resources import files

import yaml

from .parsing import branches_to_lowercase
from .parsing import test_ancestry
from .parsing import level_json
from .parsing import parse_spec
from .parsing import name_from_map
from .parsing import get_non_merges
from .parsing import name_merges

from gitgud.user_messages import cat_file
from gitgud.user_messages import show_level_name
from gitgud.user_messages import show_tree
from gitgud.user_messages import default_fail
from gitgud.user_messages import level_complete
from gitgud.user_messages import skill_complete
from gitgud.user_messages import all_levels_complete
from gitgud.user_messages import no_solutions_available

from gitgud.util import operations


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
        self.mark_visited()
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
        return self.get_progress() == "complete"

    def _test(self):
        raise NotImplementedError

    def test(self):
        passed = self._test()
        if passed:
            self.mark_complete()
            self.test_passed()
        else:
            self.test_failed()
        return passed

    def test_passed(self):
        if self.next_level is None:
            all_levels_complete()
        elif self.next_level.skill != self.skill:
            skill_complete(self)
        else:
            level_complete(self)

    def test_failed(self):
        default_fail()

    def mark_complete(self):
        file_operator = operations.get_operator()
        file_operator.mark_level(self, "complete")

    def mark_partial(self):
        file_operator = operations.get_operator()
        file_operator.mark_level(self, "partial")

    def mark_visited(self):
        file_operator = operations.get_operator()
        file_operator.mark_level(self, "visited")

    def get_progress(self):
        file_operator = operations.get_operator()
        return file_operator.get_level_progress(self)


class BasicLevel(Level):
    def __init__(self, readable_name, name, skill_package):
        super().__init__(readable_name, name)
        self.level_dir = files(skill_package) / '_{}/'.format(name)

    def file(self, path):
        return self.level_dir / path

    def cat_file(self, path):
        cat_file(self.file(path))

    def _setup(self):
        file_operator = operations.get_operator()
        file_operator.use_repo()
        commits, head = parse_spec(self.file('setup.spec'))

        details_path = self.file('details.yaml')
        if details_path.is_file():
            details = yaml.safe_load(details_path.open())
        else:
            details = None

        file_operator.create_tree(commits, head, details, self.level_dir)

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
        try:
            lines = self.file('explanation.txt').read_text().split('\n>>>\n')
            for i, line in enumerate(lines):
                print(line.strip())
                progress_string = '>>> ({}/{})'.format(i+1, len(lines))
                if i != len(lines) - 1:
                    input(progress_string + '\n')
                    sys.stdout.write("\033[F")  # Cursor up one line
                else:
                    print(progress_string)
        except KeyboardInterrupt:
            exit()  # Handle Traceback for keyboard interrupt

    def goal(self):
        self.cat_file("goal.txt")

    def solution_list(self):
        solution_text = self.file('solution.txt').read_text()

        # Needed because split('\n') would return ['']
        if len(solution_text) == 0:
            return []

        solution_commands = solution_text.strip().split('\n')
        return solution_commands

    def solution(self):
        solution = self.solution_list()
        if not solution:
            no_solutions_available()
        else:
            for command in solution:
                words = command.split()
                if len(words) == 0:
                    continue

                if words[0] == '{create}':
                    filename = command[len('{create} '):].strip()
                    print(f'Create a new file named "{filename}"')
                else:
                    print(command)

    def _test(self):
        file_operator = operations.get_operator()

        # Get commit trees
        test_tree = level_json(*parse_spec(self.file('test.spec')))
        level_tree = file_operator.get_current_tree()

        # Make all user-created branches lowecase
        setup_tree = level_json(*parse_spec(self.file('setup.spec')))
        branches_to_lowercase(level_tree, setup_tree, test_tree)

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
