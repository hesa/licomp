# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

clean:
	find . -name "*~" | xargs rm -f
	rm -fr build
	rm -fr dist
	rm -fr test/python/pytest_cache
	rm -fr licomp/__pycache__
	rm -fr tests/python/__pycache__
	rm -fr licomp.egg-info

py-lint:
	PYTHONPATH=. flake8 flame

build:
	rm -fr build && python3 setup.py sdist

test:
	PYTHONPATH=python/ python3 -m pytest --log-cli-level=10 tests/python
	tests/shell/test_cli.sh

install:
	pip install .

reuse:
	reuse lint

lint:
	flake8
