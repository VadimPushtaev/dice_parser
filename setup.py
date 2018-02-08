from setuptools import setup

setup(
    name='dice_parser',
    version='0.2',
    packages=['dice_parser'],
    extras_require=['lark'],
    url='https://github.com/VadimPushtaev/dice_parser',
    license='MIT',
    author='Vadim Pushtaev',
    author_email='pushtaev.vm@gmail.com',
    description='Arithmetic expressions with dice roll support'
)
