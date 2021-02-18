from tkinter import ttk, N, E, W, LEFT, X, VERTICAL, Y
import source.gui.widgets as widgets
import json
import os

import source.classes.constants as CONST

def custom_page(top,parent):
    # Custom Item Pool
    self = widgets.make_frame(parent)

    # Create uniform list columns
    def create_list_frame(parent, framename):
        parent.frames[framename] = widgets.make_frame(parent)
        parent.frames[framename].pack(side=LEFT, padx=(0,0), anchor=N)
        parent.frames[framename].thisRow = 0
        parent.frames[framename].thisCol = 0

    # Create a vertical rule to help with splitting columns visually
    def create_vertical_rule(num=1):
        for _ in range(0,num):
            ttk.Separator(self, orient=VERTICAL).pack(side=LEFT, anchor=N, fill=Y)

    # This was in here, I have no idea what it was but I left it just in case: MikeT
    def validation(P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
    vcmd=(self.register(validation), '%P')

    # Custom Item Pool options
    self.customWidgets = {}

    # Custom Item Pool option sections
    self.frames = {}
    # Create 5 columns with 2 vertical rules in between each
    create_list_frame(self, "itemList1")
    create_vertical_rule(2)
    create_list_frame(self, "itemList2")
    create_vertical_rule(2)
    create_list_frame(self, "itemList3")
    create_vertical_rule(2)
    create_list_frame(self, "itemList4")
    create_vertical_rule(2)
    create_list_frame(self, "itemList5")

    # Load Custom option widgets as defined by JSON file
    # Defns include frame name, widget type, widget options, widget placement attributes
    with open(os.path.join("resources", "app", "gui", "custom", "overview", "widgets.json")) as widgetDefns:
        myDict = json.load(widgetDefns)
        for framename,theseWidgets in myDict.items():
            dictWidgets = widgets.make_widgets_from_dict(self, theseWidgets, self.frames[framename])
            for key in dictWidgets:
                self.customWidgets[key] = dictWidgets[key]

    # Load Custom Item Pool settings from settings file
    for key in CONST.CUSTOMITEMS:
        self.customWidgets[key].storageVar.set(top.settings["customitemarray"][key])

    return self
