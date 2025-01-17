# Licomp Comand Line Interface

Licomp itself does not have any data to make a command line relevant. However, licomp has functionality that Licomp resources (implementing the [Licomp interface](https://github.com/hesa/licomp/blob/main/docs/python-api.md)). Licomp provides a generic command line interface, used by the Licomp resources, described below.

The whole purpose of licomp is to determine comptibility between an outbound and an inbound license. The command to check this is `verify`.

# Commands

## verify

Verify license compatibility between for a package or an outbound license expression against inbound license expression.

### Return values

* `0` - compatible, i.e. inbound license can be used with outbound license
* `2` - incompatible, i.e. inbound license can not be used with outbound license
* `3` - depends, i.e. whether inbound license can be used with outbound license needs to be determined by a lawyer
* `4` - unknown, i.e. whether inbound license can not be used with outbound license is unknown
* `5` - unsupported, i.e. one (or both) of the licenses are not supported
* `10` - internal, an internal error occurred

## supported-licenses

List supported licenses.

### Return values

* `0` - for success
* `10` - internal, an internal error occured

## supported-usecases

List supported usecases.

### Return values

* `0` - for success
* `10` - internal, an internal error occured

## supported-provisionings

List supported provisionings.

### Return values

* `0` - for success
* `10` - internal, an internal error occured
