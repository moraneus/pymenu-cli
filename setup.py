from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pymenu-cli',
    version='1.0.5',
    description='A Python library for creating interactive CLI menus',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Moraneus',
    author_email='moraneus@gmail.com',
    url='https://github.com/moraneus/pymenu-cli',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pymenu-cli = pymenu_cli.menu:main'
        ]
    },
    license='MIT',
)