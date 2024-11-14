# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
import logging

from licomp_dummy import DummyLicense

dl = DummyLicense()

def test_supported():
    assert len(dl.supported_licenses()) == 2
    
def test_is_supported():
    assert dl.license_supported("BSD-3-Clause")
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

