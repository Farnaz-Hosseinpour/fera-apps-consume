#-------------------------------------------------------------------------------
# Name:        cmdline.py
# Purpose:
#
# Author:      kjells
#
# Created:     12/10/2011
# Copyright:   (c) kjells 2011
#-------------------------------------------------------------------------------
import sys
import os
import argparse
import logging


def make_parser():
    ''' This is the parser for the consume_batch command line
    '''
    # - general description of the program and how to use it
    USAGE = r'''

The Consume batch calculator requires a burn type argument, either 'natural' or 'activity', and
an input file with fuelbed and environmental data. The input file can contain 1 of 2 parameter sets
depending on the burn_type specified. See input_natural.csv and input_activity.csv for examples of the
required input parameters.

Additional options are detailed below.'''

    # - example of program usage, this is printed after the generated argument descriptions
    EPILOG = '''
Examples:
    // simple case
    consume_batch.exe natural input_natural.csv

    // same thing on linux
    python consume_batch.py natural input_natural.csv

    // specify an alternative loadings file
    consume_batch.exe natural input_natural.csv -f my_loadings.xml

    // specify a column configuration file
    consume_batch.exe activity input_activity.csv -x output_summary.csv'''

    # - build the parser
    parser = argparse.ArgumentParser(
        description=USAGE,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    # - add the positional arguments
    parser.add_argument('burn_type', metavar='burn type\t(activity | natural)', nargs='?')
    parser.add_argument('csv_file', metavar='input file\t(csv format)', nargs='?')

    # - specify an alternative loadings file
    parser.add_argument('-f', action='store', nargs=1, dest='fuel_loadings_file', metavar='loadings file',
        help='Specify the fuel loadings file for consume to use. Run the FCCS batch processor over \
            the fuelbeds for which you want to generate consumption/emission results to create\
            a fuel loadings file.')

    # - customize the output column configuration
    parser.add_argument('-x', action='store', nargs=1, dest='col_cfg_file', metavar='output columns',
        help='Specify the output column configuration file for consume to use')

    # - customize the message output
    parser.add_argument('-l', action='store', nargs=1, dest='msg_level', metavar='message level',
        help='Specify the detail level of messages (1 | 2 | 3). 1 = fewest messages 3 = most messages')

    # - specify an output filename
    parser.add_argument('-o', action='store', nargs=1, default=['consume_results.csv'],
        dest='output_filename', metavar='output filename',
        help='Specify the name of the Consume output results file.'
        )
    return parser

class ConsumeParserException(Exception):
    pass

class ConsumeParser(object):
    ''' Parse the consume_batch command line arguments
    '''
    def __init__(self, pickle_string=None):
        self._pickle_string = pickle_string.lower() if pickle_string else None
        self._burn_type = None
        self._csv_file = None
        self._fuel_loadings_file = None
        self._col_cfg_file = None
        self._msg_level = logging.ERROR

    def do_parse(self, argv):
        parser = make_parser()
        argv = argv[1:] ### - remove the calling script name
        if 0 == len(argv):
            parser.parse_args(['--help'])
        else:
            args = parser.parse_args(argv)

            # - verify burn_type
            if not args.burn_type:
                raise(ConsumeParserException("\nError: A burn_type is required."))
            if 'natural' != args.burn_type and 'activity' != args.burn_type:
                raise(ConsumeParserException("\nError: The burn_type must be 'natural' or 'activity'."))
            self._burn_type = args.burn_type

            # check for valid input file
            if not args.csv_file:
                raise(ConsumeParserException("\nError: An input file in csv format is required."))
            if not self.exists(args.csv_file):
                raise(ConsumeParserException("\nError: The file '{}' does not exist.".format(args.csv_file)))
            self._csv_file = os.path.abspath(args.csv_file)

            # -  check for optional fuel loadings file
            if args.fuel_loadings_file:
                if not self.exists(args.fuel_loadings_file[0]):
                    raise(ConsumeParserException("\nError: The loadings file '{}' does not exist.".format(args.fuel_loadings_file[0])))
                self._fuel_loadings_file = os.path.abspath(args.fuel_loadings_file[0])

            if args.col_cfg_file:
                if args.col_cfg_file[0].lower() == self._pickle_string:
                    # no need to validate anything
                    self._col_cfg_file = args.col_cfg_file[0]
                else:
                    if not self.exists(args.col_cfg_file[0]):
                        raise(ConsumeParserException("\nError: The column config file '{}' does not exist.".format(args.col_cfg_file[0])))
                    self._col_cfg_file = os.path.abspath(args.col_cfg_file[0])

            if args.output_filename:
                self.output_filename = os.path.abspath(args.output_filename[0])

            if args.msg_level:
                level = int(args.msg_level[0])
                if level in [1, 2, 3]:
                    if 1 == level: self._msg_level = logging.ERROR
                    if 2 == level: self._msg_level = logging.WARNING
                    if 3 == level: self._msg_level = logging.DEBUG


    def exists(self, filename):
        return True if os.path.exists(filename) else False

    @property
    def burn_type(self): return self._burn_type
    @property
    def csv_file(self): return self._csv_file
    @property
    def col_cfg_file(self): return self._col_cfg_file
    @property
    def msg_level(self): return self._msg_level
    @property
    def fuel_loadings_file(self): return self._fuel_loadings_file


def main():
    ConsumeParser(sys.argv)

if __name__ == '__main__':
    main()
