#!/bin/env python3

# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os
import logging
from jsonschema import validate
from jsonschema.exceptions import ValidationError
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

with open('tests/replies/success.json') as fp:
    success_reply = json.load(fp)

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
        print(json.dumps(ret, indent=4))
        validate(instance=ret, schema=schema)
    except Exception as e:
        pytest.fail(f'Unexpected exception: {e}')


#
# Test from reply file
#
def _test_content(content):
    validate(instance=content, schema=schema)

def _test_content_raise(content):
    with pytest.raises(ValidationError) as e_info:
        _test_content(content)

def test_success_reply():
    _test_content(success_reply)

# status
def test_status_valid():
    for status in [ "failure", "success" ]:
        reply = dict(success_reply)
        reply['status'] = status
        _test_content(reply)

def test_status_raise():
    for status in [ None, "nonesuch" ]:
        reply = dict(success_reply)
        reply['status'] = status
        _test_content_raise(reply)

# status_details
def test_status_valid():
    for sub in ["provisioning_status", "usecase_status", "license_supported_status" ]:
        for status in [ "failure", "success" ]:
            reply = dict(success_reply)
            reply['status_details'][sub] = status
            _test_content(reply)

def test_status_raise():
    for status in [ None, "nonesuch" ]:
        reply = dict(success_reply)
        reply['status'] = status
        _test_content_raise(reply)

def test_license_raise():
    for sub in ["inbound", "outbound" ]:
        for lic in [ None, "" ]:
            reply = dict(success_reply)
            reply[sub] = lic
            _test_content_raise(reply)

def test_usecase():
    for usecase in ["library", "compiler", "snippet", "tool", "test"]:
        reply = dict(success_reply)
        reply['usecase'] = usecase
        _test_content(reply)

def test_usecase_raises():
    for usecase in [ "", None, True, False, []]:
        reply = dict(success_reply)
        reply['usecase'] = usecase
        _test_content_raise(reply)

def test_provisioning():
    for provisioning in ["source-code-distribution", "binary-distribution", "local-use", "provide-service", "provide-webui"]:
        reply = dict(success_reply)
        reply['provisioning'] = provisioning
        _test_content(reply)

def test_provisioning_raises():
    for provisioning in [ "", None, True, False, []]:
        reply = dict(success_reply)
        reply['provisioning'] = provisioning
        _test_content_raise(reply)

def test_modification():
    for modification in ["modified", "unmodified"]:
        reply = dict(success_reply)
        reply['modification'] = modification
        _test_content(reply)

def test_modification_raises():
    for modification in [ "", None, True, False, []]:
        reply = dict(success_reply)
        reply['modification'] = modification
        _test_content_raise(reply)

def test_compatibilities():
    reply = dict(success_reply)
    for compat_status in [ "yes", "no", "depends", "unknown", "unsupported", None]:
        reply['compatibility_status'] = compat_status
        _test_content(reply)
    
def test_compatibilities_raises():
    reply = dict(success_reply)
    for compat_status in ["", True, False, []]:
        reply['compatibility_status'] = compat_status
        _test_content_raise(reply)
    
def test_explanation():
    reply = dict(success_reply)
    for explanation in [ "a", "bla bla bla", None]:
        reply['explanation'] = explanation
        _test_content(reply)
    
def test_explanation_raises():
    reply = dict(success_reply)
    for explanation in [True, False, []]:
        reply['explanation'] = explanation
        _test_content_raise(reply)
    
def test_api_version():
    reply = dict(success_reply)
    for api_version in [ "0.5", "0.5.6"]:
        reply['api_version'] = api_version
        _test_content(reply)
    
def test_api_version_raises():
    reply = dict(success_reply)
    for api_version in [None, True, False, [], "", "0", "01", "0.5.6.0"]:
        reply['api_version'] = api_version
        _test_content_raise(reply)
    
def test_resource_name():
    reply = dict(success_reply)
    for resource_name in [ "licomp-ososososo", "some licomp name" ]:
        reply['resource_name'] = resource_name
        _test_content(reply)
    
def test_resource_name_raises():
    reply = dict(success_reply)
    for resource_name in [None, True, False, [], "", "0", "01", "abcdefg"]:
        reply['resource_name'] = resource_name
        _test_content_raise(reply)
    
def test_resource_version():
    reply = dict(success_reply)
    for resource_version in [ "0.5", "0.5.6"]:
        reply['resource_version'] = resource_version
        _test_content(reply)
    
def test_resource_version_raises():
    reply = dict(success_reply)
    for resource_version in [None, True, False, [], "", "0", "01", "0.5.6.0"]:
        reply['resource_version'] = resource_version
        _test_content_raise(reply)
    
def test_disclaimer():
    reply = dict(success_reply)
    for disclaimer in [ "not my fault, really", "itwas the other three" ]:
        reply['resource_disclaimer'] = disclaimer
        _test_content(reply)
    
def test_disclaimer_raises():
    reply = dict(success_reply)
    for disclaimer in [None, True, False, [], "", "0", "01", "abcdefg"]:
        reply['resource_disclaimer'] = disclaimer
        _test_content_raise(reply)
    
def test_resource_url():
    reply = dict(success_reply)
    for resource_url in [ "not my fault, really", "itwas the other three" ]:
        reply['resource_url'] = resource_url
        _test_content(reply)
    
def test_resource_url_raises():
    reply = dict(success_reply)
    for resource_url in [None, True, False, [], "", "0", "01", "abcdefg"]:
        reply['resource_url'] = resource_url
        _test_content_raise(reply)
    
def test_data_url():
    reply = dict(success_reply)
    for data_url in [ "not my fault, really", "itwas the other three" ]:
        reply['data_url'] = data_url
        _test_content(reply)
    
def test_data_url_raises():
    reply = dict(success_reply)
    for data_url in [None, True, False, [], "", "0", "01", "abcdefg"]:
        reply['data_url'] = data_url
        _test_content_raise(reply)
    
