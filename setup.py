# -*- coding: utf-8 -*-
import sys
from setuptools import setup
import flyadmin

if sys.version_info < (3, 0):

    long_description = "\n".join([
        open('README.md', 'r').read(),
    ])
else:
    long_description = "\n".join([
        open('README.md', 'r', encoding='utf-8').read(),
    ])

setup(
    name='flyadmin',
    version=flyadmin.get_version(),
    packages=['flyadmin'],
    zip_safe=False,
    include_package_data=True,
    url='https://github.com/panyuan5056/flyadmin',
    license='Apache License 2.0',
    author='py',
    long_description=long_description,
    author_email='376105482@qq.com',
    description='django admin theme 后台模板',
    install_requires=['django'],
)
