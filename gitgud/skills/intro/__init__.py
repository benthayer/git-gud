import subprocess

from gitgud.skills.util import Skill
from gitgud.skills.level_builder import BasicLevel

from gitgud.skills.user_messages import simulate_command
from gitgud.skills.user_messages import show_tree
from gitgud.skills.user_messages import default_fail_no_reset

class Level1(BasicLevel):
    def __init__(self):
        super().__init__('welcome' , __name__)

    def post_setup(self):
        self.display_message("post-setup.txt")

    def status(self):
        self.display_message("status-1.txt")
        simulate_command("git log")
        self.display_message("status-2.txt")
    
    def test_failed(self):
        default_fail_no_reset()

    def test_passed(self):
        self.display_message("passed.txt")


def get_name_and_email():
    name = subprocess.check_output('git config user.name', shell=True).decode().strip()
    email = subprocess.check_output('git config user.email', shell=True).decode().strip()
    return name, email

class Level2(BasicLevel):
    def __init__(self):
        super().__init__('level2' , __name__)

    def post_setup(self):
        self.display_message("post-setup.txt")

    def status(self):
        self.display_message("status-1.txt")

        name, email = get_name_and_email()

        print()
        print('user.name: "{}"'.format(name))
        print('user.email: "{}"'.format(email))

        self.display_message("how-to-configure.txt")

    def _test(self, file_operator):
        name, email = get_name_and_email()
        return name and email
    
    def test_failed(self):
        default_fail_no_reset()
    
    def test_passed(self):
        self.display_message("passed.txt")


skill = Skill(
    'intro',
    [
        Level1(),
        Level2(),
    ]
)
