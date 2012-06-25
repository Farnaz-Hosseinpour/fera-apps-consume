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

def print_default_column_config_xml(filename):
    ''' output the text for a default column configuration file
    '''
    DEFAULT_XML = r'''
<!--
This file allows you to customize the consume output results.

There are 4 top-level catagories. Display or exclude the data from the catagory by
setting the "include" attribute to "yes" or "no".

The data from the heat release, emissions, and combustion catagories can be
displayed 2 different ways. The "detail" attribute is responsible for this choice.
Choose "all" to see the data in flaming, smoldering, residual, and total columns.
Choose "total" to limit the display to simply the total column.

When generated this file reflects the application defaults.

Be mindful that regenerating this file will overwrite any changes you have made.
Save the file to a name of your choice to avoid having it overwritten.
-->

<consume_output>
    <!-- Include the parameters data? yes/no. -->
    <parameters_column include="yes" />

    <!-- Include the heat release data? yes/no. How much detail? all/total. -->
    <heat_release_column include="no" detail="all" />

    <!-- Include the emissions data? yes/no. How much detail? all/total. -->
    <emissions_column include="no" detail="all">
        <stratum_column  include="no" detail="total"  />
    </emissions_column>

    <!-- Include the consumption data? yes/no. How much detail? all/total. -->
    <consumption_column include="yes" detail="total"  />
</consume_output>
    '''
    with open(filename, 'w') as outfile:
        for line in DEFAULT_XML:
            outfile.write(line)
        print("\nSuccess: Consume column configuration file written - {}\n".format(filename))

def make_parser():
    USAGE = r'''
Generate consumption, emissions, and heat release data.

The Consume batch calculator can be used 2 different ways and with a number of different
options. In either case, an input file specifying additional parameters is necessary.

1.) Prompt for inputs. This path will interactively prompt for required input data.

2.) Supply all inputs via command line arguments. As mentioned above, the only required argument 
is an input file in comma-separated (csv) format. The input file can contain 1 of 2 parameter sets
depending on the burn_type specified. See input_natural.csv and input_activity.csv for examples of the
required input parameters.

Additional options, detailed below, are available when all inputs are specified via command line arguments.
    '''
    parser = argparse.ArgumentParser(
        description=USAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    # - required parameter
    parser.add_argument('-c', action='store', nargs=1, dest='csv_file', required=True,
        help='REQUIRED - Specify the csv input file. See input_natural.csv and input_activity.csv \
        for examples of the required parameter sets')

    # - invoke the prompt-for-input path
    parser.add_argument('-p', action='store_true', dest='do_prompt', default=False,
        help='Prompt for required inputs (burn_type, input file, 1000hr fuel moisture (activity))')

    # - specify an alternative loadings file
    parser.add_argument('-f', action='store', nargs=1, dest='fuel_loadings_file',
        help='Specify the fuel loadings file for consume to use. Run the FCCS batch processor over \
            the fuelbeds for which you want to generate consumption/emission results to create\
            a fuel loadings file.')

    # - customize the output column configuration
    parser.add_argument('-x', action='store', nargs=1, dest='col_cfg_file',
        help='Specify the output column configuration file for consume to use')

    # - generate a default column configuration file from which to work
    parser.add_argument('-g', action='store', nargs='?',
        default="", const="output_config.xml", dest='gen_col_cfg',
        help='This option will print a default column configuration xml file. The output file is \
            called \"output_config.xml\". Modify this file as needed and save it to another name. \
            Each time the -g option is run the configuration file is overwritten.'
        )
    return parser

class ConsumeParser(object):
    def __init__(self, argv):
        self._csv_file = None
        self._col_cfg_file = None
        self._fuel_loadings_file = None
        parser = make_parser()
        if 1 == len(argv):
            parser.parse_args(['--help'])
        else:
            args = parser.parse_args(argv[1:])
            print(args)

            # Generate a column configuration file
            if args.gen_col_cfg:
                print_default_column_config_xml(args.gen_col_cfg)
                sys.exit(0)

            if args.do_prompt:
                print('\nPrompting for required inputs...')
                sys.exit(0)

            # check for valid input file and optional fuel loadings file
            if args.csv_file:
                if self.exists(args.csv_file[0]):
                    self._csv_file = os.path.abspath(args.csv_file[0])
                if args.fuel_loadings_file:
                    if self.exists(args.fuel_loadings_file[0]):
                        self._fuel_loadings_file = os.path.abspath(args.fuel_loadings_file[0])
            else:
                print("\nError: an input file is required.\n")
                sys.exit(1)
            if args.col_cfg_file and self.exists(args.col_cfg_file[0]):
                self._col_cfg_file = args.col_cfg_file[0]

    def exists(self, filename):
        if not os.path.exists(filename):
            print("Error: file not found \"{}\"".format(filename))
            sys.exit(1)
        return True

    @property
    def csv_file(self): return self._csv_file
    @property
    def col_cfg_file(self): return self._col_cfg_file
    @property
    def fuel_loadings_file(self): return self._fuel_loadings_file


def main():
    ConsumeParser(sys.argv)

if __name__ == '__main__':
    main()
