# Licomp Reply Format

# Example output (version 0.3)

```
/licomp verify -il BSD-3-Clause -ol GPL-2.0-only
{
    "status": "success",
    "status_details": {
        "provisioning_status": "success",
        "usecase_status": "success",
        "license_supported_status": "success"
    },
    "outbound": "GPL-2.0-only",
    "inbound": "BSD-3-Clause",
    "usecase": "library",
    "provisioning": "binary-distribution",
    "modification": "unmodified",
    "compatibility_status": "yes",
    "explanation": "some stupid explanation",
    "api_version": "0.3",
    "resource_name": "DummyLicense",
    "resource_version": "version sth",
    "resource_disclaimer": "example disclaimer"
}
```

# Reply details

## Status

Overall status of the reply to your request. Can be either:
* `success` - the request was understood and an answer is available
* `failure`- at least one of the inputs was invalid, and thus an answer is not available

## Status details

If the overall status is `failure`, then at least one of the below is a also a `failure`. This detailed status gives you an hint of what was incorrect.

### provisioning_status

* `success` - the supplied provisioning case is correct
* `failure`-  the supplied provisioning case is incorrect

### usecase_status

* `success` - the supplied usecase is correct
* `failure`-  the supplied usecase is incorrect

### license_supported_status

* `success` - both of the supplied license are supported
* `failure` -  at least one of the supplied license is not supported

## Outbound

The supplied outbound license.

## Inbound

The supplied inbound license.

## Usecase

The supplied usecase.

## Provisioning

The supplied provisioning case.

## Modification

The supplied modification. This is currently not implemented and thus discarded.

## Compatibility_status

The compatibility status for your request.

Compatibility statuses:
* `yes` - the inbound license is compatible the outbound license (see note below)
* `no` - the inbound license is NOT compatible the outbound license (see note below)
* `depends` - the inbound license compatibility to the outbound license could not be determined and need manual review (see notes below)
* `unknown`  - the inbound license is compatible the outbound license (see note below)
* `unsupported` - at least one of the licenses are not supported. This may happen if the licomp resource only can provide an answer one way (license A against license B, but not the other way around)

__Note: The above compatibility status depend on the supplied usecase, provisioning, modification (currently not implemeted, and discarded)__

## Explanation

An explanation to what went wrong. Typically for use in interaction with a user.

## Api_version

The version of the api and format as provided by Licomp.

## Resource_name

The name of the Licomp resource providing the compatibility data.

## Resource_version

The verison of the Licomp resource providing the compatibility data.

## Resource_disclaimer

The disclaimer of the Licomp resource providing the compatibility data.








