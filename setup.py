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
    install_requires=[
        'colorama==0.4.6',
        'prompt_toolkit==3.0.43',
    ],
    author='project-team-14',
    description='Personal assistant for managing contacts and notes',
    license='MIT',
    keywords='cli, personal assistant, contacts, notes',
    url='https://github.com/bingooo1337/project-init2024',
)
