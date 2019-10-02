import setuptools

with open('README.md') as readme:
    long_description = readme.read()

setuptools.setup(
    name='git-gud',
    version='0.1',
    author='Ben Thayer',
    author_email='ben@benthayer.com',
    description='A tool to learn git',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bthayer2365/git-gud/',
    packages=setuptools.find_packages()
)