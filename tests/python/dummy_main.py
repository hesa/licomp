# SPDX-FileCopyrightText: 2021 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import sys

from licomp.interface import ObligationTrigger
from licomp.main_base import LicompParser
from test_lcm import DummyLicense

def main():
    o_parser = LicompParser(DummyLicense(),
                            name = "Dummy license impl",
                            description = "Just a dummy impl",
                            epilog = "Do not use",
                            default_trigger = ObligationTrigger.BIN_DIST)
    o_parser.run()
    
if __name__ == '__main__':
    main()
