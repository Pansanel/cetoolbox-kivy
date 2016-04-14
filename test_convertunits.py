# -*. coding: utf-8 -*-
# Copyright (c) 2015 CNRS and University of Strasbourg
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

import unittest

from convertunits import LengthUnits 
from convertunits import PressureUnits 
from convertunits import TimeUnits 
from convertunits import ConcentrationUnits 
from convertunits import MolConcentrationUnits 
from convertunits import MolWeightUnits 
from convertunits import VoltUnits 

class TestLengthUnits(unittest.TestCase):

    def test_convert_meter_to_meter(self):
        value = LengthUnits.convert_unit(10, 'm', 'm')
        self.assertEqual(value, 10)

    def test_convert_centimeter_to_meter(self):
        value = LengthUnits.convert_unit(10, 'cm', 'm')
        self.assertEqual(value, 0.1)

    def test_convert_millimeter_to_centimeter(self):
        value = LengthUnits.convert_unit(10, 'mm', 'cm')
        self.assertEqual(value, 1)

class TestPressureUnits(unittest.TestCase):

    def test_convert_pascal_to_pascal(self):
        value = PressureUnits.convert_unit(10, 'pa', 'pa')
        self.assertEqual(value, 10)

    def test_convert_bar_to_pascal(self):
        value = PressureUnits.convert_unit(0.1, 'bar', 'pa')
        self.assertEqual(value, 10000)

    def test_convert_mbar_to_bar(self):
        value = PressureUnits.convert_unit(10, 'mbar', 'bar')
        self.assertEqual(value, 0.01)

    def test_convert_bar_to_psi(self):
        value = PressureUnits.convert_unit(0.1, 'bar', 'psi')
        self.assertAlmostEqual(value, 1.45036839357, places=11)

class TestTimeUnits(unittest.TestCase):

    def test_convert_second_to_second(self):
        value = TimeUnits.convert_unit(10, 's', 's')
        self.assertEqual(value, 10)

    def test_convert_minute_to_second(self):
        value = TimeUnits.convert_unit(1.5, 'min', 's')
        self.assertEqual(value, 90)

    def test_convert_hour_to_minute(self):
        value = TimeUnits.convert_unit(2, 'h', 'min')
        self.assertEqual(value, 120)

class TestConcentrationUnits(unittest.TestCase):

    def test_convert_gperl_to_gperl(self):
        value = ConcentrationUnits.convert_unit(10, 'g/L', 'g/L')
        self.assertEqual(value, 10)

    def test_convert_mgperl_to_gperl(self):
        value = ConcentrationUnits.convert_unit(10, 'mg/L', 'g/L')
        self.assertEqual(value, 0.01)

class TestMolConcentrationUnits(unittest.TestCase):

    def test_convert_molperl_to_molperl(self):
        value = MolConcentrationUnits.convert_unit(10, 'mol/L', 'mol/L')
        self.assertEqual(value, 10)

    def test_convert_mmolperl_to_molperl(self):
        value = MolConcentrationUnits.convert_unit(10, 'mmol/L', 'mol/L')
        self.assertEqual(value, 0.01)

class TestMolWeightUnits(unittest.TestCase):

    def test_convert_gpermol_to_gpermol(self):
        value = MolWeightUnits.convert_unit(10, 'g/mol', 'g/mol')
        self.assertEqual(value, 10)

    def test_convert_mgpermol_to_gpermol(self):
        value = MolWeightUnits.convert_unit(10, 'mg/mol', 'g/mol')
        self.assertEqual(value, 0.01)

class TestVoltUnits(unittest.TestCase):

    def test_convert_volt_to_volt(self):
        value = VoltUnits.convert_unit(10, 'V', 'V')
        self.assertEqual(value, 10)

    def test_convert_mvolt_to_volt(self):
        value = VoltUnits.convert_unit(10, 'mV', 'V')
        self.assertEqual(value, 0.01)

    def test_convert_mvolt_to_kvolt(self):
        value = VoltUnits.convert_unit(100, 'mV', 'KV')
        self.assertEqual(value, 0.0001)

if __name__ == '__main__':
    unittest.main()
