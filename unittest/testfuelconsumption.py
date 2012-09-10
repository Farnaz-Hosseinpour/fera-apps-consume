#This file was originally generated by PyScripter's unitest wizard

import unittest
import consume
import helper

class TestFuelConsumption(unittest.TestCase):

    def setUp(self):
        infile = helper.get_test_inputfile()
        self._consumer = consume.FuelConsumption()
        '''
        self._consumer.burn_type = 'natural'
        self._consumer.fuelbed_area_acres = [100]
        self._consumer.fuel_moisture_1000hr_pct = [20]
        self._consumer.fuel_moisture_duff_pct = [20]
        self._consumer.canopy_consumption_pct = [20]
        self._consumer.shrub_blackened_pct = [50]
        self._consumer.output_units = 'tons_ac'
        self._consumer.fuelbed_fccs_ids = [i for i in self._consumer.FCCS.loadings_data_]
        '''

    def tearDown(self):
        pass

    """
    def testreset_inputs_and_outputs(self):
        pass

    def testload_example(self):
        pass

    def testprompt_for_inputs(self):
        pass

    def testresults(self):
        pass

    def testreport(self):
        pass

    def testbatch_process(self):
        pass

    def testdisplay_inputs(self):
        pass

    def testlist_variable_names(self):
        pass

    def testsave_scenario(self):
        pass

    def testload_scenario(self):
        pass

    def test_display_report(self):
        pass
    """

    def test_wfeis_return(self):
        ''' We don't use this method, but presumably MTI does.
            Make sure it is callable
        out = self._consumer._wfeis_return()
        for key in out.keys():
            for i in ['smoldering', 'total', 'flaming', 'residual']:
                self.assertTrue(out[key][i] == 0.0, msg="Not zero {}:{}".format(key, i))
        '''

    """
    def test_build_input_set(self):
        pass

    def test_calculate(self):
        pass

    def test_convert_units(self):
        pass

    def test_heat_release_calc(self):
        pass

    def test_consumption_calc(self):
        pass
    """

if __name__ == '__main__':
    unittest.main()
