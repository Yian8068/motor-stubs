# -*- coding: utf-8 -*-
from setuptools import setup

packages = ['src', 'src.motor_stubs.motor']

package_data = {'': ['*']}

setup_kwargs = {
    'name': 'motor-stubs-test',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'Daniel Hsiao',
    'author_email': 'yian8068@yahoo.com.tw',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
