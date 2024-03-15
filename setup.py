from setuptools import setup, find_packages

setup(
    name='InfoCLI',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'info-cli=main:main',
        ],
    },
    author='project-team-14',
    description='Personal assistant for managing contacts and notes',
    license='MIT',
    keywords='cli, personal assistant, contacts, notes',
    url='https://github.com/bingooo1337/project-init2024',
)
