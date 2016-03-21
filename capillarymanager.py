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
CapillaryManager
==================

The CapillaryManager class is used to interface the Kivy store class
and the capillary.

'''
# System import
import math

# Project import
from store import get_store
from capillary import Capillary
from convertunits import (LengthUnits, PressureUnits, TimeUnits,
                          ConcentrationUnits, MolConcentrationUnits,
                          MolWeightUnits, VoltUnits)

class CapillaryManager:
    '''CapillaryManager class
    '''
    def __init__(self):
        '''Get all needed values from the store
        '''
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
            concentration = MolConcentrationUnits.convert_unit(float(store.get('Concentration')["value"]),
                                                                 store.get('Concentration')["unit"],
                                                                 u"mol/L")
            self.concentration = self.molweight * concentration
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
        self.capillary = Capillary(self.total_length, self.to_window_length,
                                   self.diameter, self.pressure,
                                   self.duration, self.viscosity, self.molweight,
                                   self.concentration, self.voltage,
                                   self.electric_current,
                                   self.detection_time,
                                   self.electro_osmosis_time)

    def delivered_volume(self):
        '''Return the volume delivered during the injection
        '''
        return self.capillary.delivered_volume()

    def capillary_volume(self):
        '''Return the volume of the capillary
        '''
        return self.capillary.capillary_volume()

    def to_window_volume(self):
        '''Return the volume to window
        '''
        return self.capillary.to_window_volume()

    def injection_plug_length(self):
        '''Return the plug_length used in the injection
        '''
        return self.capillary.injection_plug_length()

    def time_to_replace_volume(self):
        '''Return the time required to replace the volume
        '''
        return self.capillary.time_to_replace_volume()

    def compute_viscosity(self):
        '''Return an assessment of the viscosity
        '''
        return self.capillary.compute_viscosity()

    def compute_conductivity(self):
        '''Return the conductivity
        '''
        return self.capillary.compute_conductivity()

    def field_strength(self):
        '''Return the field strength
        '''
        return self.capillary.field_strength()

    def micro_eof(self):
        '''Return the Micro EOF
        '''
        return self.capillary.micro_eof()

    def length_per_minute(self):
        '''Return the length per minute
        '''
        return self.capillary.length_per_minute()

    def flow_rate_inj(self):
        '''Return the flow rate for the flow rate screen
        '''
        flow_rate_inj_per_second = self.capillary.flow_rate_inj()
        return flow_rate_inj_per_second / TimeUnits.convert_unit(1, u"s", u"min")

    def flow_rate_flow(self):
        '''Return the flow rate per minute for the flow screen
        '''
        return self.capillary.flow_rate_flow()

    def injection_pressure(self):
        '''Return the injection pressure in psi per second
        '''
        inj_pressure = self.capillary.injection_pressure()
        return inj_pressure * PressureUnits.convert_unit(1, u"mbar", u"psi")

    def analyte_injected_ng(self):
        '''Return the analyte injected in ng
        '''
        return self.capillary.analyte_injected_ng()

    def analyte_injected_pmol(self):
        '''Return the analyte injected in pmol
        '''
        return self.capillary.analyte_injected_pmol()

    def micro_app(self, time):
        '''Return the micro_app time in second
        '''
        return self.capillary.micro_app(time)

    def micro_ep(self, time):
        '''Return the micro_ep time in second
        '''
        return self.capillary.micro_ep(time)

    def save_vicosity_result(self):
        '''Compute and save the results for the vicosity screen
        '''
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
        #saving
        store.put('Viscosity', value=viscosity, unit="cp")
        return 0, ""

    def save_conductivy_result(self):
        '''Compute and save the result for the conductivy screen
        '''
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
        '''Compute and save the result for the flow screen
        '''
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
        #saving
        store.put("Fieldstrength", value=strengh, unit="V/cm")
        store.put("MicroEOF", value=microeof, unit="cm²/V/s")
        store.put("Lengthpermin", value=LengthUnits.convert_unit(lpermin, u'm', u'cm'), unit="cm")
        store.put("Flowrate", value=flowrate, unit="nL/min")
        return 0, ""

    def save_injection_result(self):
        '''Compute and save the result for the injection screen
        '''
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
        #saving
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
        '''Compute and save the result for the mobility result
        '''
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
        #saving
        store.put("MicroEOF", value=microeof, unit="cm²/V/s")
        for i in range(1, store.get('Nbtimecompound')["value"]+1):
            keystore = "Timecompound"+str(i)
            time = TimeUnits.convert_unit(float(store.get(keystore)["value"]),
                                                store.get(keystore)["unit"],
                                                u"s")

            microep = self.micro_ep(time)
            store.put("MicroEP"+str(i), value=microep, unit="cm²/V/s")
        return 0, ""
