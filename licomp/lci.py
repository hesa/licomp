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
    COMPATIBLE = 1
    INCOMPATIBLE = 2
    DEPENDS = 3
    UNKNOWN = 4
    UNSUPPORTED = 5

class LicenseCompatibilityInterface:

    def __init__(self):
        self.obligation_trigger_strings = {
            ObligationTrigger.SOURCE_DIST: "source-code-distribution",
            ObligationTrigger.BIN_DIST: "binary-distribution",
            ObligationTrigger.SNIPPET: "snippet",
            ObligationTrigger.LOCAL_USE: "local-use",
            ObligationTrigger.PROVIDE_SERVICE: "provide-service",
            ObligationTrigger.PROVIDE_WEBUI: "provide-webui"
        }
    
        self.modified_strings = {
            ModifiedTrigger.MODIFIED: "modified",
            ModifiedTrigger.UNMODIFIED: "unmodified"
        }
    
        self.status_strings = {
            CompatibilityStatus.COMPATIBLE:   "Yes",
            CompatibilityStatus.INCOMPATIBLE: "No",
            CompatibilityStatus.DEPENDS:      "Depends",
            CompatibilityStatus.UNKNOWN:      "Unknown",
            CompatibilityStatus.UNSUPPORTED:  "Unsupported"
        }

    def obligation_trigger_string(self, trigger):
        return self.obligation_trigger_strings[trigger]
        
    def outbound_inbound_compatibility(self,
                                       outbound,
                                       inbound,
                                       trigger=ObligationTrigger.BIN_DIST,
                                       modified=ModifiedTrigger.UNMODIFIED):
        return None

    def compatibility_reply(self,
                            status,
                            outbound,
                            inbound,
                            trigger,
                            modified,
                            compatibility_status,
                            explanation):
        return {
            "outbound": outbound,
            "inbound": inbound,
            "trigger": self.obligation_trigger_strings[trigger],
            "modified": self.modified_strings[modified],
            "compatibility_status": self.status_strings[status],
            "explanation": explanation,
        }

    def supported_licenses(self):
        return None

    def supported_triggers(self):
        return None

    def license_supported(self, license_name):
        return license_name in self.supported_licenses()

    def trigger_supported(self, trigger):
        return trigger in self.supported_triggers()


