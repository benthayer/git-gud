import sys
import os

from configparser import NoSectionError

from git import Actor
from git import Repo

actor = Actor("Git Gud", "git-gud@example.com")
actor_string = "Git Gud <git-gud@example.com>"


class GitConfig(Repo):
    def __init__(self, *args, **kwargs):
        #
        # Work around the GitPython issue #775
        # https://github.com/gitpython-developers/GitPython/issues/775
        #
        self.git_dir = os.path.join(os.getcwd(), ".git")
        Repo.__init__(self, *args, **kwargs)


def create_alias(config_writer=None):
    python = sys.executable.replace('\\', '/')  # Git uses unix-like path separators

    if config_writer is None:
        config_writer = GitConfig().config_writer(config_level='global')

    try:
        config_writer.remove_option('alias', 'gud')
    except NoSectionError:
        pass
    config_writer.add_value('alias', 'gud', f'"! {python} -m gitgud"')

