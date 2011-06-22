#This file was originally generated by PyScripter's unitest wizard

import unittest
import fccs_db
import nose
import re
import helper

class TestFCCSDB(unittest.TestCase):

    def setUp(self):
        infile = helper.get_test_inputfile()
        self.db = fccs_db.FCCSDB(fccs_file=infile)

    def tearDown(self):
        pass

    """
    def testget_canopy_pct(self):
        # get_canopy_pct() should likely be removed. Old xml files have this as data.
        pass

    def testbrowse(self):
        pass

    def testlist_fuel_loading_names(self):
        pass
    """

    def short_info(self):
        short_info = self.db.info(1, detail=False, ret=True)
        chunks = short_info.split('\n')
        nose.tools.ok_(5 == len(chunks), "Got = {}".format(len(chunks)))
        nose.tools.ok_('1' in chunks[1], "Got {}".format(chunks[1]))
        nose.tools.ok_('sitename' in chunks[2], "Got {}".format(chunks[2]))
        nose.tools.ok_('sitedescription' in chunks[4], "Got {}".format(chunks[4]))

    def long_info(self):
        expected = {
            'FCCS ID#':1,
            'Bailey\'s ecoregion division(s)':240,
            'SAM/SRM cover type(s)':129,
            'Overstory':19.44,
            'Midstory':8.72,
            'Understory':0.51,
            'Snags, class 1, foliage':0,
            'Snags, class 1, wood':0,
            'Snags, class 1, w/o foliage':1.3,
            'Snags, class 2':0.25,
            'Snags, class 3':1.17,
            'Ladder fuels':4.6,
            #'Shrub Primary':1.15, this is in the xml file. It is multiplied by 3 for some reason.
            'Shrub Primary':3.45,
            'Shrub Primary % live':95.0,
            'Shrub Secondary':0,
            'Shrub Secondary % live':0,
            'NW Primary':0.2,
            'NW Primary % live':90,
            'NW Secondary':0,
            'NW Secondary % live':0,
            'Litter depth':.5,
            'Litter % cover':85,
            'Short needle':30,
            'Long needle':0,
            'Other conifer':0,
            'Broadleaf deciduous':70.0,
            'Broadleaf evergreen':0,
            'Palm frond':0,
            'Grass':0,
            'Lichen depth':0.1,
            'Lichen % cover':5,
            'Moss depth':0.5,
            'Moss % cover':40.0,
            'Moss type':2,
            'Duff depth, upper':0.5,
            'Duff % cover, upper':100,
            'Duff derivation, upper':2,
            'Duff depth, lower':1.5,
            'Duff % cover, lower':100,
            'Duff derivation, lower':4,
            'Basal accumulations depth':0,
            'Basal accum. % cover':0,
            'Basal accumulations radius':0,
            'Squirrel midden depth':0,
            'Squirrel midden density':0,
            'Squirrel midden radius':0,
            '1-hr (0-0.25")':0.2,
            '10-hr (0.25-1")':0.8,
            '100-hr (1-3")':3.5,
            '1000-hr (3-9"), sound':0.4,
            '10,000-hr (9-20"), sound':0.5,
            '10,000-hr+ (>20"), sound':0,
            '1000-hr (3-9"), rotten':3.0,
            '10,000-hr (9-20"), rotten':4.0,
            '10,000-hr+ (>20"), rotten':5.0,
            'Stumps, sound':0,
            'Stumps, rotten':0.029,
            'Stumps, lightered':0
        }
        long_info = self.db.info(1, detail=True, ret=True)
        chunks = long_info.split('\n')
        for item in chunks:
            item = item.strip()
            if ':' in item:
                parts = item.split(':')
                key = parts[0].strip()
                match = re.search('[0-9\.]+', parts[1])
                if match:
                    if expected.has_key(key):
                        nose.tools.eq_(
                            float(expected[key]), float(match.group(0)),
                            "\"{}\" {} {}".format(key, float(expected[key]),
                            float(match.group(0))))
                    else:
                        nose.tools.ok_(False, "Missing key \"{}\"".format(key))

    def check_info(self):
        check_good = self.db.info(1, detail=False, ret=True)
        nose.tools.ok_('not found' not in check_good)
        check_bad = self.db.info(14, detail=False, ret=True)
        nose.tools.ok_('not found' in check_bad)

    def testinfo(self):
        self.check_info()
        self.short_info()
        self.long_info()

if __name__ == '__main__':
    unittest.main()
