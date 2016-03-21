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

'''
Capillary
=========

The Capillary class is for handling capillary used in electrophoresis.

Usage example
-------------

The following example permits to compute the volume of a capillary:

    import capillary

    my_capillary = capillary.Capillary()
    my_capillary.capillary_volume()

'''

import math

class Capillary:
    '''The Capillary class permits to compute capillary parameters
       during a Capillary Electrophoresis experiment.
    '''
    def __init__(self, total_length = 100.0, to_window_length = 90.0,
                 diameter = 30.0, pressure = 30.0, duration = 21.0,
                 viscosity = 1.0,
                 molweight = 150000.0, concentration = 21.0,
                 voltage = 30000.0, electric_current = 4.0,
                 detection_time = 3815.0, electro_osmosis_time = 100):
        '''Initialize the capillary
        '''
        # The length of the capillary (centimeter)
        self.total_length = total_length

        # The window length (centimeter)
        self.to_window_length = to_window_length

        # The capillary inside diameter (micrometer)
        self.diameter = diameter

        # The pressure drop across the capillary (mbar)
        self.pressure = pressure

        # The time the pressure is applied (second)
        self.duration = duration

        # The buffer viscosity (cp)
        self.viscosity = viscosity

        # Analyte concentration (g/L)
        self.concentration = concentration

        # Analyte molecular weight (g/mol)
        self.molweight = molweight

        # The voltage applied to the capillary (volt)
        self.voltage = voltage

        # The current applied to the capillary (microampere)
        self.electric_current = electric_current

        # The detection time (s)
        self.detection_time = detection_time

        # The electro-osmosis time (s)
        self.electro_osmosis_time = electro_osmosis_time

    def delivered_volume(self):
        '''Return the volume delivered during the injection
        '''
        delivered_volume = (self.pressure * self.diameter**4 * math.pi * self.duration) / (128 * self.viscosity * self.total_length * 10**5)
        return delivered_volume

    def capillary_volume(self):
        '''Return the volume of the capillary
        '''
        capillary_volume = (self.total_length * math.pi * (self.diameter / 2)**2) / 100
        return capillary_volume

    def to_window_volume(self):
        '''Return the volume to window
        '''
        to_window_volume = (self.to_window_length * math.pi * (self.diameter / 2)**2) / 100
        return to_window_volume

    def injection_plug_length(self):
        '''Return the plug_length used in the injection
        '''
        injection_plug_length = (self.pressure * self.diameter**2 * self.duration) / (32 * self.viscosity * self.total_length * 10**2)
        return injection_plug_length

    def time_to_replace_volume(self):
        '''Return the time required to replace the volume
        '''
        time_to_replace_volume = (32 * self.viscosity * self.total_length**2) / (self.diameter**2 * 10**-3 * self.pressure)
        return time_to_replace_volume

    def compute_viscosity(self):
        '''Return an assessment of the viscosity
        '''
        computed_viscosity = (self.pressure * self.diameter**2 *self.detection_time) / (32 * self.total_length * self.to_window_length * 10**3)
        return computed_viscosity

    def compute_conductivity(self):
        '''Return the conductivity
        '''
        computed_conductivity = (4 * self.total_length * 10**4 * self.electric_current) / (math.pi * self.diameter**2 * self.voltage)
        return computed_conductivity

    def field_strength(self):
        '''Return the field strength
        '''
        field_strength = self.voltage / self.total_length
        return field_strength

    def micro_eof(self):
        '''Return the Micro EOF
        '''
        micro_eof = (self.total_length * self.to_window_length) / (self.electro_osmosis_time * self.voltage)
        return micro_eof

    def length_per_minute(self):
        '''Return the length per minute
        '''
        length_per_minute = 60 * self.micro_eof() * self.field_strength() * 10**-2
        return length_per_minute

    def flow_rate_inj(self):
        '''Return the flow rate for the flow rate screen
        '''
        flow_rate = self.capillary_volume()/self.time_to_replace_volume()
        return flow_rate

    def flow_rate_flow(self):
        '''Return the flow rate per minute
        '''
        flow_rate = (math.pi * self.diameter**2 * self.length_per_minute()) / 4
        return flow_rate

    def injection_pressure(self):
        '''Return the injection pressure per second
        '''
        return self.pressure*self.duration

    def analyte_injected_ng(self):
        '''Return the analyte injected in ng
        '''
        return self.concentration * self.delivered_volume()

    def analyte_injected_pmol(self):
        '''Return the analyte injected in pmol
        '''
        return (self.analyte_injected_ng()/self.molweight)*1000

    def micro_app(self, time):
        '''Return the micro_app time in second'''
        return (self.total_length * self.to_window_length) / (time * self.voltage)

    def micro_ep(self, time):
        '''Return the micro_ep time in second'''
        return self.micro_app(time) - self.micro_eof()
