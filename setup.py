from setuptools import setup


with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='git-gud',
    version=open('gitgud/version.txt').read().strip(),
    url='https://github.com/benthayer/git-gud/',
    description='A tool to learn git',
    author='Ben Thayer',
    author_email='ben@benthayer.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[
        'gitgud',
        'gitgud.hooks',
        'gitgud.skills',
        'gitgud.skills.basics',
        'gitgud.skills.extras',
        'gitgud.skills.rampup',
    ],
    package_data={
        'gitgud': ['version.txt', 'welcome.txt'],
        'gitgud.skills.basics': ['_*/*'],
        'gitgud.skills.extras': ['_*/*'],
        'gitgud.skills.rampup': ['_*/*'],
    },
    python_requires='>=3.5',
    install_requires=[
        'gitpython',
        'importlib_resources'
    ],
    entry_points={
        "console_scripts": [
            "git-gud=gitgud.__main__:main"
        ]
    }
)
