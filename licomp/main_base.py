# SPDX-FileCopyrightText: 2021 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import json
import logging
import sys

from licomp.interface import ObligationTrigger
from licomp.interface import Status


class LicompFormatter():

    def format_compatibility(self, compatibility, verbose=False):
        return None

    def format_licenses(self, licenses, verbose=False):
        return None

    def format_error(self, error_string, verbose=False):
        return None

    @staticmethod
    def formatter(format):
        if format.lower() == 'json':
            return JsonLicompFormatter()
        if format.lower() == 'text':
            return TextLicompFormatter()
    
class JsonLicompFormatter():

    def format_compatibility(self, compatibility, verbose=False):
        return json.dumps(compatibility, indent=4)

    def format_licenses(self, licenses, verbose=False):
        return json.dumps(licenses, indent=4)

    def format_triggers(self, triggers, verbose=False):
        return json.dumps(triggers, indent=4)

    def format_error(self, error_string, verbose=False):
        return json.dumps({
            'status': 'failure',
            'message': error_string
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
        res.append(f'Compatibility: {status}')
        res.append(f'Explanation:   {explanation}')
        res.append(f'Trigger:       {compatibility["trigger"]}')
        res.append(f'Resource:      {compatibility["resource_name"]}, {compatibility["resource_version"]}')
                
        return '\n'.join(res)

    def format_licenses(self, licenses, verbose=False):
        return ', '.join(licenses)

    def format_triggers(self, triggers, verbose=False):
        return ', '.join(triggers)

    def format_error(self, error_string, verbose=False):
        return f'Error: {error_string}'
    
class LicompParser():

    def __init__(self, licomp, name, description, epilog, default_trigger):
        self.licomp = licomp
        self.default_trigger = default_trigger
        self.parser = argparse.ArgumentParser(
            prog=name,
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

        self.parser.add_argument('--trigger', '-t',
                                 type=str,
                                 default=ObligationTrigger.trigger_to_string(self.default_trigger),
                                 help=f'Provisioning trigger, default: {ObligationTrigger.trigger_to_string(self.default_trigger)}')

        subparsers = self.parser.add_subparsers(help='Sub commands')
        
        parser_v = subparsers.add_parser(
            'verify', help='Verify license compatibility between for a package or an outbound license expression against inbound license expression.')
        parser_v.set_defaults(which="verify", func=self.verify)
        parser_v.add_argument('--outbound-license', '-ol', type=str, dest='out_license', help='Outbound license expressions', default=None)
        parser_v.add_argument('--inbound-license', '-il', type=str, dest='in_license', help='Inbound license expression', default=None)

        parser_sl = subparsers.add_parser(
            'supported-licenses',help='List supported licenses.')
        parser_sl.set_defaults(which="supported_licenses", func=self.supported_licenses)

        parser_st = subparsers.add_parser(
            'supported-triggers', help='List supported triggers.')
        parser_st.set_defaults(which="supported_triggers", func=self.supported_triggers)

    def verify(self, args):
        inbound = self.args.in_license
        outbound = self.args.out_license
        try:
            trigger = ObligationTrigger.string_to_trigger(args.trigger)
        except:
            return None, LicompFormatter.formatter(self.args.output_format).format_error(f'Trigger {args.trigger} not supported.')
        res = self.licomp.outbound_inbound_compatibility(outbound, inbound, trigger=trigger)
        return LicompFormatter.formatter(self.args.output_format).format_compatibility(res, args.verbose), None
        
    def supported_licenses(self, args):
        res = self.licomp.supported_licenses()
        return LicompFormatter.formatter(self.args.output_format).format_licenses(res), None
        
    def supported_triggers(self, args):
        triggers = [ObligationTrigger.trigger_to_string(x) for x in self.licomp.supported_triggers()]
        return LicompFormatter.formatter(self.args.output_format).format_triggers(triggers), None

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def run(self):
        self.args = self.parser.parse_args()

        # --name
        if self.args.name:
            print(self.licomp.name())
            sys.exit(0)

        # --version
        if self.args.version:
            print(self.licomp.version())
            sys.exit(0)

        # if missing command
        if not 'func' in vars(self.args):
            print("Error: missing command", file=sys.stderr)
            self.parser.print_help(file=sys.stderr)
            sys.exit(1)

        # if --verbose
        if self.args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)


        # execute command
        res, err = self.args.func(self.args)
        if err:
            print(err, file=sys.stderr)
            sys.exit(1)

        # print (formatted) result
        print(res)
