import pytest

import os

from gitgud.__main__ import GitGud


@pytest.fixture
def gg(tmp_path):
    tmp_path = str(tmp_path)
    os.chdir(tmp_path)
    gg = GitGud()
    gg.handle_init(gg.parser.parse_args(['init']))

    return gg
