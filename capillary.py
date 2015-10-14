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

"""
Capillary
=========

The Capillary class is for handling capillary used in electrophoresis.

Usage example
-------------

The following example permits to compute the volume of a capillary:

    import capillary

    my_capillary = capillary.Capillary()
    my_capillary.diameter = 60.0
    my_capillary.total_length = 80.0
    my_capillary.capillary_volume()

"""

import math

from store import get_store
from convertunits import (LengthUnits, PressureUnits, TimeUnits, 
						  ConcentrationUnits, MolConcentrationUnits,
						  MolWeightUnits, VoltUnits)

class Capillary:
    '''Capillary class, see module documentation for more information.
    '''
    def __init__(self):
        store = get_store()
        # The length of the capillary (centimeter)
        self.total_length = LengthUnits.convert_unit(float(store.get('Capillary')["value"]), 
                                                     store.get('Capillary')["unit"], 
                                                     u"cm")
        # The window length (centimeter)
        self.to_window_length = LengthUnits.convert_unit(float(store.get('Towindow')["value"]),
                                                         store.get('Towindow')["unit"], 
                                                         u"cm")
        # The capillary inside diameter (micrometer)
        #PROBLEM WITH UNICODE NON ASCII 
        self.diameter = LengthUnits.convert_unit(float(store.get('Idiameter')["value"]),
                                                 store.get('Idiameter')["unit"], 
                                                 u"µm")
        # The pressure drop across the capillary (mbar)
        self.pressure = PressureUnits.convert_unit(float(store.get('Pressure')["value"]),
                                                   store.get('Pressure')["unit"], 
                                                   u"mbar")
        # The time the pressure is applied (second)
        self.duration = TimeUnits.convert_unit(float(store.get('Time')["value"]),
                                               store.get('Time')["unit"], 
                                               u"s")
        # The buffer viscosity (cp)
        self.viscosity = float(store.get('Viscosity')["value"])
        # Analyte concentration (mol/l)
        if store.get('Concentration')["unit"] == u"mmol/L":
            self.concentration = MolConcentrationUnits.convert_unit(float(store.get('Concentration')["value"]),
                                                                    store.get('Concentration')["unit"], 
                                                                    u"mol/L")
        else:
            self.concentration = float(store.get('Concentration')["value"]) / \
                                       float(store.get('Molweight')["value"])
        # The voltage applied to the capillary (volt)
        self.voltage = VoltUnits.convert_unit(float(store.get('Voltage')["value"]),
                                              store.get('Voltage')["unit"], 
                                              u"V")
        # The current applied to the capillary (microampere)
        self.electric_current = float(store.get('Electriccurrent')["value"])
        # The detection time (s)
        self.detection_time = TimeUnits.convert_unit(float(store.get('Detectiontime')["value"]),
                                                     store.get('Detectiontime')["unit"], 
                                                     u"s")
        # The electro-osmosis time (s)
        self.electro_osmosis_time = TimeUnits.convert_unit(float(store.get('Electroosmosis')["value"]),
                                                           store.get('Electroosmosis')["unit"], 
                                                           u"s")

    def delivered_volume(self):
        """Return the volume delivered during the injection
        """
        delivered_volume = (self.pressure * self.diameter**4 * math.pi * self.duration) / (128 * self.viscosity * self.total_length * 10**5)
        return delivered_volume

    def capillary_volume(self):
        """Return the volume of the capillary
        """
        capillary_volume = (self.total_length * math.pi * (self.diameter / 2)**2) / 100
        return capillary_volume

    def to_window_volume(self):
        """Return the volume to window
        """
        to_window_volume = (self.to_window_length * math.pi * (self.diameter / 2)**2) / 100
        return to_window_volume

    def injection_plug_length(self):
        """Return the plug_length used in the injection
        """
        injection_plug_length = (self.pressure * self.diameter**2 * self.duration) / (32 * self.viscosity * self.total_length * 10**2)
        return injection_plug_length

    def time_to_replace_volume(self):
        """Return the time required to replace the volume
        """
        time_to_replace_volume = (32 * self.viscosity * self.total_length**2) / (self.diameter**2 * 10**-3 * self.pressure)
        return time_to_replace_volume
    
    def compute_viscosity(self):
        """Return an assessment of the viscosity
        """
        computed_viscosity = (self.pressure * self.diameter**2 *self.detection_time) / (32 * self.total_length * self.to_window_length * 10**3)
        return computed_viscosity

    def compute_conductivity(self):
        """Return the conductivity
        """
        computed_conductivity = (4 * self.total_length * 10**4 * self.electric_current) / (math.pi * self.diameter**2 * self.voltage)
        return computed_conductivity

    def field_strength(self):
        """Return the field strength
        """
        field_strength = self.voltage / self.total_length
        return field_strength

    def micro_eof(self):
        """Return the Micro EOF
        """
        micro_eof = (self.total_length * self.to_window_length) / (self.electro_osmosis_time * self.voltage)
        return micro_eof

    def length_per_minute(self):
        """Return the length per minute
        """
        length_per_minute = 60 * self.micro_eof() * self.field_strength() * 10**-2
        return length_per_minute 

    def flow_rate(self):
        """Return the flow rate
        """
        flow_rate = (math.pi * self.diameter**2 * self.length_per_minute()) / 4
        return flow_rate

    def save_vicosity_result(self):
        """ compute and save the results for the vicosity screen """
        store = get_store()
        viscosity = self.compute_viscosity()
        store.put('Viscosity', value=viscosity, unit="cp")
		
    def save_conductivy_result(self):
        """ compute and save the result for the conductivy screen """  
        store = get_store()
        conductivity = self.compute_conductivity()
        store.put('Conductivity', value=conductivity, unit="S/m")
		
