
import subprocess

from gitgud.skills import all_skills


def test_load(gg):
    load_tests = [
        ('git gud load 1', all_skills[0][0]),
        ('git gud load rampup', all_skills["rampup"][0]),
        ('git gud load 2 detaching', all_skills[1]["detaching"]),
        ('git gud load rampup 4', all_skills["rampup"][3]),
        ('git gud load 3-octopus', all_skills[2]["octopus"]),
        ('git gud load basics-4', all_skills["basics"][3]),
        ('git gud load -2', all_skills["basics"][1])
    ]
    
    for command, level in load_tests:
        subprocess.call(command, shell=True)
        assert level == gg.file_operator.get_level()
    
    