# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import setuptools
from licomp.config import licomp_version
from licomp.config import licomp_description
from licomp.config import licomp_module_name


requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

requirements_dev = []
with open('requirements-dev.txt') as f:
    requirements_dev = f.read().splitlines()

setuptools.setup(
    name=licomp_module_name,
    version=licomp_version,
    author="Henrik Sanklef",
    author_email="hesa@sandklef.com",
    description="",
    long_description=licomp_description,
    long_description_content_type="text/markdown",
    license_files=('LICENSES/GPL-3.0-or-later.txt',),
    url="https://github.com/hesa/licomp",
    packages=['licomp'],
    entry_points={
        "console_scripts": [
        ],
    },
    package_data={
        'licomp': ['var/*'],
    },
    install_requires=requirements,
    extras_require={
        'dev': requirements_dev,
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Legal Industry",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires='>=3.6',
)
