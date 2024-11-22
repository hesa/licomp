# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
import logging

from licomp_olddummy import OldDummyLicense
from licomp.interface import UseCase
from licomp.interface import Provisioning
from licomp.interface import Modification



def test_oldversion():
    with pytest.raises(Exception):
        dl = OldDummyLicense()    
    
