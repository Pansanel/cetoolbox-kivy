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

import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.utils import platform

from os.path import join
import re

from store import get_store, create_store
from capillary import Capillary


#when the keyboard is open resize the window
Window.softinput_mode = 'resize'
#to test when the version 1.9.1 of kivy is out
#~ Window.softinput_mode = 'below_target'




__version__ = '0.0.7'

def add_color(text, color):
    return "[color="+color+"]"+text+"[/color]"
  
class FloatInput(TextInput):
    pass
    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)

class CEToolBoxLabel(Label):
    pass

class CEToolBoxTextInput(FloatInput):
    pass

class CEToolBoxSpinner(Spinner):
    pass

class CEToolBoxPopup(Popup):
    pass
    
class MenuScreen(Screen):
    pass

class ErrorPopup(CEToolBoxPopup):
    
    def show_popup(self, data):
        message = add_color(data["errtext"], "FF0000")
        self.ids.errormessage.text = message
        self.open()

class ViscosityPopup(CEToolBoxPopup):
    
    def show_popup(self, data):
        store = get_store()
        
        self.ids.inlayout.rows = 1
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Viscosity :", "FFFFFF")))
        value = round(store.get('Viscosity')["value"], 2)
        viscotext = str(value)+" "+store.get('Viscosity')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(viscotext, "FFFFFF")))
        self.open()

class InjectionPopup(CEToolBoxPopup):
    
    def show_popup(self, data):
        store = get_store()
        
        if data["errcode"] == 2:
            self.ids.inlayout.rows = 14
        else:
            self.ids.inlayout.rows = 13
        
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Hydrodynamic injection :", "FFFFFF")))
        value = round(store.get('Hydrodynamicinjection')["value"], 2)
        value = str(value)+" "+store.get('Hydrodynamicinjection')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value, "FFFFFF")))
        
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Capillary volume :", "BFBFBF")))
        value = round(store.get('Capillaryvolume')["value"], 2)
        value = str(value)+" "+store.get('Capillaryvolume')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value, "BFBFBF")))
        
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Capillary volume to window :", "FFFFFF")))
        value = round(store.get('Capillaryvolumetowin')["value"], 2)
        value = str(value)+" "+store.get('Capillaryvolumetowin')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value, "FFFFFF")))
        
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Injection plug length :", "BFBFBF")))
        value = round(store.get('Injectionpluglen')["value"], 2)
        value = str(value)+" "+store.get('Injectionpluglen')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value, "BFBFBF")))
                
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Plug (% of total length) :", "FFFFFF")))
        value = round(store.get('Pluglenpertotallen')["value"], 2)
        value = str(value)+" "+store.get('Pluglenpertotallen')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value, "FFFFFF")))
                
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Plug (% of length to window) :", "BFBFBF")))
        value = round(store.get('Pluglenperlentowin')["value"], 2)
        value = str(value)+" "+store.get('Pluglenperlentowin')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value, "BFBFBF")))
            
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Time to replace 1 volume :", "FFFFFF")))
        value = round(store.get('Timetoreplaces')["value"], 2)
        value = str(value)+" "+store.get('Timetoreplaces')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value, "FFFFFF")))
        
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=""))
        value = round(store.get('Timetoreplacem')["value"], 2)
        value = str(value)+" "+store.get('Timetoreplacem')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value, "FFFFFF")))
                
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Injected analyte :", "BFBFBF")))
        value = round(store.get('Injectedanalyteng')["value"], 2)
        value = str(value)+" "+store.get('Injectedanalyteng')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value, "BFBFBF")))
    
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=""))
        value = round(store.get('Injectedanalytepmol')["value"], 2)
        value = str(value)+" "+store.get('Injectedanalytepmol')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value, "BFBFBF")))
        
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Injection pressure :", "FFFFFF")))
        value = round(store.get('Injectionpressure')["value"], 2)
        value = str(value)+" "+store.get('Injectionpressure')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value, "FFFFFF")))
        
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Flow rate :", "BFBFBF")))
        value = round(store.get('Flowrate')["value"], 2)
        value = str(value)+" "+store.get('Flowrate')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value, "BFBFBF")))
        
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Field strength :", "FFFFFF")))
        value = round(store.get('Fieldstrength')["value"], 2)
        value = str(value)+" "+store.get('Fieldstrength')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value, "FFFFFF")))
        
        if data["errcode"] == 2:
            self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Warning :", "FF0000")))
            self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(data["errtext"], "FF0000")))
        
        self.open()
        
class ConductivityPopup(CEToolBoxPopup):
    
    def show_popup(self, data):
        store = get_store()
        
        self.ids.inlayout.rows = 1
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Conductivity :", "FFFFFF")))
        value = round(store.get('Conductivity')["value"], 2)
        conductivitytext = str(value)+" "+store.get('Conductivity')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(conductivitytext, "FFFFFF")))
        self.open()

class FlowPopup(CEToolBoxPopup):
    
    def show_popup(self, data):
        store = get_store()
        
        self.ids.inlayout.rows = 4
        
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Field strength :", "FFFFFF")))
        value = round(store.get('Fieldstrength')["value"], 2)
        value = str(value)+" "+store.get('Fieldstrength')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value, "FFFFFF")))
        
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("µEOF :","BFBFBF")))
        value = "{:.2E}".format(store.get('MicroEOF')["value"])
        value = value +" "+store.get('MicroEOF')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value,"BFBFBF")))
        
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Length per min :", "FFFFFF")))
        value = round(store.get('Lengthpermin')["value"], 2)
        value = str(value)+" "+store.get('Lengthpermin')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value,"FFFFFF")))
        
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("Flow rate :", "BFBFBF")))
        value = round(store.get('Flowrate')["value"], 2)
        value = str(value)+" "+store.get('Flowrate')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value,"BFBFBF")))
        
        self.open()
        
class MobilityPopup(CEToolBoxPopup):
    
    def show_popup(self, data):
        store = get_store()
        
        self.ids.inlayout.rows = 1 + store.get('Nbtimecompound')["value"]
        
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("µEOF :","FFFFFF")))
        value = "{:.2E}".format(store.get('MicroEOF')["value"])
        value = value+" "+store.get('MicroEOF')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value,"FFFFFF")))
        
        for i in range(1, store.get('Nbtimecompound')["value"]+1):
            if i%2 != 0:
                color = "BFBFBF"
            else:
                color = "FFFFFF"
            
            self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color("µEP"+str(i)+" :", color)))
            value = "{:.2E}".format(store.get('MicroEP'+str(i))["value"])
            value = value +" "+store.get('MicroEP'+str(i))["unit"]
            self.ids.inlayout.add_widget(CEToolBoxLabel(text=add_color(value,color)))
        
        self.open()
        

class InjectionScreen(Screen):
    
    def on_pre_enter(self):
        """special function lauch at the clic of the button to go
        on the injectionscreen 
        this value comes from the json file where we keep it
        """
        store = get_store()
        self.ids.Capillary.text = str(store.get('Capillary')["value"])
        self.ids.CapillaryUnit.text = store.get('Capillary')["unit"]
        self.ids.Towindow.text = str(store.get('Towindow')["value"])
        self.ids.TowindowUnit.text = store.get('Towindow')["unit"]
        self.ids.Idiameter.text = str(store.get('Idiameter')["value"])
        self.ids.IdiameterUnit.text = unicode(store.get('Idiameter')["unit"])
        self.ids.Pressure.text = str(store.get('Pressure')["value"])
        self.ids.PressureUnit.text = store.get('Pressure')["unit"]
        self.ids.Time.text = str(store.get('Time')["value"])
        self.ids.TimeUnit.text = store.get('Time')["unit"]
        self.ids.Viscosity.text = str(store.get('Viscosity')["value"])
        self.ids.ViscosityUnit.text = store.get('Viscosity')["unit"]
        self.ids.Concentration.text = str(store.get('Concentration')["value"])
        self.ids.ConcentrationUnit.text = store.get('Concentration')["unit"]
        self.ids.Molweight.text = str(store.get('Molweight')["value"])
        self.ids.MolweightUnit.text = store.get('Molweight')["unit"]
        self.ids.Voltage.text = str(store.get('Voltage')["value"])
        self.ids.VoltageUnit.text = store.get('Voltage')["unit"]
    
    
    def show_injection_results(self):
        """ lauch when clicked on result"""
        #save data
        store = get_store()
        store.put('Capillary', value=float(self.ids.Capillary.text),
                  unit=self.ids.CapillaryUnit.text)
        store.put('Towindow', value=float(self.ids.Towindow.text),
                  unit=self.ids.TowindowUnit.text)
        store.put('Idiameter', value=float(self.ids.Idiameter.text),
                  unit=self.ids.IdiameterUnit.text)
        store.put('Pressure', value=float(self.ids.Pressure.text),
                  unit=self.ids.PressureUnit.text)
        store.put('Time', value=float(self.ids.Time.text),
                  unit=self.ids.TimeUnit.text)
        store.put('Viscosity', value=float(self.ids.Viscosity.text),
                  unit=self.ids.ViscosityUnit.text)
        store.put('Concentration', 
                  value=float(self.ids.Concentration.text), 
                  unit=self.ids.ConcentrationUnit.text)
        store.put('Molweight', value=float(self.ids.Molweight.text),
                  unit=self.ids.MolweightUnit.text)
        store.put('Voltage', value=float(self.ids.Voltage.text),
                  unit=self.ids.VoltageUnit.text)
                  
        
        #add data          
        computation = Capillary()
        errcode, errtext = computation.save_injection_result()
        
        data = {}
        data["errcode"] = errcode
        data["errtext"] = errtext
        
        if data["errcode"] == 1:
            self._popup = ErrorPopup()
        else:
            self._popup = InjectionPopup()
        self._popup.show_popup(data)
    
        

class ViscosityScreen(Screen):
    
    def on_pre_enter(self):
        """special function lauch at the clic of the button to go
        on the injectionscreen 
        this value comes from the json file where we keep it
        """
        store = get_store()
        self.ids.Capillary.text = str(store.get('Capillary')["value"])
        self.ids.CapillaryUnit.text = store.get('Capillary')["unit"]
        self.ids.Towindow.text = str(store.get('Towindow')["value"])
        self.ids.TowindowUnit.text = store.get('Towindow')["unit"]
        self.ids.Idiameter.text = str(store.get('Idiameter')["value"])
        self.ids.IdiameterUnit.text = unicode(store.get('Idiameter')["unit"])
        self.ids.Pressure.text = str(store.get('Pressure')["value"])
        self.ids.PressureUnit.text = store.get('Pressure')["unit"]
        self.ids.Detectiontime.text = str(store.get('Detectiontime')["value"])
        self.ids.DetectiontimeUnit.text = store.get('Detectiontime')["unit"]
    
    
    def show_viscosity_results(self):
        """ lauch when clicked on result"""
        #save data
        store = get_store()
        store.put('Capillary', value=float(self.ids.Capillary.text),
                  unit=self.ids.CapillaryUnit.text)
        store.put('Towindow', value=float(self.ids.Towindow.text),
                  unit=self.ids.TowindowUnit.text)
        store.put('Idiameter', value=float(self.ids.Idiameter.text),
                  unit=self.ids.IdiameterUnit.text)
        store.put('Pressure', value=float(self.ids.Pressure.text),
                  unit=self.ids.PressureUnit.text)
        store.put('Detectiontime', value=float(self.ids.Detectiontime.text),
                  unit=self.ids.DetectiontimeUnit.text)
        
        computation = Capillary()
        errcode, errtext = computation.save_vicosity_result()
        
        data = {}
        data["errcode"] = errcode
        data["errtext"] = errtext
        
        if data["errcode"] == 1:
            self._popup = ErrorPopup()
        else:
            self._popup = ViscosityPopup()
        self._popup.show_popup(data)


class ConductivityScreen(Screen):
    
    def on_pre_enter(self):
        """special function lauch at the clic of the button to go
        on the injectionscreen 
        this value comes from the json file where we keep it
        """
        store = get_store()
        self.ids.Capillary.text = str(store.get('Capillary')["value"])
        self.ids.CapillaryUnit.text = store.get('Capillary')["unit"]
        self.ids.Towindow.text = str(store.get('Towindow')["value"])
        self.ids.TowindowUnit.text = store.get('Towindow')["unit"]
        self.ids.Idiameter.text = str(store.get('Idiameter')["value"])
        self.ids.IdiameterUnit.text = store.get('Idiameter')["unit"]
        self.ids.Voltage.text = str(store.get('Voltage')["value"])
        self.ids.VoltageUnit.text = store.get('Voltage')["unit"]
        self.ids.Electriccurrent.text = str(store.get('Electriccurrent')["value"])
        self.ids.ElectriccurrentUnit.text = store.get('Electriccurrent')["unit"]
    
    def show_conductivity_results(self):
        #save data
        store = get_store()
        store.put('Capillary', value=float(self.ids.Capillary.text),
                  unit=self.ids.CapillaryUnit.text)
        store.put('Towindow', value=float(self.ids.Towindow.text),
                  unit=self.ids.TowindowUnit.text)
        store.put('Idiameter', value=float(self.ids.Idiameter.text),
                  unit=self.ids.IdiameterUnit.text)
        store.put('Voltage', value=float(self.ids.Voltage.text),
                  unit=self.ids.VoltageUnit.text)
        store.put('Electriccurrent', value=float(self.ids.Electriccurrent.text),
                  unit=self.ids.ElectriccurrentUnit.text)
        
        computation = Capillary()
        errcode, errtext = computation.save_conductivy_result()
        
        data = {}
        data["errcode"] = errcode
        data["errtext"] = errtext
        
        if data["errcode"] == 1:
            self._popup = ErrorPopup()
        else:
            self._popup = ConductivityPopup()
        self._popup.show_popup(data)

class FlowScreen(Screen):
    
    def on_pre_enter(self):
        """special function lauch at the clic of the button to go
        on the injectionscreen 
        this value comes from the json file where we keep it
        """
        store = get_store()
        self.ids.Capillary.text = str(store.get('Capillary')["value"])
        self.ids.CapillaryUnit.text = store.get('Capillary')["unit"]
        self.ids.Towindow.text = str(store.get('Towindow')["value"])
        self.ids.TowindowUnit.text = store.get('Towindow')["unit"]
        self.ids.Idiameter.text = str(store.get('Idiameter')["value"])
        self.ids.IdiameterUnit.text = store.get('Idiameter')["unit"]
        self.ids.Voltage.text = str(store.get('Voltage')["value"])
        self.ids.VoltageUnit.text = store.get('Voltage')["unit"]
        self.ids.Electroosmosis.text = str(store.get('Electroosmosis')["value"])
        self.ids.ElectroosmosisUnit.text = store.get('Electroosmosis')["unit"]
    
    
    def show_flow_results(self):
                #save data
        store = get_store()
        store.put('Capillary', value=float(self.ids.Capillary.text),
                  unit=self.ids.CapillaryUnit.text)
        store.put('Towindow', value=float(self.ids.Towindow.text),
                  unit=self.ids.TowindowUnit.text)
        store.put('Idiameter', value=float(self.ids.Idiameter.text),
                  unit=self.ids.IdiameterUnit.text)
        store.put('Voltage', value=float(self.ids.Voltage.text),
                  unit=self.ids.VoltageUnit.text)
        store.put('Electroosmosis', value=float(self.ids.Electroosmosis.text),
                  unit=self.ids.ElectroosmosisUnit.text)
        
        computation = Capillary()
        errcode, errtext = computation.save_flow_result()
        
        data = {}
        data["errcode"] = errcode
        data["errtext"] = errtext
        
        if data["errcode"] == 1:
            self._popup = ErrorPopup()
        else:
            self._popup = FlowPopup()
        self._popup.show_popup(data)


class MobilityScreen(Screen):
    
    def show_mobility_results(self):
        #save data
        store = get_store()
        store.put('Capillary', value=float(self.ids.Capillary.text),
                  unit=self.ids.CapillaryUnit.text)
        store.put('Towindow', value=float(self.ids.Towindow.text),
                  unit=self.ids.TowindowUnit.text)
        store.put('Voltage', value=float(self.ids.Voltage.text),
                  unit=self.ids.VoltageUnit.text)
        store.put('Electroosmosis', value=float(self.ids.Electroosmosis.text),
                  unit=self.ids.ElectroosmosisUnit.text)
        
        #save all the timecompound
        for sublist in self.timecompoundlist:
            store.put(sublist[1].id, value=float(sublist[1].text),
                      unit=sublist[2].text)
        
        computation = Capillary()
        errcode, errtext = computation.save_mobility_result()
        
        data = {}
        data["errcode"] = errcode
        data["errtext"] = errtext
        
        if data["errcode"] == 1:
            self._popup = ErrorPopup()
        else:
            self._popup = MobilityPopup()
        self._popup.show_popup(data)
    
    def on_pre_enter(self):
        """special function lauch at the clic of the button to go
        on the injectionscreen 
        this value comes from the json file where we keep it
        """        
        store = get_store()
        self.ids.Capillary.text = str(store.get('Capillary')["value"])
        self.ids.CapillaryUnit.text = store.get('Capillary')["unit"]
        self.ids.Towindow.text = str(store.get('Towindow')["value"])
        self.ids.TowindowUnit.text = store.get('Towindow')["unit"]
        self.ids.Voltage.text = str(store.get('Voltage')["value"])
        self.ids.VoltageUnit.text = store.get('Voltage')["unit"]
        self.ids.Electroosmosis.text = str(store.get('Electroosmosis')["value"])
        self.ids.ElectroosmosisUnit.text = store.get('Electroosmosis')["unit"]
        self.ids.Timecompound1.text = str(store.get('Timecompound1')["value"])
        self.ids.Timecompound1Unit.text = store.get('Timecompound1')["unit"]
        
        #set the number of rows
        self.ids.inlayout.rows = 5 + store.get('Nbtimecompound')["value"]
        #force the good size
        self.ids.tscrollview.change_child_height(self.ids.tscrollview.height)
        
        #set the rest of the time compound
        self.timecompoundlist = []
        for i in range(2, store.get('Nbtimecompound')["value"]+1):
            timecompount = CEToolBoxLabel(text="Time compound "+str(i))
            timecompountvalue = CEToolBoxTextInput(text=str(store.get('Timecompound'+str(i))["value"]),
                                                   id='Timecompound'+str(i))
            timecompountunit =  CEToolBoxSpinner(text=store.get('Timecompound'+str(i))["unit"],
                                                 id='Timecompound'+str(i)+'Unit', 
                                                 values=["s", "min"])
            self.ids.inlayout.add_widget(timecompount)
            self.ids.inlayout.add_widget(timecompountvalue)
            self.ids.inlayout.add_widget(timecompountunit)
            tosave = [timecompount, timecompountvalue, timecompountunit]
            self.timecompoundlist.append(tosave)
            
        #create the button add and del
        self.add_button = Button(text="Add", id="addbutton", on_release=self.add_line)
        self.ids.inlayout.add_widget(self.add_button)
        self.del_button = Button(text="Del", id="delbutton", on_release=self.del_line)
        self.ids.inlayout.add_widget(self.del_button)
            
    def add_line(self, buttoninstance):
        #del and create again to respect the order
        self.ids.inlayout.remove_widget(self.add_button)
        self.ids.inlayout.remove_widget(self.del_button)
        
        #create the new line
        store = get_store()
        lastval = store.get('Nbtimecompound')["value"]
        store.put('Nbtimecompound', value=1+lastval)
        self.ids.inlayout.rows = 5 + store.get('Nbtimecompound')["value"]
        
        #add the widget
        newval = str(store.get('Nbtimecompound')["value"])
        timecompount = CEToolBoxLabel(text="Time compound "+newval)
        timecompountvalue = CEToolBoxTextInput(text=str(1.0),
                                               id='Timecompound'+newval)
        timecompountunit =  CEToolBoxSpinner(text=u"min",
                                             id='Timecompound'+newval+'Unit', 
                                             values=["s", "min"])
        store.put('Timecompound'+newval, value=1.0, unit="min")
        self.ids.inlayout.add_widget(timecompount)
        self.ids.inlayout.add_widget(timecompountvalue)
        self.ids.inlayout.add_widget(timecompountunit)
        tosave = [timecompount, timecompountvalue, timecompountunit]
        self.timecompoundlist.append(tosave)
        
        #recreate the button
        self.add_button = Button(text="Add", id="addbutton", on_release=self.add_line)
        self.ids.inlayout.add_widget(self.add_button)
        self.del_button = Button(text="Del", id="delbutton", on_release=self.del_line)
        self.ids.inlayout.add_widget(self.del_button)
        self.ids.inlayout.rows = 5 + store.get('Nbtimecompound')["value"]
        
        #force the good size
        self.ids.tscrollview.change_child_height(self.ids.tscrollview.height)
        
        
    def del_line(self, buttoninstance):
        try:
            widgets = self.timecompoundlist.pop()
        except IndexError:
            return
        for w in widgets:
            self.ids.inlayout.remove_widget(w)
        
        store = get_store()
        lastval = store.get('Nbtimecompound')["value"]
        store.delete('Timecompound'+str(lastval))
        store.put('Nbtimecompound', value=lastval-1)
        self.ids.inlayout.rows = 5 + store.get('Nbtimecompound')["value"]
        
        #force the good size
        self.ids.tscrollview.change_child_height(self.ids.tscrollview.height)
            
        
    def on_leave(self):
        for widgets in self.timecompoundlist:
            for w in widgets:
                self.ids.inlayout.remove_widget(w)
        self.ids.inlayout.remove_widget(self.add_button)
        self.ids.inlayout.remove_widget(self.del_button)
    
    def reset(self):
        store = get_store()
        nbval = store.get('Nbtimecompound')["value"]
        for i in range(1, nbval):
            self.del_line(1) 
        
        
    

class AboutScreen(Screen):
    
    def on_pre_enter(self):
        self.ids.alabel.text = """[b][size=20]CEToolBox kivy v"""+ __version__ +"""[/size][/b]\n"""
        


class CEToolBoxLayout(GridLayout):
    
    def set_min_height(self):
        self.minimum_height = 350
    
    def set_min_width(self):
        self.minimum_width = 350
    
    def change_height(self, height_par):
        #~ reset because of a bug in kivy
        #~ need to depend of the number of row 
        self.set_min_height()
        
        if height_par > self.minimum_height:
            self.height = height_par
        else:
            self.height = self.minimum_height
    
    def change_width(self, wid):
        #~ reset because of a bug in kivy
        self.set_min_width()
        
        if wid > self.minimum_width:
            self.width = wid
        else:
            self.width = self.minimum_width
    
    
class TopScreenLayout(CEToolBoxLayout):
    """ set the size of the layout from minimals values and the size
    of the scrollviewspe parrent."""
    def set_min_height(self):
        self.minimum_height = 40 *self.rows + 10 

class TopPopupLayout(CEToolBoxLayout):
    """ set the size of the layout from minimals values and the size
    of the scrollviewspe parrent."""
    def set_min_height(self):
        self.minimum_height = 40 *self.rows + 10 

    def set_min_width(self):
        self.minimum_width = 300
    
class DownMenuLayout(CEToolBoxLayout):
    """ set the size of the layout from minimals values and the size
    of the scrollviewspe parrent."""
    
    def set_min_height(self):
        self.minimum_height = 40 
    
class DownMenuClose(CEToolBoxLayout):
    
    def set_min_height(self):
        self.minimum_height = 40
    
    def set_min_width(self):
        self.minimum_width = 100
    
    
    
            
class ScrollViewSpe(ScrollView):
    """ Special class made to give it's own value at his layout child
    See the kv file for an exemple of use """
    
        
    def change_child_height(self, height_par):
        for child in self.children:
            child.change_height(height_par)
        return height_par

    def change_child_width(self, wid):
        for child in self.children:
            child.change_width(wid)
        return wid


class ManagerApp(App):
    title = "CEToolBox"
    create_store()
    
    
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(InjectionScreen(name='injection'))
        self.sm.add_widget(ViscosityScreen(name='viscosity'))
        self.sm.add_widget(ConductivityScreen(name='conductivity'))
        self.sm.add_widget(MobilityScreen(name='mobility'))
        self.sm.add_widget(FlowScreen(name='flow'))
        self.sm.add_widget(AboutScreen(name='about'))
        self.bind(on_start=self.post_build_init)
        return self.sm

    def post_build_init(self, *args):
        win = Window
        win.bind(on_keyboard=self.my_key_handler)

    def my_key_handler(self, window, keycode1, keycode2, text, modifiers):
        if keycode1 in [27, 1001]:
            self.sm.current = "menu"
            return True
        return False

    def on_pause(self):
        #perfect save but why ?
        store = get_store()
        store.put("pause", value=self.sm.current)
        return True
    
    def on_resume(self):
        pass
        store = get_store()
        self.sm.current = str(store.get('pause')["value"])

if __name__ == '__main__':
    ManagerApp().run()
