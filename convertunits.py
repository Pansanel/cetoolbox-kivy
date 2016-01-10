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
Units
=====

The Units provide a set of classes to manage units and unit conversion.

'''

class UnitList:
    '''A class to manage units and to convert values.
    '''
    def __init__(self, baseUnitAbbr, baseUnitName):
        self.baseUnitAbbr = baseUnitAbbr
        self.baseUnitName = baseUnitName
        self.units = {}
        self.units[baseUnitAbbr] = [baseUnitName, 1]

    def add_unit(self, unitAbbr, unitName, unitFactor = 1):
        self.units[unitAbbr] = [unitName, unitFactor]

    def get_factor(self, unitAbbr):
        return self.units[unitAbbr][1]

    def convert_to_unit(self, value, from_unit, to_unit):
        convertedValue = value * self.get_factor(from_unit) / self.get_factor(to_unit)
        return float(convertedValue)

class BaseUnits:
    '''A class use to be herited to convert value
    '''

    @classmethod
    def convert_unit(self, value, from_unit, to_unit):
        """
        @param value: the value to convert
        @type value: float
        @param from_unit: the unit of the value
        @type from_unit: unicode
        @param to_unit: the unit to get
        @type to_unit: unicode"""
        raise NotImplementedError("""You must implement convert_unit's 
            %s method""" % type(self).__name__)

class LengthUnits(BaseUnits):
    '''A class use to convert length (only the metric system)
    It handles µm, mm, cm and m.
    '''
    unitList = UnitList('m', 'metter')
    unitList.add_unit('cm', 'centimetter', 0.01)
    unitList.add_unit('mm', 'millimetter', 0.001)
    unitList.add_unit(u'µm', 'micrometter', 0.000001)

    @classmethod
    def convert_unit(cls, value, from_unit, to_unit):
        '''Convert the value from an unit to another unit
        @param value: the value to convert
        @type value: float
        @param from_unit: the unit of the value
        @type from_unit: unicode
        @param to_unit: the unit to get
        @type to_unit: unicode
        @return: the value converted
        @rtype: float'''
        val = cls.unitList.convert_to_unit(value, from_unit, to_unit)
        return float(val)

class PressureUnits(BaseUnits):
    '''A class use to convert pressure.
    It handles pa, mbar, bar and psi.
    '''
    unitList = UnitList('pa', 'pascal')
    unitList.add_unit('bar', 'bar',  100000.0)
    unitList.add_unit('mbar', 'millibar',  100.0)
    unitList.add_unit('psi', 'psi', 6894.8)

    @classmethod
    def convert_unit(cls, value, from_unit, to_unit):
        '''Convert the value from an unit to another unit
        @param value: the value to convert
        @type value: float
        @param from_unit: the unit of the value
        @type from_unit: unicode
        @param to_unit: the unit to get
        @type to_unit: unicode
        @return: the value converted
        @rtype: float'''
        val = cls.unitList.convert_to_unit(value, from_unit, to_unit)
        return float(val)

class TimeUnits(BaseUnits):
    '''A class use to convert time.
    It handles s, min and h.
    '''
    unitList = UnitList('s','seconde')
    unitList.add_unit('min','minute', 60.0)
    unitList.add_unit('h','hour', 3600.0)

    @classmethod
    def convert_unit(cls, value, from_unit, to_unit):
        '''Convert the value from an unit to another unit
        @param value: the value to convert
        @type value: float
        @param from_unit: the unit of the value
        @type from_unit: unicode
        @param to_unit: the unit to get
        @type to_unit: unicode
        @return: the value converted
        @rtype: float'''
        val = cls.unitList.convert_to_unit(value, from_unit, to_unit)
        return float(val)

class ConcentrationUnits(BaseUnits):
    '''A class use to convert concentration.
    It handles g/L and mg/L.
    '''
    unitList = UnitList('g/L','gramm per litter')
    unitList.add_unit('mg/L','milligram per litter', 0.001)

    @classmethod
    def convert_unit(cls, value, from_unit, to_unit):
        '''Convert the value from an unit to another unit
        @param value: the value to convert
        @type value: float
        @param from_unit: the unit of the value
        @type from_unit: unicode
        @param to_unit: the unit to get
        @type to_unit: unicode
        @return: the value converted
        @rtype: float'''
        val = cls.unitList.convert_to_unit(value, from_unit, to_unit)
        return float(val)
 
class MolConcentrationUnits(BaseUnits):
    '''A class use to convert molar concentration.
    It handles mol/L and mmol/L.
    '''
    unitList = UnitList('mol/L','mol per litter')
    unitList.add_unit('mmol/L','millimol per litter', 0.001)

    @classmethod
    def convert_unit(cls, value, from_unit, to_unit):
        '''Convert the value from an unit to another unit
        @param value: the value to convert
        @type value: float
        @param from_unit: the unit of the value
        @type from_unit: unicode
        @param to_unit: the unit to get
        @type to_unit: unicode
        @return: the value converted
        @rtype: float'''
        val = cls.unitList.convert_to_unit(value, from_unit, to_unit)
        return float(val)

class MolWeightUnits(BaseUnits):
    '''A class use to convert molar weight.
    It handles g/mol and mg/mol.
    '''
    unitList = UnitList('g/mol','gramm per mol')
    unitList.add_unit('mg/mol','milligram per mol', 0.001)

    @classmethod
    def convert_unit(cls, value, from_unit, to_unit):
        '''Convert the value from an unit to another unit
        @param value: the value to convert
        @type value: float
        @param from_unit: the unit of the value
        @type from_unit: unicode
        @param to_unit: the unit to get
        @type to_unit: unicode
        @return: the value converted
        @rtype: float'''
        val = cls.unitList.convert_to_unit(value, from_unit, to_unit)
        return float(val)

class VoltUnits(BaseUnits):
    '''A class use to convert the volt familly.
    It handles V, mV and KV.
    '''
    unitList = UnitList('V','Volt')
    unitList.add_unit('mV','millivolt', 0.001)
    unitList.add_unit('KV','kilovolt', 1000)

    @classmethod
    def convert_unit(cls, value, from_unit, to_unit):
        '''Convert the value from an unit to another unit
        @param value: the value to convert
        @type value: float
        @param from_unit: the unit of the value
        @type from_unit: unicode
        @param to_unit: the unit to get
        @type to_unit: unicode
        @return: the value converted
        @rtype: float'''
        val = cls.unitList.convert_to_unit(value, from_unit, to_unit)
        return float(val)

if __name__ == "__main__":
    print(LengthUnits.convert_unit(1000, u'µm', 'm'))
    print(LengthUnits.convert_unit(100, 'cm', u'µm'))
    print(PressureUnits.convert_unit(3, 'psi', 'pa'))
    print(PressureUnits.convert_unit(1, 'bar', 'pa'))
    print(TimeUnits.convert_unit(30, 's', 'min'))
    print(ConcentrationUnits.convert_unit(42, 'mg/L', 'g/L'))
