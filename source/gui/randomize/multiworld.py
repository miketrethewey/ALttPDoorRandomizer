from tkinter import StringVar, N, E, W, X, LEFT
import source.gui.widgets as widgets
import json
import os
from source.classes.Empty import Empty

def multiworld_page(parent,settings):
    # Multiworld
    self = widgets.make_frame(parent)

    # Multiworld options
    self.widgets = {}

    # Multiworld option sections
    self.frames = {}
    self.frames["widgets"] = widgets.make_frame(self)
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
    label = "Player names"

    # Empty object
    self.widgets[widget] = Empty()
    # pieces
    self.widgets[widget].pieces = {}

    # frame
    self.widgets[widget].pieces["frame"] = widgets.make_frame(self.frames["widgets"])
    # storage var
    self.widgets[widget].storageVar = StringVar(value=settings["names"])

    # FIXME: Got some strange behavior here; both Entry-like objects react to mousewheel on Spinbox
    def saveMultiNames(caller,_,mode):
        settings["names"] = self.widgets["names"].storageVar.get()
    self.widgets[widget].storageVar.trace_add("write",saveMultiNames)
    # textbox
    self.widgets[widget].type = "textbox"
    self.widgets[widget].pieces["widget"] = widgets.make_widget(
      self,
      self.widgets[widget].type,
      self,
      label,
      self.widgets[widget].storageVar,
      "pack",
      {
        "label": {"side": LEFT, "anchor": N},
        "textbox": {"side": LEFT, "anchor": N, "fill": X, "expand": True},
        "entry": {"justify": LEFT}
      }
    )

    # frame: pack
    self.widgets[widget].pieces["frame"].pack()

    return self,settings
