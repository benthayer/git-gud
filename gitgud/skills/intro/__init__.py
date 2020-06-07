import subprocess

from gitgud.skills.util import Skill
from gitgud.skills.level_builder import BasicLevel

from gitgud.skills.user_messages import simulate_command
from gitgud.skills.user_messages import default_fail_no_reset


class Welcome(BasicLevel):
    def post_setup(self):
        self.display_message("post-setup.txt")

    def status(self):
        self.display_message("status-1.txt")
        simulate_command("git log")

    def test_failed(self):
        default_fail_no_reset()

    def test_passed(self):
        self.display_message("passed.txt")

    def _test(self):
        return True


def get_name_and_email():
    name = subprocess.check_output('git config user.name', shell=True) \
        .decode().strip()
    email = subprocess.check_output('git config user.email', shell=True) \
        .decode().strip()
    return name, email


class Config(BasicLevel):
    def post_setup(self):
        self.display_message("post-setup.txt")

    def status(self):
        self.display_message("status-1.txt")

        name, email = get_name_and_email()

        print()
        print('user.name: "{}"'.format(name))
        print('user.email: "{}"'.format(email))

        self.display_message("status-2.txt")

    def _test(self):
        name, email = get_name_and_email()
        return name and email

    def test_failed(self):
        default_fail_no_reset()

    def test_passed(self):
        self.display_message("passed.txt")


class Init(BasicLevel):
    def setup(self):
        # Make sure we are not in a git repo
        pass

    def post_setup(self):
        self.display_message("post-setup.txt")

    def status(self):
        if self._test():
            self.display_message("status-repo.txt")
        else:
            self.display_message("status-norepo.txt")

    def _test(self):
        # Check if we are in a git repo
        return True

    def test_failed(self):
        default_fail_no_reset()

    def test_passed(self):
        self.display_message("passed.txt")


skill = Skill(
    'intro',
    [
        Welcome('welcome', __name__),
        Config('config', __name__),
        Init('init', __name__),
    ]
)
