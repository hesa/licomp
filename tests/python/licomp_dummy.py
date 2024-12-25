# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from licomp.interface import Licomp
from licomp.interface import UseCase
from licomp.interface import Provisioning
from licomp.interface import Modification
from licomp.interface import CompatibilityStatus
from licomp.interface import Status

class DummyLicense(Licomp):

    def __init__(self):
        Licomp.__init__(self)
        self.provisionings = [Provisioning.BIN_DIST]
        self.usecases = [UseCase.LIBRARY]
        self.licenses = {
            "BSD-3-Clause": {
                "GPL-2.0-only": CompatibilityStatus.INCOMPATIBLE,
                "BSD-3-Clause": CompatibilityStatus.COMPATIBLE
            },
            "GPL-2.0-only": {
                "BSD-3-Clause": CompatibilityStatus.COMPATIBLE,
                "GPL-2.0-only": CompatibilityStatus.COMPATIBLE,
            }
        }

    def _outbound_inbound_compatibility(self,
                                        outbound,
                                        inbound,
                                        usecase,
                                        trigger,
                                        modified):
        return self.outbound_inbound_reply(self.licenses[outbound][inbound],
                                           'some stupid explanation')

    def name(self):
        return "DummyLicense"
    
    def version(self):
        return "version sth"
    
    def supported_licenses(self):
        return list(self.licenses.keys())

    def supported_usecases(self):
        return self.usecases

    def supported_provisionings(self):
        return self.provisionings

    def supported_api_version(self):
        return "0.4"

    def disclaimer(self):
        return "example disclaimer"

    def data_url(self):
        return 'https://a-url'

    def url(self):
        return 'https://another-url'
