from setuptools import setup

setup(
    name='dice_parser',
    version='0.4',
    packages=['dice_parser'],
    install_requires=['lark-parser'],
    url='https://github.com/VadimPushtaev/dice_parser',
    license='MIT',
    author='Vadim Pushtaev',
    author_email='pushtaev.vm@gmail.com',
    description='Arithmetic expressions with dice roll support'
)
