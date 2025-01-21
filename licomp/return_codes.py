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

    LICOMP_LAST_SUCCESSFUL_CODE = 19
    # ... 18 saved for future

    LICOMP_MISSING_ARGUMENTS = 20
    LICOMP_ILLEGAL_LICENSE = 21
    LICOMP_ILLEGAL_ARGUMENTS = 22
    LICOMP_PARSE_ERROR = 23
    LICOMP_INTERNAL_ERROR = 100


__comp_str_status_map__ = {
    CompatibilityStatus.compat_status_to_string(CompatibilityStatus.COMPATIBLE): ReturnCodes.LICOMP_OK,
    CompatibilityStatus.compat_status_to_string(CompatibilityStatus.INCOMPATIBLE): ReturnCodes.LICOMP_INCOMPATIBLE,
    CompatibilityStatus.compat_status_to_string(CompatibilityStatus.DEPENDS): ReturnCodes.LICOMP_DEPENDS,
    CompatibilityStatus.compat_status_to_string(CompatibilityStatus.UNKNOWN): ReturnCodes.LICOMP_UNKNOWN,
    CompatibilityStatus.compat_status_to_string(CompatibilityStatus.UNSUPPORTED): ReturnCodes.LICOMP_UNSUPPORTED_LICENSE,
}

__comp_status_str_map__ = {
    ReturnCodes.LICOMP_OK.value: CompatibilityStatus.compat_status_to_string(CompatibilityStatus.COMPATIBLE),
    ReturnCodes.LICOMP_INCOMPATIBLE.value: CompatibilityStatus.compat_status_to_string(CompatibilityStatus.INCOMPATIBLE),
    ReturnCodes.LICOMP_DEPENDS.value: CompatibilityStatus.compat_status_to_string(CompatibilityStatus.DEPENDS),
    ReturnCodes.LICOMP_UNKNOWN.value: CompatibilityStatus.compat_status_to_string(CompatibilityStatus.UNKNOWN),
    ReturnCodes.LICOMP_UNSUPPORTED_LICENSE.value: CompatibilityStatus.compat_status_to_string(CompatibilityStatus.UNSUPPORTED),
}

def compatibility_status_to_returncode(compat_status):
    return __comp_str_status_map__[compat_status].value

def returncode_to_compatibility_status(ret_code):
    return __comp_status_str_map__[ret_code]

def licomp_status_to_returncode(licomp_status_details):
    if licomp_status_details['provisioning_status'] == 'failure':
        return ReturnCodes.LICOMP_UNSUPPORTED_PROVISIONING.value
    if licomp_status_details['usecase_status'] == 'failure':
        return ReturnCodes.LICOMP_UNSUPPORTED_USECASE.value
    if licomp_status_details['license_supported_status'] == 'failure':
        return ReturnCodes.LICOMP_UNSUPPORTED_LICENSE.value
    return ReturnCodes.LICOMP_INTERNAL_ERROR.value
