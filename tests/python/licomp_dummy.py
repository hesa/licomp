# SPDX-FileCopyrightText: 2021 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from licomp.interface import Licomp
from licomp.interface import ObligationTrigger
from licomp.interface import ModifiedTrigger
from licomp.interface import CompatibilityStatus
from licomp.interface import Status

class DummyLicense(Licomp):

    def __init__(self):
        Licomp.__init__(self)
        self.supported_obligation_triggers = [ObligationTrigger.BIN_DIST]
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
                                       trigger=ObligationTrigger.BIN_DIST,
                                       modified=ModifiedTrigger.UNMODIFIED):
        return self.outbound_inbound_reply(self.licenses[outbound][inbound],'some stupid explanation')

    def name(self):
        return "dummy"
    
    def version(self):
        return "version sth"
    
    def supported_licenses(self):
        return list(self.licenses.keys())

    def supported_triggers(self):
        return self.supported_obligation_triggers

