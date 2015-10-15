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
from os.path import join
import re

from store import get_store, create_store
from capillary import Capillary


__version__ = '0.0.2'


    
class FloatInput(TextInput):
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

class CEToolBoxPopupLabel(CEToolBoxLabel):
    pass


class MenuScreen(Screen):
    pass


class ViscosityPopup(Popup):
    
    def show_popup(self, data):
        #~ need error gestion => through data
        store = get_store()
        
        self.ids.inlayout.rows = 1
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="Viscosity :"))
        viscotext = str(store.get('Viscosity')["value"])+" "+store.get('Viscosity')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=viscotext))
        self.open()

class InjectionPopup(Popup):
    
    def show_popup(self, data):
        #~ need error gestion => through data
        store = get_store()
        
        self.ids.inlayout.rows = 13
        
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="Hydrodynamic \ninjection :"))
        value = str(store.get('Hydrodynamicinjection')["value"])+" "+store.get('Hydrodynamicinjection')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
        
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="Capillary volume :"))
        value = str(store.get('Capillaryvolume')["value"])+" "+store.get('Capillaryvolume')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
        
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="Capillary volume \nto window :"))
        value = str(store.get('Capillaryvolumetowin')["value"])+" "+store.get('Capillaryvolumetowin')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
        
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="Injection plug \nlength :"))
        value = str(store.get('Injectionpluglen')["value"])+" "+store.get('Injectionpluglen')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
                
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="Plug (% of \ntotal length) :"))
        value = str(store.get('Pluglenpertotallen')["value"])+" "+store.get('Pluglenpertotallen')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
                
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="Plug (% of \nlength to window) :"))
        value = str(store.get('Pluglenperlentowin')["value"])+" "+store.get('Pluglenperlentowin')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
                
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="Time to replace \n1 volume :"))
        value = str(store.get('Timetoreplaces')["value"])+" "+store.get('Timetoreplaces')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
        
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text=""))
        value = str(store.get('Timetoreplacem')["value"])+" "+store.get('Timetoreplacem')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
                
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="Injected analyte:"))
        value = str(store.get('Injectedanalyteng')["value"])+" "+store.get('Injectedanalyteng')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
    
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text=""))
        value = str(store.get('Injectedanalytepmol')["value"])+" "+store.get('Injectedanalytepmol')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
        
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="Injection pressure :"))
        value = str(store.get('Injectionpressure')["value"])+" "+store.get('Injectionpressure')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
        
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="Flow rate :"))
        value = str(store.get('Flowrate')["value"])+" "+store.get('Flowrate')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
        
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="Field strength :"))
        value = str(store.get('Fieldstrength')["value"])+" "+store.get('Fieldstrength')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
        
        self.open()
        
class ConductivityPopup(Popup):
    
    def show_popup(self, data):
        #~ need error gestion => through data
        store = get_store()
        
        self.ids.inlayout.rows = 1
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="Conductivity :"))
        conductivitytext = str(store.get('Conductivity')["value"])+" "+store.get('Conductivity')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=conductivitytext))
        self.open()

class FlowPopup(Popup):
    
    def show_popup(self, data):
        #~ need error gestion => through data
        store = get_store()
        
        self.ids.inlayout.rows = 4
        
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="Field strength :"))
        value = str(store.get('Fieldstrength')["value"])+" "+store.get('Fieldstrength')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
        
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="µEOF :"))
        value = str(store.get('MicroEOF')["value"])+" "+store.get('MicroEOF')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
        
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="Length per min :"))
        value = str(store.get('Lengthpermin')["value"])+" "+store.get('Lengthpermin')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
        
        self.ids.inlayout.add_widget(CEToolBoxPopupLabel(text="Flow rate :"))
        value = str(store.get('Flowrate')["value"])+" "+store.get('Flowrate')["unit"]
        self.ids.inlayout.add_widget(CEToolBoxLabel(text=value))
        
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
        computation.save_injection_result()
        
        data = {}
        data["error"] = 0
        
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
        computation.save_vicosity_result()
        data = {}
        data["error"] = 0
        
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
        computation.save_conductivy_result()
        
        data = {}
        data["error"] = 0
        
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
        computation.save_flow_result()
        
        data = {}
        data["error"] = 0
        
        self._popup = FlowPopup()
        self._popup.show_popup(data)

class AboutScreen(Screen):
    pass


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
        self.minimum_height = 30 
    
class DownMenuClose(CEToolBoxLayout):
    
    def set_min_height(self):
        self.minimum_height = 30
    
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
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(InjectionScreen(name='injection'))
        sm.add_widget(ViscosityScreen(name='viscosity'))
        sm.add_widget(ConductivityScreen(name='conductivity'))
        sm.add_widget(FlowScreen(name='flow'))
        sm.add_widget(AboutScreen(name='about'))
        return sm

if __name__ == '__main__':
    ManagerApp().run()
