from tkinter import E, W, LEFT, RIGHT
import source.gui.widgets as widgets
import json
import os

def entrando_page(parent):
    # Entrance Randomizer
    self = widgets.make_frame(parent)

    # Entrance Randomizer options
    self.widgets = {}

    # Entrance Randomizer option sections
    self.frames = {}
    self.frames["widgets"] = widgets.make_frame(self)
    self.frames["widgets"].pack(anchor=W)

    # Load Entrance Randomizer option widgets as defined by JSON file
    # Defns include frame name, widget type, widget options, widget placement attributes
    # Checkboxes go West
    # Everything else goes East
    # They also get split left & right
    with open(os.path.join("resources","app","gui","randomize","entrando","widgets.json")) as widgetDefns:
        myDict = json.load(widgetDefns)
        for framename,theseWidgets in myDict.items():
            dictWidgets = widgets.make_widgets_from_dict(self, theseWidgets, self.frames[framename])
            for key in dictWidgets:
                self.widgets[key] = dictWidgets[key]
                packAttrs = {"anchor":E}
                if self.widgets[key].type == "checkbox":
                    packAttrs["anchor"] = W
                self.widgets[key].pack(packAttrs)

    return self
