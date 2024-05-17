from setuptools import setup, find_packages

setup(
    name='pymenu-cli',
    version='1.0.0',
    description='A Python library for creating interactive CLI menus',
    author='Moraneus',
    author_email='moraneus@gmail.com',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pymenu-cli = pymenu_cli:main'
        ]
    }
)