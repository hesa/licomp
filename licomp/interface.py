from enum import Enum

class ObligationTrigger(Enum):
    SOURCE_DIST = 1
    BIN_DIST = 2
    SNIPPET = 3
    LOCAL_USE = 4
    PROVIDE_SERVICE = 5
    PROVIDE_WEBUI = 6
    
class ModifiedTrigger(Enum):
    MODIFIED = 1
    UNMODIFIED = 2

class CompatibilityStatus(Enum):
    COMPATIBLE = 1
    INCOMPATIBLE = 2
    DEPENDS = 3
    UNKNOWN = 4
    UNSUPPORTED = 5

class Status(Enum):
    SUCCESS = 1
    FAILURE = 10

class LicompException(Exception):
    pass

class Licomp:

    def __init__(self):
        self.obligation_trigger_strings = {
            ObligationTrigger.SOURCE_DIST: "source-code-distribution",
            ObligationTrigger.BIN_DIST: "binary-distribution",
            ObligationTrigger.SNIPPET: "snippet",
            ObligationTrigger.LOCAL_USE: "local-use",
            ObligationTrigger.PROVIDE_SERVICE: "provide-service",
            ObligationTrigger.PROVIDE_WEBUI: "provide-webui"
        }
    
        self.obligation_string_triggers = {
            "source-code-distribution":  ObligationTrigger.SOURCE_DIST,
            "binary-distribution":       ObligationTrigger.BIN_DIST,
            "snippet":                   ObligationTrigger.SNIPPET,
            "local-use":                 ObligationTrigger.LOCAL_USE,
            "provide-service":           ObligationTrigger.PROVIDE_SERVICE,
            "provide-webui":             ObligationTrigger.PROVIDE_WEBUI,
        }
    
        self.modified_strings = {
            ModifiedTrigger.MODIFIED: "modified",
            ModifiedTrigger.UNMODIFIED: "unmodified"
        }
    
        self.compatibility_status_strings = {
            CompatibilityStatus.COMPATIBLE:   "Yes",
            CompatibilityStatus.INCOMPATIBLE: "No",
            CompatibilityStatus.DEPENDS:      "Depends",
            CompatibilityStatus.UNKNOWN:      "Unknown",
            CompatibilityStatus.UNSUPPORTED:  "Unsupported",
            None:  None
        }
        
        self.status_strings = {
            Status.SUCCESS: "success",
            Status.FAILURE: "fail"
        }

    def name(self):
        return None
    
    def version(self):
        return None
    
    def obligation_trigger_string(self, trigger):
        return self.obligation_trigger_strings[trigger]
        
    def obligation_string_trigger(self, trigger_str):
        return self.obligation_string_triggers[trigger_str]
        
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
            ret =  self.compatibility_reply(Status.FAILURE,
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
            "status": self.status_strings[status],
            "outbound": outbound,
            "inbound": inbound,
            "trigger": self.obligation_trigger_strings[trigger],
            "modified": self.modified_strings[modified],
            "compatibility_status": self.compatibility_status_strings[compatibility_status],
            "explanation": explanation,
            "resource_name": self.name(),
            "resource_version": self.version(),
        }

    def check_trigger(self,trigger):
        if trigger not in self.supported_triggers():
            explanation = f'{self.obligation_trigger_string(trigger)} not supported'
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

