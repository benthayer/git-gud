from gitgud.util.level_builder import BasicLevel
from gitgud.util import Skill
from gitgud.util import operations
from gitgud.user_messages import separated, bool_to_word
from gitgud.user_messages.stateful import display_repo_files


class FirstCommit(BasicLevel):
    @separated
    def status(self):
        created, added, committed = self.get_state()
        print("Created:", bool_to_word(created))
        print("Added:", bool_to_word(added))
        print("Committed:", bool_to_word(committed))

    def get_state(self):
        file_operator = operations.get_operator()

        created = bool(file_operator.get_working_directory_content())
        added = bool(file_operator.get_staging_content())
        committed = file_operator.repo.head.is_valid() \
            and bool(file_operator.get_commit_content('HEAD'))

        return created, added, committed

    def _test(self):
        created, added, committed = self.get_state()
        return created and added and committed

    def post_setup(self):
        self.cat_file("post-setup.txt")


class TwoCommits(BasicLevel):
    def post_setup(self):
        self.goal()

    def status(self):
        display_repo_files()

    def _test(self):
        file_operator = operations.get_operator()

        # There are two commits
        if len(file_operator.get_all_commits()) != 2:
            return False

        # The first commit has one file
        content1 = file_operator.get_commit_content('HEAD~')
        if len(content1.keys()) != 1:
            return False

        # The second commit has two files
        content2 = file_operator.get_commit_content('HEAD')
        if len(content2.keys()) != 2:
            return False

        # The file from the first commit is in the second commit
        file1_name = next(iter(content1.keys()))
        if file1_name not in content2:
            return False

        # The first file is unchanged
        if content1[file1_name] != content2[file1_name]:
            return False

        # Working Directory, Staging Area and Commit 2 are the same
        content_wd = file_operator.get_working_directory_content()
        content_sa = file_operator.get_staging_content()
        if not (content2 == content_wd == content_sa):
            return False

        return True


class FiveCommits(BasicLevel):
    def _setup(self):
        # TODO Start on the master commit
        pass
    def status(self):
        complete = "✔️"
        incomplete = "✘"
        untested = "•"

        tests = [
            (self._test1, "Commit 1: Add a file"),
            (self._test2, "Commit 2: Add another file"),
            (self._test3, "Commit 3: Modify both files"),
            (self._test4, "Commit 4: Delete the file from commit 1"),
            (self._test5, "Commit 5: Rename the file from commit 2")
        ]

        failed = False
        for test, user_text in tests:
            if failed:
                print(f"{untested} {user_text}")
            if test():
                print(f"{complete} {user_text}")
            else:
                print(f"{incomplete} {user_text}")

        print()
        print("Note: Fix errors before continuing.")
        print("Try these if you're stuck:")
        print("git gud explain add")
        print("git gud explain modify")
        print("git gud explain remove")
        print("git gud explain rename")

    def _test1(self):
        # Test if a single file has been added to the first commit
        file_operator = operations.get_operator()
        commit1 = file_operator.get_all_commits()[0]
        content = file_operator.get_commit_content(commit1)
        if len(content.keys()) != 1:
            return False
        return True

    def _test2(self):
        # Test if a single file has been added to the second commit
        file_operator = operations.get_operator()

        all_commits = file_operator.get_all_commits()

        content1 = file_operator.get_commit_content(all_commits[0])
        content2 = file_operator.get_commit_content(all_commits[1])

        # All files from commit 1 are in commit 2
        for file in content1:
            if file not in content2:
                return False
            if content1[file] != content2[file]:
                return False

        # There is only one more file in the second commit
        if len(content1) + 1 != len(content2):
            return False

        return True

    def _test3(self):
        # Test that both files were renamed in commit three

        file_operator = operations.get_operator()
        all_commits = file_operator.get_all_commits()
        # Two files
        # Files both present previously
        # Files both have different content

        return True

    def _test4(self):
        # Get the file from the original commit
        # File 1 has been removed
        file_operator = operations.get_operator()
        return True

    def _test5(self):
        # File 2 has moved
        file_operator = operations.get_operator()
        return True

    def _test(self):
        if not self._test1():
            return False
        if not self._test2():
            return False
        if not self._test3():
            return False
        if not self._test4():
            return False
        if not self._test5():
            return False

        file_operator = operations.get_operator()
        # There are two commits
        if len(file_operator.get_all_commits()) != 5:
            return False

        return True


skill = Skill(
    'New Basics',
    'newbasics',
    [
        FirstCommit('First Commit', 'firstcommit', __name__),
        TwoCommits('Two Commits', 'two', __name__),
        FiveCommits('Five Commits', 'five', __name__)
    ]
)
