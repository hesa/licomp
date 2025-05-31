# SPDX-FileCopyrightText: 2021 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum
import logging
import json
import jsonschema
import os

from licomp.config import licomp_api_version

SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
SCHEMA_FILE = os.path.join(DATA_DIR, 'reply_schema.json')


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

    def __init__(self, message, return_code):
        super().__init__(message)
        self.return_code = return_code

class Licomp:

    def __init__(self):
        self.__check_api()
        pass

    def __check_api(self):
        base_api_version = self.api_version()
        subclass_api_version = self.supported_api_version()
        if (base_api_version) > (subclass_api_version):
            raise LicompException(f'API version mismatch between Licomp ({base_api_version}) and {self.name()} ({subclass_api_version}).')

    @staticmethod
    def api_version():
        return licomp_api_version

    @staticmethod
    def json_schema():
        with open(SCHEMA_FILE) as fp:
            return json.load(fp)

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
            total_status = Status.SUCCESS
            provisioning_status = Status.SUCCESS
            usecase_status = Status.SUCCESS
            license_supported_status = Status.SUCCESS
            explanations = []

            # Check if the usecase, provisioning, modifications is not supported
            if provisioning not in self.supported_provisionings():
                explanations.append(f'Provisioning "{Provisioning.provisioning_to_string(provisioning)}" not supported')
                provisioning_status = Status.FAILURE
                total_status = Status.FAILURE

            if usecase not in self.supported_usecases():
                explanations.append(f'Use case "{UseCase.usecase_to_string(usecase)}" not supported')
                usecase_status = Status.FAILURE
                total_status = Status.FAILURE

            # Make sure both licenses are supported
            ret = self.__licenses_supported(inbound, outbound, usecase, provisioning, modification)
            if ret:
                explanations.append(ret)
                license_supported_status = Status.FAILURE
                total_status = Status.FAILURE

            if total_status == Status.SUCCESS:

                # Check if the licenses are the same
                ret = self.__licenses_same(inbound, outbound, usecase, provisioning, modification)
                if ret:
                    explanation = ret
                    compat_status = CompatibilityStatus.COMPATIBLE

                else:
                    response = self._outbound_inbound_compatibility(outbound,
                                                                    inbound,
                                                                    usecase,
                                                                    provisioning,
                                                                    modification)

                    # A license can be supported one way but not the other
                    # e.g. a resource can support license A and B, but
                    # only     A -> B
                    # and not  B -> A
                    # so double check license support after response from resource
                    if response['compatibility_status'] == CompatibilityStatus.UNSUPPORTED:
                        license_supported_status = Status.FAILURE
                        total_status = Status.FAILURE
                        logging.debug(f'licmp: adjusting compat to failure, since: {response["compatibility_status"]}')
                        pass

                    compat_status = response['compatibility_status']
                    explanation = response['explanation']
            else:
                compat_status = None
                explanation = None

            status_details = {
                'provisioning_status': Status.status_to_string(provisioning_status),
                'usecase_status': Status.status_to_string(usecase_status),
                'license_supported_status': Status.status_to_string(license_supported_status),
            }

            ret = self.compatibility_reply(total_status,
                                           status_details,
                                           outbound,
                                           inbound,
                                           usecase,
                                           provisioning,
                                           modification,
                                           compat_status,
                                           explanation,
                                           self.disclaimer())
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
                            status_details,
                            outbound,
                            inbound,
                            usecase,
                            provisioning,
                            modification,
                            compatibility_status,
                            explanation,
                            disclaimer):

        return {
            "status": Status.status_to_string(status),
            "status_details": status_details,
            "outbound": outbound,
            "inbound": inbound,
            "usecase": UseCase.usecase_to_string(usecase),
            "provisioning": Provisioning.provisioning_to_string(provisioning),
            "modification": Modification.modification_to_string(modification),
            "compatibility_status": CompatibilityStatus.compat_status_to_string(compatibility_status),
            "explanation": explanation,
            "api_version": self.api_version(),
            "resource_name": self.name(),
            "data_url": self.data_url(),
            "resource_url": self.url(),
            "resource_version": self.version(),
            "resource_disclaimer": disclaimer,
        }

    def __licenses_supported(self, inbound, outbound, usecase, provisioning, modification):
        unsupported = set()
        if outbound not in self.supported_licenses():
            unsupported.add(outbound)
        if inbound not in self.supported_licenses():
            unsupported.add(inbound)
        if len(unsupported) > 0:
            return f'Unsupported licenses: {", ".join(unsupported)}.'

    def __licenses_same(self, inbound, outbound, usecase, provisioning, modification):
        if outbound == inbound:
            return f'Inbound and outbound license are the same: {outbound}'

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
                                        {},
                                        outbound,
                                        inbound,
                                        usecase,
                                        provisioning,
                                        modification,
                                        None,
                                        explanation,
                                        self.disclaimer())

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

    def disclaimer(self):
        return None

    def url(self):
        return None

    def data_url(self):
        return None

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

    def validate(self, content):
        with open(SCHEMA_FILE) as fp:
            schema = json.load(fp)

            jsonschema.validate(instance=content,
                                schema=schema)
