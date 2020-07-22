import subprocess

from gitgud.skills.util import Skill
from gitgud.skills.level_builder import BasicLevel

from gitgud.skills.user_messages import simulate_command
from gitgud.skills.user_messages import default_fail_no_reset

from gitgud import operations


class Welcome(BasicLevel):
    def post_setup(self):
        self.cat_file("post-setup.txt")

    def status(self):
        self.cat_file("status-1.txt")
        simulate_command("git log")

    def test_failed(self):
        default_fail_no_reset()

    def test_passed(self):
        self.cat_file("passed.txt")

    def _test(self):
        return True


def get_name_and_email():
    name = subprocess.run('git config user.name', shell=True,
            check=False, stdout=subprocess.PIPE).stdout.decode().strip()
    email = subprocess.run('git config user.email', shell=True,
            check=False, stdout=subprocess.PIPE).stdout.decode().strip()

    return name, email


class Config(BasicLevel):
    def post_setup(self):
        self.cat_file("post-setup.txt")

    def status(self):
        self.cat_file("status-1.txt")

        name, email = get_name_and_email()

        print()
        print('user.name: "{}"'.format(name))
        print('user.email: "{}"'.format(email))

        self.cat_file("status-2.txt")

    def _test(self):
        name, email = get_name_and_email()
        return bool(name and email)

    def test_failed(self):
        default_fail_no_reset()

    def test_passed(self):
        self.cat_file("passed.txt")


class Init(BasicLevel):
    def _setup(self):
        # Make sure we are not in a git repo
        file_operator = operations.get_operator()
        file_operator.destroy_repo()

    def post_setup(self):
        self.cat_file("post-setup.txt")

    def status(self):
        simulate_command("git status")

    def _test(self):
        # Check if we are in a git repo
        file_operator = operations.get_operator()
        return file_operator.repo_exists()

    def test_failed(self):
        default_fail_no_reset()

    def test_passed(self):
        self.cat_file("passed.txt")


skill = Skill(
    'Introduction',
    'intro',
    [
        Welcome('Welcome', 'welcome', __name__),
        Config('Configuring', 'config', __name__),
        Init('Initialization', 'init', __name__)
    ]
)
