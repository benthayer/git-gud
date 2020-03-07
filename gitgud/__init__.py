from importlib_resources import files

import sys
import os
import subprocess

from git import Actor

actor = Actor("Git Gud", "git-gud@example.com")
actor_string = "Git Gud <git-gud@example.com>"


def create_alias():
    python = sys.executable.replace('\\', '/')  # Git uses unix-like path separators

    subprocess.call(['git', 'config', '--global', 'alias.gud', '! "{}" -m gitgud'.format(python)])

__version__ = \
    files('gitgud').joinpath('version.txt').read_text().strip()
