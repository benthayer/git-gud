from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        from gitgud import create_alias
        create_alias()
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        from gitgud import create_alias
        create_alias()
        install.run(self)


with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='git-gud',
    version='0.1',
    url='https://github.com/bthayer2365/git-gud/',
    description='A tool to learn git',
    author='Ben Thayer',
    author_email='ben@benthayer.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[
        'gitgud'
    ],
    install_requires=[
        'gitpython',
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    }
)
