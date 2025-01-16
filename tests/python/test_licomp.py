# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
import logging

from licomp_dummy import DummyLicense
from licomp.interface import UseCase
from licomp.interface import Provisioning
from licomp.interface import Modification

dl = DummyLicense()

def test_supported():
    assert len(dl.supported_licenses()) == 3
    
def test_provisionings():
    assert len(dl.supported_provisionings()) == 1
    
def test_usecases():
    assert len(dl.supported_usecases()) == 1
    
def test_license_is_supported():
    assert dl.license_supported("BSD-3-Clause")
    
def test_license_is_not_supported():
    assert not dl.license_supported("Some-license-that-does-not-exist")
    
def test_compat():
    ret = dl.outbound_inbound_compatibility("GPL-2.0-only", "BSD-3-Clause")
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == "yes"
    assert ret['status'] == "success"

def test_incompat():
    ret = dl.outbound_inbound_compatibility("BSD-3-Clause", "GPL-2.0-only")
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == "no"
    assert ret['status'] == "success"

def test_compat_unsupported_license():
    ret = dl.outbound_inbound_compatibility("BSD-3-Clause", "NOT-SUPPORTED")
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == None
    assert ret['status'] == "failure"

def test_compat_supported_use_case():
    ret = dl.outbound_inbound_compatibility("BSD-3-Clause", "NOT-SUPPORTED", UseCase.LIBRARY)
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == None
    assert ret['status'] == "failure"

def test_compat_unsupported_use_case():
    ret = dl.outbound_inbound_compatibility("BSD-3-Clause", "NOT-SUPPORTED", UseCase.SNIPPET)
    logging.debug("ret: " + str(ret))
    assert ret['compatibility_status'] == None
    assert ret['status'] == "failure"

