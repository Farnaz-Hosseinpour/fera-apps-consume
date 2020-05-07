# Consume

### Purpose/Description:
Consume calculates consumption and emission results based on a number of input parameters. The core Consume code was designed for interactive use in a REPL (read, evaluate, print, loop) environment. FERA has wrapped the core code to provide an application interface. Run the wrapper (consume_batch.py) with no arguments to see usage instructions.

```

$ python consume_batch.py 
usage: consume_batch.py [-h] [-f loadings file] [-x output columns]
                        [-l message level] [--metric] [--nosera] [-o output filename]
                        [burn type	(activity | natural)]
                        [input file	csv format]

    Consume predicts fuel consumption, pollutant emissions, and heat release
    based on input fuel loadings and environmental variables.  This command
    line interface requires a specified burn type (either activity or natural),
    environmental variables input file (csv format), and fuel loadings file
    (generated by FCCS 3.0, csv format), and.  A sample fuel loadings file
    (fuel_loadings.csv) and environmental inputs file (input.csv) have been
    provided. For more information on FCCS input files and results,
    please see: LINK.

positional arguments:
  burn type	(activity | natural)
  input file	(csv format)

optional arguments:
  -h, --help            show this help message and exit
  -f loadings file      Specify the fuel loadings file for consume to use. Run
                        the FCCS batch processor over the fuelbeds for which
                        you want to generate consumption/emission results to
                        create a fuel loadings file.
  -x output columns     Specify the output column configuration file for
                        consume to use
  -l message level      Specify the detail level of messages (1 | 2 | 3). 1 =
                        fewest messages 3 = most messages
  --metric              Indicate that columns should be converted to metric
                        units.
  --nosera              Normally, emissions factors are looked up in tables based
                        on the Smoke Emissions Reference Application (SERA) database: 
                        (https://depts.washington.edu/nwfire/sera/index.php) 
                        Use this option to lookup values in tables not based 
                        on the SERA database.
  -o output filename    Specify the name of the Consume output results file.

Examples:
    // display help (this text)
    python consume_batch.py

    // Simple case, natural fuel types, required input file (uses built-in loadings file)
    python consume_batch.py natural input_natural.csv

    // Specify an alternative loadings file
    python consume_batch.py natural input_natural.csv -f my_loadings.xml

    // Specify a column configuration file. Please see the documentation for details.
    python consume_batch.py activity input_activity.csv -x output_summary.csv

```

### Building
Consume is written in Python so there is no build. Consume runs under both Python 2 an 3

### Tests
Consume has regression tests and unit tests (depends on the green library). 
```
pip install green
```

Run them like so:

```
$ ./run_regression_tests.sh 
python3 consume_batch.py natural ./test/regression_input_southern.csv 


Success!!! Results are in "/home/kjells/fera/consume/consume_results.csv"
diff ./consume_results.csv ./test/expected/regression_expected_southern.csv 

python3 consume_batch.py natural ./test/regression_input_western.csv 


Success!!! Results are in "/home/kjells/fera/consume/consume_results.csv"
diff ./consume_results.csv ./test/expected/regression_expected_western.csv 


Success !!!

```

```
$ ./run_unit_tests.sh 
......................................

Ran 38 tests in 0.111s

OK (passes=38)

```


### Problems/Quirks
Consume runs under both Python 2 and 3, and we package a version of portable Python within FFT. At some point, there will be changes to Python that break the portable Python. At some point, it might be advisable to pull python from FFT and require Windows users to install Python locally.

Known dependencies on Consume:

* Bluesky uses the Consume_loadings.csv file (FCCS output)

* Consume module has been implemented in:

    - BlueSky

    - FFT

    - WFEIS (not maintained - Michigan Tech)

    - WA DNR Smoke Management System

    - ODF ACost System 


### Links
name (link)
