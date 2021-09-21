# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = open('requirements.txt').read().split('\n')

setup(
    name='ocrmultieval',
    version='0.0.1',
    description='Frontend to multiple OCR evaluation tools',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Konstantin Baierer',
    author_email='unixprog@gmail.com',
    url='https://github.com/OCR-D/ocrmultieval',
    license='Apache License 2.0',
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'ocrmultieval=ocrmultieval.cli:cli',
            'ocrd-ocrmultieval=ocrmultieval.ocrd_cli:cli',
        ]
    },
)
