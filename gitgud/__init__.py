from importlib_resources import files

import sys
import subprocess

from git import Actor


class InitializationError(Exception):
    pass


actor = Actor("Git Gud", "git-gud@example.com")
actor_string = "Git Gud <git-gud@example.com>"


def create_alias():
    # Git uses unix-like path separators
    python = sys.executable.replace('\\', '/')

    subprocess.call(['git config --global alias.gud ! "{}" -m gitgud'
                    .format(python)])


__version__ = files('gitgud').joinpath('version.txt').read_text().strip()
