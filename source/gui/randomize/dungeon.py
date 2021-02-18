from tkinter import E, W, LEFT, RIGHT
import source.gui.widgets as widgets
import json
import os

def dungeon_page(parent):
    # Dungeon Shuffle
    self = widgets.make_frame(parent)

    # Dungeon Shuffle options
    self.widgets = {}

    # Dungeon Shuffle option sections
    self.frames = {}
    self.frames["keysanity"] = widgets.make_frame(self)
    self.frames["keysanity"].pack(anchor=W)

    ## Dungeon Item Shuffle
    mscbLabel = widgets.make_label(self.frames["keysanity"], label="Shuffle: ")
    mscbLabel.pack(side=LEFT)

    # Load Dungeon Shuffle option widgets as defined by JSON file
    # Defns include frame name, widget type, widget options, widget placement attributes
    # This first set goes in the Keysanity frame
    with open(os.path.join("resources","app","gui","randomize","dungeon","keysanity.json")) as keysanityItems:
        myDict = json.load(keysanityItems)
        myDict = myDict["keysanity"]
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["keysanity"])
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(side=LEFT)

    # These get split left & right
    self.frames["widgets"] = widgets.make_frame(self)
    self.frames["widgets"].pack(anchor=W)
    with open(os.path.join("resources","app","gui","randomize","dungeon","widgets.json")) as dungeonWidgets:
        myDict = json.load(dungeonWidgets)
        myDict = myDict["widgets"]
        dictWidgets = widgets.make_widgets_from_dict(self, myDict, self.frames["widgets"])
        for key in dictWidgets:
            self.widgets[key] = dictWidgets[key]
            self.widgets[key].pack(anchor=W)

    return self
