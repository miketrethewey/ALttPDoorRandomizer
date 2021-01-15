from tkinter import ttk, StringVar, Entry, Frame, Label, N, E, W, X, LEFT
import source.gui.widgets as widgets
import json
import os
from source.classes.Empty import Empty

global bgcolor
global fgcolor
bgcolor = "black"
fgcolor = "white"

def multiworld_page(parent,settings):
    # Multiworld
    self = ttk.Frame(parent)

    # Multiworld options
    self.widgets = {}

    # Multiworld option sections
    self.frames = {}
    self.frames["widgets"] = ttk.Frame(self)
    self.frames["widgets"].pack(anchor=W, fill=X)

    # Load Multiworld option widgets as defined by JSON file
    # Defns include frame name, widget type, widget options, widget placement attributes
    with open(os.path.join("resources","app","gui","randomize","multiworld","widgets.json")) as multiworldItems:
        myDict = json.load(multiworldItems)
        myDict = myDict["widgets"]
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["widgets"])
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(side=LEFT, anchor=N)

    ## List of Player Names
    # This one's more-complicated, build it and stuff it
    # widget ID
    widget = "names"

    # Empty object
    self.widgets[widget] = Empty()
    # pieces
    self.widgets[widget].pieces = {}

    # frame
    self.widgets[widget].pieces["frame"] = ttk.Frame(self.frames["widgets"])
    # frame: label
    self.widgets[widget].pieces["frame"].label = widgets.make_label(self.widgets[widget].pieces["frame"], text='Player names')
    # storage var
    self.widgets[widget].storageVar = StringVar(value=settings["names"])

    # FIXME: Got some strange behavior here; both Entry-like objects react to mousewheel on Spinbox
    def saveMultiNames(caller,_,mode):
        settings["names"] = self.widgets["names"].storageVar.get()
    self.widgets[widget].storageVar.trace_add("write",saveMultiNames)
    # textbox
    self.widgets[widget].pieces["textbox"] = widgets.make_textbox(self.widgets[widget].pieces["frame"], None, self.widgets[widget].storageVar)
    # self.widgets[widget].pieces["textbox"].configure(background=bgcolor, foreground=fgcolor, insertbackground=fgcolor)

    # frame label: pack
    self.widgets[widget].pieces["frame"].label.pack(side=LEFT, anchor=N)
    # textbox: pack
    # self.widgets[widget].pieces["textbox"].pack(side=LEFT, anchor=N, fill=X, expand=True)
    # frame: pack
    self.widgets[widget].pieces["frame"].pack(side=LEFT, anchor=N, fill=X, expand=True)

    return self,settings
