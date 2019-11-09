
import subprocess

from gitgud.skills import all_skills


def test_load(gg):
    subprocess.call('git gud load basics committing', shell=True)

    level = all_skills['basics']['committing']
    assert level == gg.file_operator.get_level()