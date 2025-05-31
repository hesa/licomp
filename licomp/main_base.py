# SPDX-FileCopyrightText: 2021 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import json
import logging
import sys

from licomp.interface import UseCase
from licomp.interface import Provisioning
from licomp.interface import Status
from licomp.return_codes import ReturnCodes
from licomp.return_codes import compatibility_status_to_returncode
from licomp.return_codes import licomp_status_to_returncode

class LicompFormatter():

    def format_compatibility(self, compatibility, verbose=False):
        return None

    def format_licenses(self, licenses, verbose=False):
        return None

    def format_usecases(self, usecases, verbose=False):
        return None

    def format_provisionings(self, provisionings, verbose=False):
        return None

    def format_error(self, error_string, verbose=False):
        return None

    @staticmethod
    def formatter(fmt):
        if fmt.lower() == 'json':
            return JsonLicompFormatter()
        if fmt.lower() == 'text':
            return TextLicompFormatter()

class JsonLicompFormatter():

    def format_compatibility(self, compatibility, verbose=False):
        return json.dumps(compatibility, indent=4)

    def format_licenses(self, licenses, verbose=False):
        return json.dumps(licenses, indent=4)

    def format_usecases(self, usecases, verbose=False):
        return json.dumps(usecases, indent=4)

    def format_provisionings(self, provisionings, verbose=False):
        return json.dumps(provisionings, indent=4)

    def format_error(self, error_string, verbose=False):
        return json.dumps({
            'status': 'failure',
            'message': error_string,
        }, indent=4)

class TextLicompFormatter():

    def format_compatibility(self, compatibility, verbose=False):
        status = compatibility['status']
        status_ok = Status.string_to_status(status) == Status.SUCCESS
        compat = compatibility['compatibility_status']
        explanation = compatibility['explanation']
        if not status_ok:
            return f'Failure: {explanation}'
        if not verbose:
            return compat
        res = []
        res.append(f'Compatibility: {compat}')
        res.append(f'Explanation:   {explanation}')
        res.append(f'Provisioning:       {compatibility["provisioning"]}')
        res.append(f'Resource:      {compatibility["resource_name"]}, {compatibility["resource_version"]}')
        return '\n'.join(res)

    def format_licenses(self, licenses, verbose=False):
        return ', '.join(licenses)

    def format_usecases(self, usecases, verbose=False):
        return ', '.join(usecases)

    def format_provisionings(self, provisionings, verbose=False):
        return ', '.join(provisionings)

    def format_error(self, error_string, verbose=False):
        return f'Error: {error_string}'

class LicompParser():

    def __init__(self, licomp, name, description, epilog, default_usecase, default_provisioning):
        self.licomp = licomp
        self.default_usecase = default_usecase
        self.default_provisioning = default_provisioning
        self.parser = argparse.ArgumentParser(prog=name,
                                              description=description,
                                              epilog=epilog,
                                              formatter_class=argparse.RawTextHelpFormatter)

        self.parser.add_argument('-v', '--verbose',
                                 action='store_true')

        self.parser.add_argument('-of', '--output-format',
                                 type=str,
                                 default='json')

        self.parser.add_argument('--name',
                                 action='store_true')

        self.parser.add_argument('--version',
                                 action='store_true')

        self.parser.add_argument('--usecase', '-u',
                                 type=str,
                                 default=UseCase.usecase_to_string(self.default_usecase),
                                 help=f'Usecase, default: {UseCase.usecase_to_string(self.default_usecase)}')

        self.parser.add_argument('--provisioning', '-p',
                                 type=str,
                                 default=Provisioning.provisioning_to_string(self.default_provisioning),
                                 help=f'Provisioning, default: {Provisioning.provisioning_to_string(self.default_provisioning)}')

        subparsers = self.parser.add_subparsers(help='Sub commands')
        self.subparsers = subparsers

        parser_v = subparsers.add_parser(
            'verify', help='Verify license compatibility between for a package or an outbound license expression against inbound license expression.')
        parser_v.set_defaults(which="verify", func=self.verify)
        parser_v.add_argument('--outbound-license', '-ol', type=str, dest='out_license', help='Outbound license expression', default=None)
        parser_v.add_argument('--inbound-license', '-il', type=str, dest='in_license', help='Inbound license expression', default=None)

        parser_va = subparsers.add_parser(
            'validate', help='Validate that the data is following the Licomp reply specification')
        parser_va.set_defaults(which="validate", func=self.validate)
        parser_va.add_argument("file_name", type=str)

        parser_sl = subparsers.add_parser(
            'supported-licenses', help='List supported licenses.')
        parser_sl.set_defaults(which="supported_licenses", func=self.supported_licenses)

        parser_st = subparsers.add_parser(
            'supported-usecases', help='List supported usecases.')
        parser_st.set_defaults(which="supported_usecases", func=self.supported_usecases)

        parser_st = subparsers.add_parser(
            'supported-provisionings', help='List supported provisionings.')
        parser_st.set_defaults(which="supported_provisionings", func=self.supported_provisionings)

    def validate(self, args):
        with open(args.file_name) as fp:
            data = json.load(fp)
            self.licomp.validate(data)
        return "", 0, None

    def verify(self, args):
        inbound = self.args.in_license
        outbound = self.args.out_license

        # check outbound
        if not outbound:
            return None, ReturnCodes.LICOMP_MISSING_ARGUMENTS.value, LicompFormatter.formatter(self.args.output_format).format_error('Outbound license missing.')

        # check inbound
        if not inbound:
            return None, ReturnCodes.LICOMP_MISSING_ARGUMENTS.value, LicompFormatter.formatter(self.args.output_format).format_error('Inbound license missing.')

        # Check usecase
        try:
            usecase = UseCase.string_to_usecase(args.usecase)
        except KeyError:
            return None, ReturnCodes.LICOMP_UNSUPPORTED_USECASE.value, LicompFormatter.formatter(self.args.output_format).format_error(f'Usecase {args.usecase} not supported.')

        # Check provisioning case
        try:
            provisioning = Provisioning.string_to_provisioning(args.provisioning)
        except KeyError:
            return None, ReturnCodes.LICOMP_UNSUPPORTED_PROVISIONING.value, LicompFormatter.formatter(self.args.output_format).format_error(f'Provisioning {args.provisioning} not supported.')

        # usecase and provisioning case are OK
        res = self.licomp.outbound_inbound_compatibility(outbound, inbound, usecase, provisioning=provisioning)
        if res['status'] == 'success':
            ret_code = compatibility_status_to_returncode(res['compatibility_status'])
        else:
            if res['status_details']:
                ret_code = licomp_status_to_returncode(res['status_details'])
            else:
                ret_code = ReturnCodes.LICOMP_UNSUPPORTED_PROVISIONING.value

        return LicompFormatter.formatter(self.args.output_format).format_compatibility(res, args.verbose), ret_code, None

    def supported_licenses(self, args):
        res = self.licomp.supported_licenses()
        return LicompFormatter.formatter(self.args.output_format).format_licenses(res), ReturnCodes.LICOMP_OK.value, None

    def supported_usecases(self, args):
        usecases = [UseCase.usecase_to_string(x) for x in self.licomp.supported_usecases()]
        return LicompFormatter.formatter(self.args.output_format).format_usecases(usecases), ReturnCodes.LICOMP_OK.value, None

    def supported_provisionings(self, args):
        provisionings = [Provisioning.provisioning_to_string(x) for x in self.licomp.supported_provisionings()]
        return LicompFormatter.formatter(self.args.output_format).format_provisionings(provisionings), ReturnCodes.LICOMP_OK.value, None

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def sub_parsers(self):
        return self.subparsers

    def run_noexit(self):

        # a bit ugly hack to replace argparse's return value
        # with custom for parse error
        try:
            self.args = self.parser.parse_args()
        except SystemExit as e:
            exit_code = e.code
            logging.debug(f'exit code from parser: {exit_code}')
            if not exit_code:
                sys.exit(0)
            sys.exit(ReturnCodes.LICOMP_PARSE_ERROR.value)

        # --name
        if self.args.name:
            print(self.licomp.name())
            sys.exit(0)

        # --version
        if self.args.version:
            print(self.licomp.version())
            sys.exit(0)

        # if missing command
        if 'func' not in vars(self.args):
            print("Error: missing command", file=sys.stderr)
            self.parser.print_help(file=sys.stderr)
            sys.exit(1)

        # if --verbose
        if self.args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        # execute command
        res, code, err = self.args.func(self.args)
        return res, code, err, self.args.func

    def run(self):
        res, code, err, func = self.run_noexit()

        if err:
            print(err, file=sys.stderr)
            sys.exit(code)

        # print (formatted) result
        print(res)

        return code
