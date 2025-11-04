from setuptools import setup, find_packages
from core.globals import VERSION

setup(
    name='zapret_gui',
    version=VERSION,
    packages=find_packages(),
    py_modules=['main'],
    entry_points={
        'console_scripts': [
            'zapret_gui=main:main',
        ],
    },
    install_requires=[],
    author='pandazz77',
    description='GUI for zapret'
)