# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from licomp_dummy import DummyLicense

class OldDummyLicense(DummyLicense):
    

    def supported_api_version(self):
        return "0.2"

    def name(self):
        return "OldDummyLicense"

