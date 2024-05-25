"""Module for setting up the pymenu-cli package."""

from setuptools import setup, find_packages

# Read the contents of the README and CONTRIBUTORS files
with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

with open("CONTRIBUTING.md", "r", encoding="utf-8") as fh:
    contributing = fh.read()

long_description = f"{readme}\n\n## Contributors\n{contributing}"

setup(
    name='pymenu-cli',
    version='1.0.7',
    description='A Python library for creating interactive CLI menus',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Moraneus',
    author_email='moraneus@gmail.com',
    url='https://github.com/moraneus/pymenu-cli',
    packages=find_packages(),
    install_requires=[
        "colorama",
        "art"
    ],
    entry_points={
        'console_scripts': [
            'pymenu-cli = pymenu_cli.pymenu:main'
        ]
    },
    license='MIT',
)
