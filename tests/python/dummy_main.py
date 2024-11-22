# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import sys

from licomp.interface import Provisioning
from licomp.interface import UseCase
from licomp.main_base import LicompParser
from licomp_dummy import DummyLicense

def main():
    o_parser = LicompParser(DummyLicense(),
                            name = "Dummy license impl",
                            description = "Just a dummy impl",
                            epilog = "Do not use",
                            default_usecase = UseCase.LIBRARY,
                            default_provisioning = Provisioning.BIN_DIST)
    o_parser.run()
    
if __name__ == '__main__':
    main()
