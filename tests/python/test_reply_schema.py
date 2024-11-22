#!/bin/env python3

# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os
import logging
from jsonschema import validate
from licomp_dummy import DummyLicense
from licomp.interface import UseCase
from licomp.interface import Provisioning
from licomp.interface import Modification
import pytest


DATA_DIR=os.path.dirname(__file__)
DATA_DIR=os.path.join(DATA_DIR, '..')
DATA_DIR=os.path.join(DATA_DIR, '..')
DATA_DIR=os.path.join(DATA_DIR, 'licomp')
DATA_DIR=os.path.join(DATA_DIR, 'data')

JSON_SCHEMA=os.path.join(DATA_DIR, 'reply_schema.json')

with open(JSON_SCHEMA) as fp:
    schema = json.load(fp)

dl = DummyLicense()

def test_success():
    try:
        logging.info('validate response')
        ret = dl.outbound_inbound_compatibility("BSD-3-Clause", "GPL-2.0-only")
        validate(instance=ret, schema=schema)
    except Exception as e:
        pytest.fail(f'Unexpected exception: {e}')


def test_not_supported():
    try:
        logging.info('validate response')
        ret = dl.outbound_inbound_compatibility("BSD-3-Clause", "NO_SUPPORTED")
        validate(instance=ret, schema=schema)
    except Exception as e:
        pytest.fail(f'Unexpected exception: {e}')

def test_not_supported():
    try:
        logging.info('validate response')
        ret = dl.outbound_inbound_compatibility("BSD-3-Clause", "NO_SUPPORTED", usecase=UseCase.SNIPPET)
        validate(instance=ret, schema=schema)
    except Exception as e:
        pytest.fail(f'Unexpected exception: {e}')

