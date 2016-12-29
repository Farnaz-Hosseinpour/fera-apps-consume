#-------------------------------------------------------------------------------
# Name:        test_driver.py
# Author:      kjells
# Created:     9/22/2011
# Copyright:   (c) kjells 2011
# Purpose:     Use to generate results and run regression tests.
#-------------------------------------------------------------------------------

import sys
import os
import random
import traceback

INPUT_FILES = [
    './test/regression_input_southern.csv',
    './test/regression_input_western.csv',
]

CONSUME_DRIVER = 'consume_batch.py'
TYPE_NATURAL = 'natural'
TYPE_ACTIVITY = 'activity'

def exception_wrapper(func, *args):
    print("Running {}".format(func.__name__))
    try:
        func(*args)
        return 0
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('\nException running {}'.format(func.__name__))
        traceback.print_tb(exc_traceback, limit=-10, file=sys.stdout)
        print('\t{}'.format(e))
        return 1

#-------------------------------------------------------------------------------
# Start
#-------------------------------------------------------------------------------
errors = 0
for ifile in INPUT_FILES:
    cmd = 'python3 {} {} {}'.format(CONSUME_DRIVER, TYPE_NATURAL, ifile)
    errors += os.system(cmd)
if errors:
    print('\nFailed !!!\n')
else:
    print('\nSuccess !!!\n')

exit(1 if errors else 0)

