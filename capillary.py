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
        """ Get all needed values from the store"""
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
        #molecular weight (g/mol)
        self.molweight = float(store.get("Molweight")["value"])
        
        # Analyte concentration (g/L)
        
        if store.get('Concentration')["unit"] == u"mmol/L":
            tmpconcetration = MolConcentrationUnits.convert_unit(float(store.get('Concentration')["value"]),
                                                                 store.get('Concentration')["unit"], 
                                                                 u"mol/L")
            self.concentration = self.molweight * tmpconcetration
        else:
            self.concentration = float(store.get('Concentration')["value"])
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

    def flow_rate_inj(self):
        """Return the flow rate for the flow rate screen
        """
        onevol = self.time_to_replace_volume()
        flow_rate = self.capillary_volume()/TimeUnits.convert_unit(onevol, u's', u'min')
        return flow_rate
        
    def flow_rate_flow(self):
        """Return the flow rate for the flow screen """
        flow_rate = (math.pi * self.diameter**2 * self.length_per_minute()) / 4
        return flow_rate

    def injection_pressure(self):
        """ return the injection pressure /s : psi/s """
        psi = PressureUnits.convert_unit(self.pressure, u"mbar", u"psi")
        injection_pressure = psi/self.duration
        return injection_pressure

    def analyte_injected_ng(self):
        """ return the analyte injected in ng """
        return self.concentration * self.delivered_volume()
    
    def analyte_injected_pmol(self):
        """ return the analyte injected in pmol """
        return (self.analyte_injected_ng()/self.molweight)*1000
    
    def micro_app(self, time):
        """return the micro_app
        time in second"""
        return (self.total_length * self.to_window_length) / (time * self.voltage) 
    
    def micro_ep(self, time):
        """return the micro_ep
        time in second"""
        return self.micro_app(time) - self.micro_eof()
    
    def save_vicosity_result(self):
        """ compute and save the results for the vicosity screen """
        store = get_store()
        try:
            viscosity = self.compute_viscosity()
        except ZeroDivisionError: 
            if self.total_length == 0:
                return 1, "The capillary length cannot be null"
            else:
                return 1, "The window length cannot be null"
        
        if self.to_window_length > self.total_length:
            return 1, "The length to window cannot be greater than the capillary length"
        
        store.put('Viscosity', value=viscosity, unit="cp")
        return 0, ""
        
    def save_conductivy_result(self):
        """ compute and save the result for the conductivy screen """  
        store = get_store()
        
        try:
            conductivity = self.compute_conductivity()
        except ZeroDivisionError:
            if self.voltage == 0:
                return 1, "The voltage cannot be null"
            else:
                return 1, "The diameter cannot be null"
        
        if self.to_window_length > self.total_length:
            return 1, "The length to window cannot be greater than the capillary length"
        
        store.put('Conductivity', value=conductivity, unit="S/m")
        return 0, ""
    
    def save_flow_result(self):
        """ compute and save the result for the flow screen """
        store = get_store()
        
        try:
            strengh = self.field_strength()
            microeof = self.micro_eof()
            lpermin = self.length_per_minute()
            flowrate = self.flow_rate_flow()
        except ZeroDivisionError:
            if self.total_length == 0:
                return 1, "The capillary length cannot be null"
            elif self.electro_osmosis_time:
                return 1, "The EOF Time cannot be null" 
            else:
                return 1, "The voltage cannot be null"
            
        if self.to_window_length > self.total_length:
            return 1, "The length to window cannot be greater than the capillary length"
        
        store.put("Fieldstrength", value=strengh, unit="V/cm")
        store.put("MicroEOF", value=microeof, unit="cm²/V/s")
        store.put("Lengthpermin", value=LengthUnits.convert_unit(lpermin, u'm', u'cm'), unit="cm")
        store.put("Flowrate", value=flowrate, unit="nL/min")
        return 0, ""
        
    def save_injection_result(self):
        """ compute and save the result for the injection screen """
        store = get_store()
        
        try:
            hydroinj = self.delivered_volume()
            capilaryvol = self.capillary_volume()
            capilaryvoltowin = self.to_window_volume()
            pluglen = self.injection_plug_length()
            plugpertotallen = ((pluglen/10)/self.total_length)*100
            plugpertowinlen = ((pluglen/10)/self.to_window_length)*100
            timetoonevols = self.time_to_replace_volume()
            timetoonevolm = TimeUnits.convert_unit(timetoonevols, u's', u'min')
            analyteinjng = self.analyte_injected_ng()
            analyteinjpmol = self.analyte_injected_pmol()
            injpressure = self.injection_pressure()
            strengh = self.field_strength()
            flowrate = self.flow_rate_inj()
        except ZeroDivisionError:
            if self.viscosity == 0:
                return 1, "The viscosity cannot be null" 
            elif self.total_length == 0:
                return 1, "The capillary length cannot be null"
            elif self.to_window_length == 0:
                return 1, "The length to window cannot be null"
            elif self.diameter == 0:
                return 1, "The diameter cannot be null"
            elif self.pressure == 0:
                return 1, "The pressure cannot be null"
            elif self.duration == 0:
                return 1, "The time cannot be null"
            else :
                return 1, "The molecular weight cannot be null"
        
        
        if self.to_window_length > self.total_length:
            return 1, "The length to window cannot be greater than the capillary length"
        
        #special warning
        if plugpertowinlen > 100.:
            ret = (2, "The capillary is full")
        else:
            ret = (0, "")
            
        #floor for values
        if hydroinj > capilaryvol:
            hydroinj = capilaryvol
        if plugpertotallen > 100.:
            plugpertotallen = 100.
        if plugpertowinlen > 100.:
            plugpertowinlen = 100.
        
        store.put("Hydrodynamicinjection", value=hydroinj, unit="nL")
        store.put("Capillaryvolume", value=capilaryvol, unit="nL")
        store.put("Capillaryvolumetowin", value=capilaryvoltowin, unit="nL")
        store.put("Injectionpluglen", value=pluglen, unit="mm")
        store.put("Pluglenpertotallen", value=plugpertotallen, unit="%")
        store.put("Pluglenperlentowin", value=plugpertowinlen, unit="%")
        #store.put("Timetoreplaces", value=timetoonevols, unit="s")
        #store.put("Timetoreplacem", value=timetoonevolm, unit="min")
        store.put("Injectedanalyteng", value=analyteinjng, unit="ng")
        store.put("Injectedanalytepmol", value=analyteinjpmol, unit="pmol")
        store.put("Injectionpressure", value=injpressure, unit="psi/s")
        store.put("Fieldstrength", value=strengh, unit="V/cm")
        store.put("Flowrate", value=flowrate, unit="nL/min")
        
        return ret
            
        
    def save_mobility_result(self):
        """ compute and save the result for the mobility result """
        store = get_store()
        try :
            microeof = self.micro_eof()
        except ZeroDivisionError:
            if self.electro_osmosis_time == 0:
                return 1, "The EOF Time cannot be null" 
            else:
                return 1, "The voltage cannot be null" 
        
        if self.to_window_length > self.total_length:
            return 1, "The length to window cannot be greater than the capillary length"
        
        store.put("MicroEOF", value=microeof, unit="cm²/V/s")
        for i in range(1, store.get('Nbtimecompound')["value"]+1):
            keystore = "Timecompound"+str(i)
            time = TimeUnits.convert_unit(float(store.get(keystore)["value"]),
                                                store.get(keystore)["unit"], 
                                                u"s")
            
            microep = self.micro_ep(time)
            store.put("MicroEP"+str(i), value=microep, unit="cm²/V/s")
        return 0, ""
