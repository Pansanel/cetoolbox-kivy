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
convertunits.py
=========

Contain static class to do convertions of units

"""

from externlib.firkin import UnitManager, SIFamily, Family

class BaseUnits:
    """ A class use to be herited to convert value"""

    @classmethod
    def convert_unit(cls, value, from_unit, to_unit):
        """ Convert the value from an unit to another unit
        @param value: the value to convert
        @type value: float
        @param from_unit: the unit of the value
        @type from_unit: unicode
        @param to_unit: the unit to get
        @type to_unit: unicode"""
        raise NotImplementedError("""You must implement convert_unit's 
            %s method""" % type(self).__name__)

class LengthUnits(BaseUnits):
    """ a class use to convert length (only the metric system)
    all the major type m, mm, km, etc. and the cm
    """
    lengths = UnitManager()
    lengths.add(SIFamily(base='m', name='metter')) 
    centimeter = Family(name='centimeter', base='cm')
    lengths.add(centimeter, other="metter", factor=0.01)

    @classmethod
    def convert_unit(cls, value, from_unit, to_unit):
        """ Convert the value from an unit to another unit
        @param value: the value to convert
        @type value: float
        @param from_unit: the unit of the value
        @type from_unit: unicode
        @param to_unit: the unit to get
        @type to_unit: unicode
        @return: the value converted
        @rtype: float"""
        val = cls.lengths.convert_to_unit(value, from_unit, to_unit)[0]
        return float(val)

class PressureUnits(BaseUnits):
    """ a class use to convert pressure.
    Handle all the bar familly mbar, bar, kbar and the pascal (pa)
    and the psi """
    pressures = UnitManager()
    pressures.add(SIFamily(base='bar', name='bar'))
    otherpressures = Family(name='pressure', base='pa')
    otherpressures.add('psi', 6894.8, 'pa')
    pressures.add(otherpressures, other='bar', factor=0.00001)

    @classmethod
    def convert_unit(cls, value, from_unit, to_unit):
        """ Convert the value from an unit to another unit
        @param value: the value to convert
        @type value: float
        @param from_unit: the unit of the value
        @type from_unit: unicode
        @param to_unit: the unit to get
        @type to_unit: unicode
        @return: the value converted
        @rtype: float"""
        val = cls.pressures.convert_to_unit(value, from_unit, to_unit)[0]
        return float(val)

class TimeUnits(BaseUnits):
    """ a class use to convert time.
    Handle s, min, h """
    times = Family(name='time', base='s')
    times.add('min', 60, 's')
    times.add('h', 60, 'min')

    @classmethod
    def convert_unit(cls, value, from_unit, to_unit):
        """ Convert the value from an unit to another unit
        @param value: the value to convert
        @type value: float
        @param from_unit: the unit of the value
        @type from_unit: unicode
        @param to_unit: the unit to get
        @type to_unit: unicode
        @return: the value converted
        @rtype: float"""
        val = cls.times.convert(value, from_unit, to_unit)[0]
        return float(val)

class ConcentrationUnits(BaseUnits):
    """ a class use to convert concentation.
    Handle all the g/L familly : mg/L, g/L, Kg/L, etc."""
    concentration = UnitManager()
    concentration.add(SIFamily(base='g/L', name='gramm per litter'))

    @classmethod
    def convert_unit(cls, value, from_unit, to_unit):
        """ Convert the value from an unit to another unit
        @param value: the value to convert
        @type value: float
        @param from_unit: the unit of the value
        @type from_unit: unicode
        @param to_unit: the unit to get
        @type to_unit: unicode
        @return: the value converted
        @rtype: float"""
        val = cls.concentration.convert_to_unit(value, from_unit, to_unit)[0]
        return float(val)

class MolConcentrationUnits(BaseUnits):
    """ a class use to convert molar concentation.
    Handle all the mol/L familly : mmol/L, mol/L, kmol/L, etc."""
    molconcentration = UnitManager()
    molconcentration.add(SIFamily(base='mol/L', name='mol per litter'))

    @classmethod
    def convert_unit(cls, value, from_unit, to_unit):
        """ Convert the value from an unit to another unit
        @param value: the value to convert
        @type value: float
        @param from_unit: the unit of the value
        @type from_unit: unicode
        @param to_unit: the unit to get
        @type to_unit: unicode
        @return: the value converted
        @rtype: float"""
        val = cls.molconcentration.convert_to_unit(value, from_unit, to_unit)[0]
        return float(val)

class MolWeightUnits(BaseUnits):
    """ a class use to convert molar weight.
    Handle all the g/mol familly : mg/mol, g/mol, Kg/mol, etc."""
    molweight = UnitManager()
    molweight.add(SIFamily(base='g/mol', name='gramm per mol'))

    @classmethod
    def convert_unit(cls, value, from_unit, to_unit):
        """ Convert the value from an unit to another unit
        @param value: the value to convert
        @type value: float
        @param from_unit: the unit of the value
        @type from_unit: unicode
        @param to_unit: the unit to get
        @type to_unit: unicode
        @return: the value converted
        @rtype: float"""
        val = cls.molweight.convert_to_unit(value, from_unit, to_unit)[0]
        return float(val)

class VoltUnits(BaseUnits):
    """ a class use to convert the volt familly.
    Handle all the V familly : mV, V, KV, etc."""
    voltage = UnitManager()
    voltage.add(SIFamily(base='V', name='Volt'))

    @classmethod
    def convert_unit(cls, value, from_unit, to_unit):
        """ Convert the value from an unit to another unit
        @param value: the value to convert
        @type value: float
        @param from_unit: the unit of the value
        @type from_unit: unicode
        @param to_unit: the unit to get
        @type to_unit: unicode
        @return: the value converted
        @rtype: float"""
        val = cls.voltage.convert_to_unit(value, from_unit, to_unit)[0]
        return float(val)

if __name__ == "__main__":
    print(LengthUnits.convert_unit(1000, 'µm', 'm'))
    print(LengthUnits.convert_unit(100, 'cm', 'm'))
    print(PressureUnits.convert_unit(3, 'psi', 'pa'))
    print(PressureUnits.convert_unit(1, 'bar', 'pa'))
    print(TimeUnits.convert_unit(30, 's', 'm'))
    print(ConcentrationUnits.convert_unit(42, 'mg/L', 'g/L'))
