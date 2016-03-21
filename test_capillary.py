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

from capillary import Capillary

class TestCapillary(unittest.TestCase):

    def setUp(self):
        self.capillary = Capillary()
        self.capillary.total_length = 100.0
        self.capillary.to_window_length = 90.0
        self.capillary.diameter = 30.0
        self.capillary.pressure = 30.0
        self.capillary.duration = 21.0
        self.capillary.viscosity = 1.0
        self.capillary.molweight = 150000
        self.capillary.concentration = 21.0
        self.capillary.electric_current = 4.0
        self.capillary.voltage = 30000.0
        self.capillary.detection_time = 3600.0
        self.capillary.electro_osmosis_time = 330.0

    def test_delivered_volume(self):
        value = self.capillary.delivered_volume()
        self.assertAlmostEqual(value, 1.25, places=2)

    def test_capillary_volume(self):
        value = self.capillary.capillary_volume()
        self.assertAlmostEqual(value, 706.86, places=2)

    def test_to_window_volume(self):
        value = self.capillary.to_window_volume()
        self.assertAlmostEqual(value, 636.17, places=2)

    def test_injection_plug_length(self):
        value = self.capillary.injection_plug_length()
        self.assertAlmostEqual(value, 1.77, places=2)

    def test_time_to_replace_volume(self):
        value = self.capillary.time_to_replace_volume()
        self.assertAlmostEqual(value, 11851.85,	places=2)

    def test_compute_viscosity(self):
        value = self.capillary.compute_viscosity()
        self.assertAlmostEqual(value, 0.34, places=2)

    def test_compute_conductivity(self):
        value = self.capillary.compute_conductivity()
        self.assertAlmostEqual(value, 0.188, places=2)

    def test_field_strength(self):
        value = self.capillary.field_strength()
        self.assertAlmostEqual(value, 300)

    def test_micro_eof(self):
        value = self.capillary.micro_eof()
        self.assertAlmostEqual(value, 0.000909, places=6)

    def test_length_per_minute(self):
        value = self.capillary.length_per_minute()
        self.assertAlmostEqual(value, 0.1636, places=4)

    def test_flow_rate_inj(self):
        value = self.capillary.flow_rate_inj()
        self.assertAlmostEqual(value, 0.0596, places=4)

    def test_flow_rate_flow(self):
        value = self.capillary.flow_rate_flow()
        self.assertAlmostEqual(value, 115.67, places=2)

    def test_injection_pressure(self):
        value = self.capillary.injection_pressure()
        self.assertAlmostEqual(value, 630.0, places=1)

    def test_analyte_injected_ng(self):
        value = self.capillary.analyte_injected_ng()
        self.assertAlmostEqual(value, 26.3, places=1)

    def test_analyte_injected_pmol(self):
        value = self.capillary.analyte_injected_pmol()
        self.assertAlmostEqual(value, 0.18, places=2)

    def test_micro_app(self):
        value = self.capillary.micro_app(330)
        self.assertAlmostEqual(value, 0.00091, places=5)

    def test_micro_ep(self):
        value = self.capillary.micro_ep(60)
        self.assertAlmostEqual(value, 0.00409, places=5)

if __name__ == '__main__':
    unittest.main()
