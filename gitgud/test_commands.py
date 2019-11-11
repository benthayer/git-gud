
import subprocess

from gitgud.skills import all_skills


def test_load(gg):

    dash_temp = 'git gud load {}-{}'
    skill_temp = 'git gud load {}'
    nodash_temp = 'git gud load {} {}'
    twoargs_test = [dash_temp, nodash_temp]
    for i, skill in enumerate(all_skills):
        for temp in twoargs_test:
            for j, level in enumerate(skill):
                subprocess.call(temp.format(i + 1, j + 1), shell=True)
                assert all_skills[i][j] == gg.file_operator.get_level()
                
                subprocess.call(temp.format(i + 1, level.name), shell=True)
                assert all_skills[i][j] == gg.file_operator.get_level()
                
                
                subprocess.call(temp.format(skill.name, level.name), shell=True)
                assert all_skills[i][j] == gg.file_operator.get_level()

                
                subprocess.call(temp.format(skill.name, j + 1), shell=True)
                assert all_skills[i][j] == gg.file_operator.get_level()
        
        subprocess.call('git gud load {}'.format(i + 1), shell=True)
        assert all_skills[i][0] == gg.file_operator.get_level()
        
        subprocess.call('git gud load {}'.format(skill.name), shell=True)
        assert all_skills[skill.name][0] == gg.file_operator.get_level()

