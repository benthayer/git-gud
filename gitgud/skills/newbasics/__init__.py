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
        if len(file_operator.get_commits()) != 2:
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
            if not failed:
                if test():
                    goal_status = complete
                else:
                    goal_status = incomplete
                    failed = True
            else:
                goal_status = untested

            print(f"{goal_status} {user_text}")

    def _test1(self):
        # Test if a single file has been added to the first commit
        file_operator = operations.get_operator()

        commits = file_operator.get_commits()

        if len(commits) < 1:
            return None

        content = file_operator.get_commit_content(commits[0])
        if len(content.keys()) != 1:
            return False

        return True

    def _test2(self):
        # Test if a single file has been added to the second commit
        file_operator = operations.get_operator()

        commits = file_operator.get_commits()

        if len(commits) < 2:
            return None

        content1 = file_operator.get_commit_content(commits[0])
        content2 = file_operator.get_commit_content(commits[1])

        # There is only one more file in the second commit
        if len(content1) + 1 != len(content2):
            return False

        filename1 = next(iter(content1.keys()))

        if filename1 not in content2:
            return False
        if content1[filename1] != content2[filename1]:
            return False

        return True

    def _test3(self):
        # Test that both files were modified in commit three
        file_operator = operations.get_operator()

        commits = file_operator.get_commits()

        if len(commits) < 3:
            return None

        content2 = file_operator.get_commit_content(commits[1])
        content3 = file_operator.get_commit_content(commits[2])

        # Same number of files
        if len(content2) != len(content3):
            return False

        # Both files have new content and same name
        for filename in content2:
            if filename not in content3:
                return False
            if content2[filename] == content3[filename]:
                return False

        return True

    def _test4(self):
        # File 1 was removed in commit 4
        file_operator = operations.get_operator()

        commits = file_operator.get_commits()

        if len(commits) < 4:
            return None

        content1 = file_operator.get_commit_content(commits[0])
        content3 = file_operator.get_commit_content(commits[2])
        content4 = file_operator.get_commit_content(commits[3])

        file1 = next(iter(content1.keys()))

        # Construct content4 from content3
        del content3[file1]

        return content3 == content4

    def _test5(self):
        # File 2 was moved in commit 5
        file_operator = operations.get_operator()

        commits = file_operator.get_commits()

        if len(commits) < 5:
            return None

        content4 = file_operator.get_commit_content(commits[3])
        content5 = file_operator.get_commit_content(commits[4])

        if len(content5) != 1:
            return False

        filename2_orig = next(iter(content4.keys()))
        filename2_new = next(iter(content5.keys()))

        if filename2_orig in content5:
            return False

        if content4[filename2_orig] != content5[filename2_new]:
            return False

        return True

    def _test(self):
        file_operator = operations.get_operator()

        if file_operator.branch_has_merges():
            return False

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
