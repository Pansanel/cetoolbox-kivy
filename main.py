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
from kivy.storage.jsonstore import JsonStore
from os.path import join

__version__ = '0.0.1'


def get_store():
    store = JsonStore('cetoolboxdata.json')
    return store

def create_store():
    """ function to create a file with default value of each var"""
    store = get_store()
    if not store.exists('Capillary'):
        store.put('Capillary', value=100.00, unit="Unit1")
    if not store.exists('Towindow'):
        store.put('Towindow', value=100.00, unit="Unit1")
    if not store.exists('Idiameter'):
        store.put('Idiameter', value=50.00, unit="Unit1")
    if not store.exists('Pressure'):
        store.put('Pressure', value=50.00, unit="Unit1")
    if not store.exists('Time'):
        store.put('Time', value=50.00, unit="Unit1")
    if not store.exists('Viscosity'):
        store.put('Viscosity', value=1.0, unit="Unit1")
    if not store.exists('Concentration'):
        store.put('Concentration', value=1.0, unit="Unit1")
    if not store.exists('Molweight'):
        store.put('Molweight', value=1000.0, unit="Unit1")


class MenuScreen(Screen):
    pass

class ViscosityPopup(Popup):
    pass

class InjectionPopup():
    
    def show_popup(self, data):
        
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text='Hydrodynamic injection: %s' % data['injection']))
        box.add_widget(Label(text='Capillary volume: %s' % data['volume']))
        button_close = Button(text='Close')
        box.add_widget(button_close)
        popup = Popup(title='Injection Details', content=box)
        button_close.bind(on_press=popup.dismiss)
        popup.open()

class ConductivityPopup(Popup):
    pass

class FlowPopup(Popup):
    pass

class InjectionScreen(Screen):
    
    def on_pre_enter(self):
        """special function lauch at the clic of the button to go
        on the injectionscreen 
        this value comes from the json file where we keep it
        """
        store = get_store()
        self.ids.Capillary.text = str(store.get('Capillary')["value"])
        self.ids.Towindow.text = str(store.get('Towindow')["value"])
        self.ids.Idiameter.text = str(store.get('Idiameter')["value"])
        self.ids.Pressure.text = str(store.get('Pressure')["value"])
        self.ids.Time.text = str(store.get('Time')["value"])
        self.ids.Viscosity.text = str(store.get('Viscosity')["value"])
        self.ids.Concentration.text = str(store.get('Concentration')["value"])
        self.ids.Molweight.text = str(store.get('Molweight')["value"])
    
    
    def show_injection_results(self):
        """ lauch when clicked on result
        the new Capillary value is save (it's just an exemple)"""
        store = get_store()
        #save but delete why ?
        store.put('Capillary', value=float(self.ids.Capillary.text),
                  unit="Unit1")
        data = {}
        data['injection'] = self.ids.Capillary.text
        data['volume'] = self.ids.Towindow.text
        injection_popup = InjectionPopup()
        injection_popup.show_popup(data)
    
        

class ViscosityScreen(Screen):
    def show_viscosity_results(self):
        self._popup = ViscosityPopup()
        self._popup.open()

class ConductivityScreen(Screen):
    def show_conductivity_results(self):
        self._popup = ConductivityPopup()
        self._popup.open()

class FlowScreen(Screen):
    def show_flow_results(self):
        self._popup = FlowPopup()
        self._popup.open()

class AboutScreen(Screen):
    pass


class TopScreenLayout(GridLayout):
    """ set the size of the layout from minimals values and the size
    of the scrollviewspe parrent."""
    
    def change_height(self, height_par):
        #~ reset because of a bug in kivy
        #~ need to depend of the number of row 
        self.minimum_height = 350
        
        if height_par > self.minimum_height:
            self.height = height_par
        else:
            self.height = self.minimum_height
            
    def change_width(self, wid):
        #~ reset because of a bug in kivy
        self.minimum_width = 350
        
        if wid > self.minimum_width:
            self.width = wid
        else:
            self.width = self.minimum_width

class DownMenuLayout(GridLayout):
    """ set the size of the layout from minimals values and the size
    of the scrollviewspe parrent."""

    def change_height(self, height_par):
        #~ reset because of a bug in kivy 
        self.minimum_height = 30
        
        if height_par > self.minimum_height:
            self.height = height_par
        else:
            self.height = self.minimum_height
            
    def change_width(self, wid):
        #~ reset because of a bug in kivy
        self.minimum_width = 350
        
        if wid > self.minimum_width:
            self.width = wid
        else:
            self.width = self.minimum_width

class DownMenuClose(DownMenuLayout):
    
    def change_width(self, wid):
        #~ reset because of a bug in kivy
        self.minimum_width = 100
        
        if wid > self.minimum_width:
            self.width = wid
        else:
            self.width = self.minimum_width
    
    
            
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
