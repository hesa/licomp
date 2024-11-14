from enum import Enum

class ObligationTrigger(Enum):
    SOURCE_DIST = 1
    BIN_DIST = 2
    SNIPPET = 3
    LOCAL_USE = 4
    PROVIDE_SERVICE = 5
    PROVIDE_WEBUI = 6

    @staticmethod
    def string_to_trigger(trigger_string):
        map = {
            "source-code-distribution":  ObligationTrigger.SOURCE_DIST,
            "binary-distribution":       ObligationTrigger.BIN_DIST,
            "snippet":                   ObligationTrigger.SNIPPET,
            "local-use":                 ObligationTrigger.LOCAL_USE,
            "provide-service":           ObligationTrigger.PROVIDE_SERVICE,
            "provide-webui":             ObligationTrigger.PROVIDE_WEBUI,
        }
        return map[trigger_string]

    @staticmethod
    def trigger_to_string(trigger):
        map = {
            ObligationTrigger.SOURCE_DIST: "source-code-distribution",
            ObligationTrigger.BIN_DIST: "binary-distribution",
            ObligationTrigger.SNIPPET: "snippet",
            ObligationTrigger.LOCAL_USE: "local-use",
            ObligationTrigger.PROVIDE_SERVICE: "provide-service",
            ObligationTrigger.PROVIDE_WEBUI: "provide-webui"
        }
        return map[trigger]
    
class ModifiedTrigger(Enum):
    MODIFIED = 1
    UNMODIFIED = 2
    @staticmethod
    def modified_to_string(modified):
        map = {
            ModifiedTrigger.MODIFIED: "modified",
            ModifiedTrigger.UNMODIFIED: "unmodified"
        }
        return map[modified]

class CompatibilityStatus(Enum):
    COMPATIBLE = 1
    INCOMPATIBLE = 2
    DEPENDS = 3
    UNKNOWN = 4
    UNSUPPORTED = 5
    @staticmethod
    def compatibility_to_string(compatibility):
        map = {
            CompatibilityStatus.COMPATIBLE:   "yes",
            CompatibilityStatus.INCOMPATIBLE: "no",
            CompatibilityStatus.DEPENDS:      "depends",
            CompatibilityStatus.UNKNOWN:      "unknown",
            CompatibilityStatus.UNSUPPORTED:  "unsupported",
            None:  None
        }
        return map[compatibility]
    

class Status(Enum):
    SUCCESS = 1
    FAILURE = 10

    @staticmethod
    def string_to_status(status_string):
        map = {
            "success": Status.SUCCESS,
            "failue": Status.FAILURE,
        }
        return map[status_string]

    @staticmethod
    def status_to_string(status):
        map = {
            Status.SUCCESS: "success",
            Status.FAILURE: "failue",
        }
        return map[status]

class LicompException(Exception):
    pass

class Licomp:

    def __init__(self):
        pass

    def name(self):
        return None
    
    def version(self):
        return None
    
    def outbound_inbound_compatibility(self,
                                       outbound,
                                       inbound,
                                       trigger=ObligationTrigger.BIN_DIST,
                                       modified=ModifiedTrigger.UNMODIFIED):
        try:
            self.check_trigger(trigger)

            response = self._outbound_inbound_compatibility(outbound, inbound,
                                                            trigger, modified)
            compat_status = response['compatibility_status']
            explanation = response['explanation']
            ret =  self.compatibility_reply(Status.SUCCESS,
                                            outbound,
                                            inbound,
                                            trigger,
                                            modified,
                                            compat_status,
                                            explanation)
            return ret
        except AttributeError as e:
            raise e
        except TypeError as e:
            raise e
        except Exception as e:
            return self.failure_reply(e,
                                      outbound,
                                      inbound,
                                      trigger,
                                      modified)

    def compatibility_reply(self,
                            status,
                            outbound,
                            inbound,
                            trigger,
                            modified,
                            compatibility_status,
                            explanation):

        return {
            "status": Status.status_to_string(status),
            "outbound": outbound,
            "inbound": inbound,
            "trigger": ObligationTrigger.trigger_to_string(trigger),
            "modified": ModifiedTrigger.modified_to_string(modified),
            "compatibility_status": CompatibilityStatus.compatibility_to_string(compatibility_status),
            "explanation": explanation,
            "resource_name": self.name(),
            "resource_version": self.version(),
        }

    def check_trigger(self,trigger):
        if trigger not in self.supported_triggers():
            explanation = f'Trigger "{ObligationTrigger.trigger_to_string(trigger)}" not supported'
            raise LicompException(explanation)
        

    def failure_reply(self,
                      exception,
                      outbound,
                      inbound,
                      trigger,
                      modified):

        explanation = None
        if exception:
            exception_type = type(exception)
            if exception_type == KeyError:
                unsupported = ', '.join([x for x in [inbound, outbound] if not self.license_supported(x) ])
                explanation = f'Unsupported license(s) found: {unsupported}'
            if exception_type == LicompException:
                explanation = str(exception)

        return self.compatibility_reply(Status.FAILURE,
                                        outbound,
                                        inbound,
                                        trigger,
                                        modified,
                                        None,
                                        explanation)

    def supported_licenses(self):
        return None

    def supported_triggers(self):
        return None

    def license_supported(self, license_name):
        return license_name in self.supported_licenses()

    def trigger_supported(self, trigger):
        return trigger in self.supported_triggers()
    
    def outbound_inbound_reply(self, compat_status, explanation):
        """
        must be implemented by subclasses
        """
        return None
    
    def outbound_inbound_reply(self, compat_status, explanation):
        return {
            'compatibility_status': compat_status,
            'explanation': explanation
        }

