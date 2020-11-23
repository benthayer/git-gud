from setuptools import setup


with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='git-gud',
    version=open('gitgud/version.txt').read().strip(),
    url='https://github.com/benthayer/git-gud/',
    description='A command line game to learn git',
    author='Ben Thayer',
    author_email='ben@benthayer.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[
        'gitgud',
        'gitgud.util',
        'gitgud.hooks',
        'gitgud.skills',
        'gitgud.user_messages',
        'gitgud.skills.basics',
        'gitgud.skills.extras',
        'gitgud.skills.rampup',
        'gitgud.skills.rework',
        'gitgud.skills.intro',
        'gitgud.skills.mixedbag',
        'gitgud.skills.rewriting',
        'gitgud.skills.newbasics',
    ],
    package_data={
        'gitgud': ['version.txt', 'welcome.txt'],
        'gitgud.skills.intro': ['_*/*'],
        'gitgud.skills.basics': ['_*/*'],
        'gitgud.skills.extras': ['_*/*'],
        'gitgud.skills.rampup': ['_*/*'],
        'gitgud.skills.rework': ['_*/*'],
        'gitgud.skills.mixedbag': ['_*/*'],
        'gitgud.skills.rewriting': ['_*/*'],
        'gitgud.skills.newbasics': ['_*/*'],
    },
    python_requires='>=3.6',
    install_requires=[
        'gitpython==3.1.7',
        'importlib_resources',
        'pyyaml',
    ],
    entry_points={
        "console_scripts": [
            "git-gud=gitgud.__main__:main"
        ]
    },
    data_files=[('man/man1', ['git-gud.1'])]
)
