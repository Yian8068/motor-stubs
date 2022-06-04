# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages


def find_stub_files(name: str) -> list[str]:
    result = []
    for root, _dirs, files in os.walk(name):
        for file in files:
            if file.endswith('.pyi'):
                if os.path.sep in root:
                    sub_root = root.split(os.path.sep, 1)[-1]
                    file = os.path.join(sub_root, file)
                result.append(file)
    return result


with open('README.md') as f:
    readme = f.read()

setup_kwargs = {
    'name': 'motor-stubs',
    'version': '1.2.0',
    'description': '',
    'long_description': readme,
    'author': 'Daniel Hsiao',
    'author_email': 'yian8068@yahoo.com.tw',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': ['motor_stubs', *find_packages()],
    'package_data': {
        'motor-stubs': find_stub_files('motor-stubs'),
        'python_requires': '>=3.9,<4.0',
    },
}

setup(**setup_kwargs)
