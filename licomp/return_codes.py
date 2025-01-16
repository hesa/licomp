# SPDX-FileCopyrightText: 2021 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum

from licomp.interface import CompatibilityStatus

class ReturnCodes(Enum):
    LICOMP_OK = 0
    LICOMP_INCONSISTENCY = 1
    LICOMP_INCOMPATIBLE = 2
    LICOMP_DEPENDS = 3
    LICOMP_UNKNOWN = 4
    LICOMP_UNSUPPORTED_LICENSE = 5
    LICOMP_UNSUPPORTED_USECASE = 6
    LICOMP_UNSUPPORTED_PROVISIONING = 7
    LICOMP_UNSUPPORTED_MODIFICATION = 8
    # ... 19 saved for future

    LICOMP_MISSING_ARGUMENTS = 20
    LICOMP_INTERNAL_ERROR = 21


__comp_status_map__ = {
    CompatibilityStatus.compat_status_to_string(CompatibilityStatus.COMPATIBLE): ReturnCodes.LICOMP_OK.value,
    CompatibilityStatus.compat_status_to_string(CompatibilityStatus.INCOMPATIBLE): ReturnCodes.LICOMP_INCOMPATIBLE.value,
    CompatibilityStatus.compat_status_to_string(CompatibilityStatus.DEPENDS): ReturnCodes.LICOMP_DEPENDS.value,
    CompatibilityStatus.compat_status_to_string(CompatibilityStatus.UNKNOWN): ReturnCodes.LICOMP_UNKNOWN.value,
    CompatibilityStatus.compat_status_to_string(CompatibilityStatus.UNSUPPORTED): ReturnCodes.LICOMP_UNSUPPORTED_LICENSE.value,
}

def compatibility_status_to_returncode(compat_status):
    return __comp_status_map__[compat_status]

def licomp_status_to_returncode(licomp_status_details):
    if licomp_status_details['provisioning_status'] == 'failure':
        return ReturnCodes.LICOMP_UNSUPPORTED_PROVISIONING.value
    if licomp_status_details['usecase_status'] == 'failure':
        return ReturnCodes.LICOMP_UNSUPPORTED_USECASE.value
    if licomp_status_details['license_supported_status'] == 'failure':
        return ReturnCodes.LICOMP_UNSUPPORTED_LICENSE.value
    return ReturnCodes.LICOMP_INTERNAL_ERROR
