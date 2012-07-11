#-------------------------------------------------------------------------------
# Name:        test_driver.py
# Author:      kjells
# Created:     9/22/2011
# Copyright:   (c) kjells 2011
# Purpose:     Use to generate results and run regression tests.
#-------------------------------------------------------------------------------

# - run via batch file that sets PYTHONPATH correctly
import sys
import os
def pp():
    curdir = os.path.abspath(os.path.curdir)
    pardir = os.path.abspath(os.path.pardir)
    if pardir not in sys.path:
        sys.path.append(pardir)
    if curdir not in sys.path:
        sys.path.append(curdir)
    print(sys.path)

pp()
import consume
from tester import DataObj as compareCSV

def get_this_location():
    ''' Return the absolute directory path for this file
    '''
    return os.path.dirname(os.path.abspath(__file__))

def out_name(dir, filename):
    ''' Return the absolute directory path of this file
         with the supplied directory name and filename appended
    '''
    return os.path.join(
        os.path.join(get_this_location(), dir),
        filename)

def get_input_file():
    ''' Judge the location of the input file based on its relation to this file
    '''
    DATA_INPUT_FILE = "consume/input_data/fccs_loadings_1_458.xml"
    here = get_this_location()
    here = here[:-len('test')]
    return os.path.normpath(os.path.join(here, DATA_INPUT_FILE))

def wrap_input_display(inputs):
    ''' Print all the inputs with the exception of the fuelbed array
    '''
    if inputs:
        chunks = inputs.split('\n')
        print('')
        for line in chunks:
            if line and not line.startswith('FCCS'):
                print(line)
    else:
        print("\nError: missing input display")

def get_fuelbed_list(consumer):
    ''' The expected values against which we test go to the max below '''
    MAX_REFERENCE_FUELBED = 291
    return [i[0] for i in consumer.FCCS.data if MAX_REFERENCE_FUELBED >= i[0]]

def get_consumption_object(burn_type):
    ''' Return a "ready to go" consumption object
    '''
    consumer = consume.FuelConsumption(fccs_file = get_input_file())
    set_defaults(consumer, {'burn_type' : burn_type})
    # run over the reference fuelbeds
    fuelbed_list = get_fuelbed_list(consumer)
    consumer.fuelbed_fccs_ids = fuelbed_list
    return consumer

def write_columns(results, catagories, stream, first_element, index, header=False):
    out = str(first_element)
    for cat in catagories:
        sorted_keys = sorted(results[cat].keys())
        for key in sorted_keys:
            out += ","
            if not header:
                if cat != 'heat release':
                    out += str(results[cat][key]['total'][index])
                else:
                    out += str(results[cat][key][index])
            else:
                # 'primary live', 'seconday live' occur in multiple catagories,
                #   ensure unique column headings
                if ('primary' in key or 'secondary' in key) or (cat == 'heat release'):
                    key = cat + " " + key
                out += key
    out += '\n'
    stream.write(out)

def write_header(results, catagory_list, stream):
    write_columns(results, catagory_list, stream, 'fuelbed', None, True)

def write_header_emissions(catagory_list, stream):
    out = "fuelbed"
    for i in catagory_list:
        out += "," + i
    out += '\n'
    stream.write(out)

def write_csv(results, fuelbed_list, stream):
	# - top-level catagory list
    catagory_list = ['summary', 'canopy', 'ground fuels',
        'litter-lichen-moss', 'nonwoody', 'shrub', 'woody fuels', 'heat release']
    cresults = results['consumption']
    cresults['heat release'] = results['heat release']
    write_header(cresults, catagory_list, stream)
    for fb_index in xrange(0, len(fuelbed_list)):
        write_columns(cresults, catagory_list, stream, fuelbed_list[fb_index], fb_index)

def write_csv_emissions(results, fuelbed_list, stream):
    # use all the emission keys except 'stratum'
    emissions_keys = sorted(results['emissions'].keys())
    emissions_keys = [key for key in emissions_keys if key != 'stratum']
    cons_keys = sorted(results['consumption']['summary']['total'].keys())
    hr_keys = sorted(results['heat release'].keys())

    # build up the column headers
    columns = []
    for key in cons_keys:
        columns.append("{}_{}".format("cons", key))
    for i in emissions_keys:
        for j in cons_keys:
            columns.append("{}_{}".format(i, j))
    for key in hr_keys:
        columns.append("heat release {}".format(key))

    write_header_emissions(columns, stream)
    for fb_index in xrange(0, len(fuelbed_list)):
        out = str(fuelbed_list[fb_index])

        # print the consumption column values
        for key in cons_keys:
            out += "," + str(results['consumption']['summary']['total'][key][fb_index])
        # print the emission column values
        for i in emissions_keys:
            for j in cons_keys:
                out += "," + str(results['emissions'][i][j][fb_index])
        # print the heat release column values
        for key in hr_keys:
            out += "," + str(results['heat release'][key][fb_index])

        out += '\n'
        stream.write(out)

def run_tests(consumer, fuelbed_list, outfile):
    ''' Run consumption-based tests
    '''
    results = consumer.results()
    write_csv(results, fuelbed_list, outfile)

def set_defaults(consumer, map):
    ''' If a map is supplied, use the values from it (doesn't have to contain all values)
         Otherwise, use the defaults
    '''
    consumer.burn_type = map['burn_type'] if 'burn_type' in map else 'natural'
    consumer.fuelbed_area_acres = map['fuelbed_area_acres'] if 'fuelbed_area_acres' in map else 100
    consumer.fuel_moisture_1000hr_pct = map['fuel_moisture_1000hr_pct'] if 'fuel_moisture_1000hr_pct' in map else 20
    consumer.fuel_moisture_duff_pct = map['fuel_moisture_duff_pct'] if 'fuel_moisture_duff_pct' in map else 20
    consumer.canopy_consumption_pct = map['canopy_consumption_pct'] if 'canopy_consumption_pct' in map else 20
    consumer.shrub_blackened_pct = map['shrub_blackened_pct'] if 'shrub_blackened_pct' in map else 50
    consumer.output_units = map['output_units'] if 'output_units' in map else 'tons_ac'
    consumer.fuelbed_ecoregion = map['fuelbed_ecoregion'] if 'fuelbed_ecoregion' in map else ['western']
    if 'activity' == consumer.burn_type:
        set_activity_defaults(consumer, map)

def set_activity_defaults(consumer, map):
    consumer.days_since_rain = map['days_since_rain'] if 'days_since_rain' in map else 20
    consumer.fuel_moisture_10hr_pct = map['fuel_moisture_10hr_pct'] if 'fuel_moisture_10hr_pct' in map else 10
    consumer.fm_type = map['fm_type'] if 'fm_type' in map else 'MEAS-Th'
    consumer.length_of_ignition = map['length_of_ignition'] if 'length_of_ignition' in map else 30
    consumer.slope = map['slope'] if 'slope' in map else 5
    consumer.windspeed = map['windspeed'] if 'windspeed' in map else 5

def run_basic_scenarios(consumer, fuelbed_list):
    ''' Run basic consumption scenarios
    '''
    scenario_list = [['western'], ['southern'], ['boreal'], ['activity']]
    for scene in scenario_list:
        consumer.fuelbed_ecoregion = list(scene) if 'activity' not in scene else ['western']
        if 'activity' in scene:
            consumer.burn_type = scene[0]
            set_activity_defaults(consumer, {})
        else:
            consumer.burn_type = 'natural'
        outfilename = out_name("results", "{}_out.csv".format(scene[0]))
        reference_values = out_name("expected", "{}_expected.csv".format(scene[0]))
        run_and_test(consumer, fuelbed_list, outfilename, reference_values)

def run_additional_activity_scenarios(consumer, fuelbed_list):
    activityTwo = {
        'burn_type': 'activity',
        'fuel_moisture_10hr_pct':15,
        'fuel_moisture_1000hr_pct':39,
        'fuelbed_area_acres':10,
        'length_of_ignition':5 }
    activityThree = {
        'burn_type': 'activity',
        'fuel_moisture_10hr_pct':15,
        'fuel_moisture_1000hr_pct':45,
        'fuelbed_area_acres':25 }
    activityFour = {
        'burn_type': 'activity',
        'fuel_moisture_10hr_pct':17,
        'fuel_moisture_1000hr_pct':50,
        'fuelbed_area_acres':100 }
    activityFive = {
        'burn_type': 'activity',
        'fuel_moisture_10hr_pct':25,
        'fuel_moisture_1000hr_pct':55,
        'fuelbed_area_acres':100 }

    scenario_list = [activityTwo, activityThree, activityFour, activityFive]
    counter = 2
    for scene in scenario_list:
        set_defaults(consumer, scene)
        consumer.fuelbed_ecoregion = ['western']
        outfilename = out_name("results", "{}_out.csv".format(counter))
        reference_values = out_name("expected", "scen{}_activity_expected.csv".format(counter))
        counter += 1
        run_and_test(consumer, fuelbed_list, outfilename, reference_values)

#-------------------------------------------------------------------------------
# Use a new emissions object because switching units causes an internal state
#  problem for subsequent runs. todo ks
#-------------------------------------------------------------------------------
def run_emissions_western(fuelbed_list):
    consumer = get_consumption_object('natural')
    em = consume.Emissions(consumer)
    outfilename ='western_emissions.csv'
    reference_file = "{}_expected.csv".format(outfilename.split('.')[0])
    run_and_test_emissions(em, fuelbed_list, outfilename, reference_file)

def run_emissions_activity(fuelbed_list):
    consumer = get_consumption_object('activity')
    em = consume.Emissions(consumer)
    outfilename ='activity_emissions.csv'
    reference_file = "{}_expected.csv".format(outfilename.split('.')[0])
    run_and_test_emissions(em, fuelbed_list, outfilename, reference_file)

def run_emissions_activity_with_unit_conversion(fuelbed_list):
    consumer = get_consumption_object('activity')
    consumer.fuelbed_ecoregion = ['western']
    em = consume.Emissions(consumer)
    em.output_units = 'kg_ha'
    outfilename ='activity_emissions_kgha.csv'
    reference_file = "{}_expected.csv".format(outfilename.split('.')[0])
    run_and_test_emissions(em, fuelbed_list, outfilename, reference_file)

#-------------------------------------------------------------------------------
# Currently need consumption-specific and emissions-specific runners
#-------------------------------------------------------------------------------
VERBOSE = True
def run_and_test(consumer, fuelbed_list, outfilename, reference_values):
    wrap_input_display(consumer.display_inputs(print_to_console=False))
    with open(outfilename, 'w') as outfile:
        run_tests(consumer, fuelbed_list, outfile)
    ref = compareCSV(reference_values, console=VERBOSE)
    computed = compareCSV(outfilename, console=VERBOSE)
    (failed, compared) = ref.Compare(computed)
    print("{} = failed, {} compared:\t{}".format(failed, compared, outfilename))

def run_and_test_emissions(emissions, fuelbed_list, outfilename, reference_values):
    wrap_input_display(emissions._cons_object.display_inputs(print_to_console=False))
    oname = out_name("results", outfilename)
    with open(oname, 'w') as outfile:
        results = emissions.results()
        write_csv_emissions(results, fuelbed_list, outfile)
    rname = out_name("expected", reference_values)
    ref = compareCSV(rname, console=VERBOSE)
    computed = compareCSV(oname, console=VERBOSE)
    (failed, compared) = ref.Compare(computed)
    print("{} = failed, {} compared:\t{}".format(failed, compared, outfilename))

def exception_wrapper(func, *args):
    try:
        print("Running {}".format(func.__name__))
        func(*args)
    except Exception as e:
        print('\nException running {}'.format(func.__name__))
        print(e)
        
#-------------------------------------------------------------------------------
# Start
#-------------------------------------------------------------------------------
# The emissions database doesn't have data for the 1000, 1001 fuelbeds
#  and we don't have a database/input generator to create the file as yet. When
#  that occurs, we can use the larger file
NORMAL = True
#NORMAL = False
consumer = consume.FuelConsumption(fccs_file = get_input_file())
set_defaults(consumer, {})

if NORMAL:
    # run over all the fuelbeds in the input file
    fuelbed_list = get_fuelbed_list(consumer)
    consumer.fuelbed_fccs_ids = fuelbed_list

    exception_wrapper(run_basic_scenarios, consumer, fuelbed_list)
    exception_wrapper(run_additional_activity_scenarios, consumer, fuelbed_list)

    set_defaults(consumer, {})
    exception_wrapper(run_emissions_activity_with_unit_conversion, fuelbed_list)
    exception_wrapper(run_emissions_western, fuelbed_list)
    exception_wrapper(run_emissions_activity, fuelbed_list)
else:
    # - debugging
    fuelbed_list = [5]
    #fuelbed_list = get_fuelbed_list(consumer)
    consumer.fuelbed_fccs_ids = fuelbed_list
    run_basic_scenarios(consumer, fuelbed_list)

