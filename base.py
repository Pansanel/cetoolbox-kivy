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
base.py
=========

Contain all usefull function and method related to kivy if
they are not Screen, Popup or App.
It's link to the base.kv file

"""
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
from kivy.metrics import sp
from kivy.lang import Builder
Builder.load_file('base.kv')

def add_color(text, color):
    return "[color="+color+"]"+text+"[/color]" 

class CEToolBoxButton(Button):
    pass
  
class CEToolBoxLabel(Label):
    pass

class CEToolBoxTextInput(TextInput):
    pass

class CEToolBoxSpinner(Spinner):
    pass

    
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


class CEToolBoxLayout(GridLayout):
    """Special Layout use to choose the minimal size allowed
    if the actual size of the parent widget is lower.
    If the actual size of the parent is biger then get the biger size.
    /!\ The parent must be a ScrollViewSpe
    """
    
    def set_min_height(self):
        self.minimum_height = sp(350)
    
    def set_min_width(self):
        self.minimum_width = sp(350)
    
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
        self.minimum_height = sp(40) * self.rows + sp(20)
        
    def set_min_width(self):
        self.minimum_width = sp(290)

class TopPopupLayout(CEToolBoxLayout):
    """ set the size of the layout from minimals values and the size
    of the scrollviewspe parrent."""
    def set_min_height(self):
        self.minimum_height = sp(40) * self.rows + sp(20)

    def set_min_width(self):
        self.minimum_width = sp(290)
    
            



