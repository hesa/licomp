# SPDX-FileCopyrightText: 2021 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum

from licomp.config import licomp_version

class Status(Enum):
    SUCCESS = 1
    FAILURE = 10

    @staticmethod
    def string_to_status(status_string):
        _map = {
            "success": Status.SUCCESS,
            "failure": Status.FAILURE,
        }
        return _map[status_string]

    @staticmethod
    def status_to_string(status):
        _map = {
            Status.SUCCESS: "success",
            Status.FAILURE: "failure",
        }
        return _map[status]

class Modification(Enum):
    MODIFIED = 20
    UNMODIFIED = 21

    @staticmethod
    def modification_to_string(modification):
        _map = {
            Modification.MODIFIED: "modified",
            Modification.UNMODIFIED: "unmodified",
        }
        return _map[modification]


class CompatibilityStatus(Enum):
    COMPATIBLE = 41
    INCOMPATIBLE = 42
    DEPENDS = 43
    UNKNOWN = 44
    UNSUPPORTED = 45

    @staticmethod
    def string_to_compat_status(compat_status_string):
        _map = {
            "yes": CompatibilityStatus.COMPATIBLE,
            "no": CompatibilityStatus.INCOMPATIBLE,
            "depends": CompatibilityStatus.DEPENDS,
            "unknown": CompatibilityStatus.UNKNOWN,
            "unsupported": CompatibilityStatus.UNSUPPORTED,
            None: None,
        }
        return _map[compat_status_string]

    @staticmethod
    def compat_status_to_string(compat_status):
        _map = {
            CompatibilityStatus.COMPATIBLE: "yes",
            CompatibilityStatus.INCOMPATIBLE: "no",
            CompatibilityStatus.DEPENDS: "depends",
            CompatibilityStatus.UNKNOWN: "unknown",
            CompatibilityStatus.UNSUPPORTED: "unsupported",
            None: None,
        }
        return _map[compat_status]

class UseCase(Enum):
    LIBRARY = 51
    COMPILER = 52
    SNIPPET = 53
    TOOL = 54
    TEST = 55

    @staticmethod
    def string_to_usecase(usecase):
        _map = {
            "library": UseCase.LIBRARY,
            "compiler": UseCase.COMPILER,
            "snippet": UseCase.SNIPPET,
            "tool": UseCase.TOOL,
            "test": UseCase.TEST,
        }
        return _map[usecase]

    @staticmethod
    def usecase_to_string(usecase):
        _map = {
            UseCase.LIBRARY: "library",
            UseCase.COMPILER: "compiler",
            UseCase.SNIPPET: "snippet",
            UseCase.TOOL: "tool",
            UseCase.TEST: "test",
        }
        return _map[usecase]

class Provisioning(Enum):
    SOURCE_DIST = 61
    BIN_DIST = 62
    LOCAL_USE = 63
    SERVICE = 64
    WEBUI = 65

    @staticmethod
    def string_to_provisioning(provisioning):
        _map = {
            "source-code-distribution": Provisioning.SOURCE_DIST,
            "binary-distribution": Provisioning.BIN_DIST,
            "local-use": Provisioning.LOCAL_USE,
            "provide-service": Provisioning.SERVICE,
            "provide-webui": Provisioning.WEBUI,
        }
        return _map[provisioning]

    @staticmethod
    def provisioning_to_string(provisioning):
        _map = {
            Provisioning.SOURCE_DIST: "source-code-distribution",
            Provisioning.BIN_DIST: "binary-distribution",
            Provisioning.LOCAL_USE: "local-use",
            Provisioning.SERVICE: "provide-service",
            Provisioning.WEBUI: "provide-webui",
        }
        return _map[provisioning]

class LicompException(Exception):
    pass

class Licomp:

    def __init__(self):
        pass

    @staticmethod
    def api_version():
        return licomp_version

    def name(self):
        return None

    def version(self):
        return None

    def supported_api_version(self):
        return None

    def outbound_inbound_compatibility(self,
                                       outbound,
                                       inbound,
                                       usecase=UseCase.LIBRARY,
                                       provisioning=Provisioning.BIN_DIST,
                                       modification=Modification.UNMODIFIED):

        try:
            # Check if the usecase, provisioning, modifications is not supported
            self.check_triggers(usecase, provisioning, modification)

            # Make sure both licenses are supported
            ret = self.__licenses_supported(inbound, outbound, usecase, provisioning, modification)
            if ret:
                return ret
            # Check if the licenses are the same
            ret = self.__licenses_same(inbound, outbound, usecase, provisioning, modification)
            if ret:
                return ret

            response = self._outbound_inbound_compatibility(outbound,
                                                            inbound,
                                                            usecase,
                                                            provisioning,
                                                            modification)
            compat_status = response['compatibility_status']
            explanation = response['explanation']
            ret = self.compatibility_reply(Status.SUCCESS,
                                           outbound,
                                           inbound,
                                           usecase,
                                           provisioning,
                                           modification,
                                           compat_status,
                                           explanation)
            return ret
        except AttributeError as e:
            raise e
        except TypeError as e:
            raise e
        except (KeyError, LicompException) as e:
            return self.failure_reply(e,
                                      outbound,
                                      inbound,
                                      usecase,
                                      provisioning,
                                      modification)

    def compatibility_reply(self,
                            status,
                            outbound,
                            inbound,
                            usecase,
                            provisioning,
                            modification,
                            compatibility_status,
                            explanation):

        return {
            "status": Status.status_to_string(status),
            "outbound": outbound,
            "inbound": inbound,
            "usecase": UseCase.usecase_to_string(usecase),
            "provisioning": Provisioning.provisioning_to_string(provisioning),
            "modification": Modification.modification_to_string(modification),
            "compatibility_status": CompatibilityStatus.compat_status_to_string(compatibility_status),
            "explanation": explanation,
            "resource_name": self.name(),
            "resource_version": self.version(),
        }

    def __licenses_supported(self, inbound, outbound, usecase, provisioning, modification):
        unsupported = set()
        if outbound not in self.supported_licenses():
            unsupported.add(outbound)
        if inbound not in self.supported_licenses():
            unsupported.add(inbound)
        if len(unsupported) > 0:
            return self.compatibility_reply(Status.FAILURE,
                                            outbound,
                                            inbound,
                                            usecase,
                                            provisioning,
                                            modification,
                                            CompatibilityStatus.UNSUPPORTED,
                                            f'Unsupported licenses: {", ".join(unsupported)}.')

    def __licenses_same(self, inbound, outbound, usecase, provisioning, modification):
        if outbound == inbound:
            return self.compatibility_reply(Status.SUCCESS,
                                            outbound,
                                            inbound,
                                            usecase,
                                            provisioning,
                                            modification,
                                            CompatibilityStatus.COMPATIBLE,
                                            f'Inbound and outbound license are the same: {outbound}')

    def check_triggers(self, usecase, provisioning, modification):
        if provisioning not in self.supported_provisionings():
            explanation = f'Provisioning "{Provisioning.provisioning_to_string(provisioning)}" not supported'
            raise LicompException(explanation)

        if usecase not in self.supported_usecases():
            explanation = f'Use case "{UseCase.usecase_to_string(usecase)}" not supported'
            raise LicompException(explanation)

    def failure_reply(self,
                      exception,
                      outbound,
                      inbound,
                      usecase,
                      provisioning,
                      modification):

        explanation = None
        if exception:
            exception_type = type(exception)
            if exception_type == KeyError:
                unsupported = ', '.join([x for x in [inbound, outbound] if not self.license_supported(x)])
                explanation = f'Unsupported license(s) found: {unsupported}'
            if exception_type == LicompException:
                explanation = str(exception)

        return self.compatibility_reply(Status.FAILURE,
                                        outbound,
                                        inbound,
                                        usecase,
                                        provisioning,
                                        modification,
                                        None,
                                        explanation)

    def supported_licenses(self):
        return None

    def supported_usecases(self):
        return None

    def supported_provisionings(self):
        return None

    def license_supported(self, license_name):
        return license_name in self.supported_licenses()

    def usecase_supported(self, usecase):
        return usecase in self.supported_usecases()

    def provisioning_supported(self, provisioning):
        return provisioning in self.supported_provisionings()

    def _outbound_inbound_compatibility(self, compat_status, explanation):
        """
        must be implemented by subclasses
        """
        return None

    def outbound_inbound_reply(self, compat_status, explanation):
        return {
            'compatibility_status': compat_status,
            'explanation': explanation,
        }
