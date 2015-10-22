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
store.py
=========

Contain fonctions to create and access to the store

"""

from kivy.storage.jsonstore import JsonStore


def get_store():
	""" get_store return the store (it's a JsonStore).
	See kivy documentation for more information :
	http://kivy.org/docs/api-kivy.storage.html#module-kivy.storage
	@return : A JsonStore object
	@rtype : JsonStore
	"""
    store = JsonStore('cetoolboxdata.json')
    return store

def create_store():
    """ function to create a JsonStore.
    See kivy documentation for more information :
	http://kivy.org/docs/api-kivy.storage.html#module-kivy.storage
    """
    store = get_store()
    if not store.exists('Capillary'):
        store.put('Capillary', value=100.00, unit="cm")
    if not store.exists('Towindow'):
        store.put('Towindow', value=100.00, unit="cm")
    if not store.exists('Idiameter'):
        store.put('Idiameter', value=50.00, unit="µm")
    if not store.exists('Pressure'):
        store.put('Pressure', value=50.00, unit="mbar")
    if not store.exists('Time'):
        store.put('Time', value=50.00, unit="s")
    if not store.exists('Viscosity'):
        store.put('Viscosity', value=1.0, unit="cp")
    if not store.exists('Concentration'):
        store.put('Concentration', value=1.0, unit="g/L")
    if not store.exists('Molweight'):
        store.put('Molweight', value=1000.0, unit="g/mol")
    if not store.exists('Detectiontime'):
        store.put('Detectiontime', value=10.0, unit="min")
    if not store.exists('Voltage'):
        store.put('Voltage', value=3.0, unit="V")
    if not store.exists('Electriccurrent'):
        store.put('Electriccurrent', value=10.0, unit="µA")
    if not store.exists('Electroosmosis'):
        store.put('Electroosmosis', value=1.0, unit="min")  
    if not store.exists("Timecompound1"):
        store.put('Timecompound1', value=1.0, unit="min")
    if not store.exists("Nbtimecompound"):
        store.put('Nbtimecompound', value=1)
    if not store.exists("pause"):
		store.put('pause', value="menu")
