#This file was originally generated by PyScripter's unitest wizard

import unittest
import consume
import nose

class TestFuelConsumption(unittest.TestCase):

    def setUp(self):
        self._consumer = consume.FuelConsumption(
            fccs_file = "unittest/test.xml")
            #fccs_file = "input_data/fccs_pyconsume_input.xml")
        self.reset_consumer()

    def reset_consumer(self):
        self._consumer.burn_type = 'natural'
        self._consumer.fuelbed_area_acres = 100
        self._consumer.fuel_moisture_1000hr_pct = 20
        self._consumer.fuel_moisture_duff_pct = 20
        self._consumer.fuel_moisture_10hr_pct = 10
        self._consumer.canopy_consumption_pct = 20
        self._consumer.shrub_blackened_pct = 50
        self._consumer.output_units = 'tons_ac'
        self._consumer.slope = 5
        self._consumer.lengthOfIgnition = 30
        self._consumer.days_since_rain = 20
        self._consumer.windspeed = 5
        self._consumer.fm_type = 'MEAS-Th'

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

    def test_wfeis_return(self):
        pass

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

    def test_calc_intensity_reduction_factor(self):
        import numpy as np
        f = self._consumer.calc_intensity_reduction_factor_nparray
        area = np.array([10, 20, 25, 30])
        lengthOfIgnition = np.array([5, 20, 40, 60])
        fm_10hr = np.array([10, 14, 17, 25])
        fm_1000hr = np.array([35, 40, 49, 55])
        irf = f(area, lengthOfIgnition, fm_10hr, fm_1000hr)
        expected = [0.33, 0.22, 0.11, 1.0]
        for i, item, in enumerate(expected):
            nose.tools.eq_(irf[i], item, "Expected {}, got {}".format(item, irf[i]))

    def test_calc_intensity_reduction_factor_alt(self):
        f = self._consumer.calc_intensity_reduction_factor
        tests = [
            [0.78, 9, 5, 15, 39],   # - fm extreme but area too small
            [0.667, 10, 5, 15, 39],  # - fm extreme, area just adequate
            [0.89, 10, 5, 16, 39],  # - fm10 just out of extreme and makes it move 2 buckets
            [0.78, 10, 5, 15, 41],  # - fm1000 just out of extreme
            [0.78, 10, 19, 15, 41],  # - fm1000 just out of extreme
            [0.89, 10, 21, 15, 41],  # - fm1000 just out of extreme, area just over
            [0.78, 10, 11, 15, 39],  # - fm extreme, area ok, duration to high
            [0.667, 10, 9, 15, 39],  # - fm extreme, area ok, duration just below
            [0.667, 19, 18, 15, 39],  # - area just under 20
            [0.667, 21, 20, 15, 39],  # - area just over 20 duration just under
            [0.78, 21, 21, 15, 39],  # - area just over 20 duration equal
            [0.89, 19, 75, 18, 50],  # - area just over 20 duration equal
            [1.0, 19, 75, 18, 51],  # - area just over 20 duration equal
            [1.0, 19, 76, 19, 50],  # - area just over 20 duration equal
            [1.0, 19, 77, 18, 50],  # - area just over 20 duration equal
        ]
        for i, test in enumerate(tests):
            #print i
            self.assertAlmostEqual(test[0], f(test[1], test[2], test[3], test[4]), 2)

if __name__ == '__main__':
    unittest.main()
