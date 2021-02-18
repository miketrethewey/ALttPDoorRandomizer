from tkinter import filedialog, StringVar, Label, N, E, W, LEFT, RIGHT, BOTTOM, X
import source.gui.widgets as widgets
import json
import os
import webbrowser
from source.classes.Empty import Empty

def enemizer_page(parent,settings):
    def open_enemizer_download(_evt):
        webbrowser.open("https://github.com/Bonta0/Enemizer/releases")

    # Enemizer
    self = widgets.make_frame(parent)

    # Enemizer options
    self.widgets = {}

    # Enemizer option sections
    self.frames = {}

    # Enemizer option frames
    self.frames["checkboxes"] = widgets.make_frame(self)
    self.frames["checkboxes"].pack(anchor=W)

    self.frames["selectOptionsFrame"] = widgets.make_frame(self)
    self.frames["leftEnemizerFrame"] = widgets.make_frame(self.frames["selectOptionsFrame"])
    self.frames["rightEnemizerFrame"] = widgets.make_frame(self.frames["selectOptionsFrame"])
    self.frames["bottomEnemizerFrame"] = widgets.make_frame(self)
    self.frames["selectOptionsFrame"].pack(fill=X)
    self.frames["leftEnemizerFrame"].pack(side=LEFT)
    self.frames["rightEnemizerFrame"].pack(side=RIGHT)
    self.frames["bottomEnemizerFrame"].pack(fill=X)

    # Load Enemizer option widgets as defined by JSON file
    # Defns include frame name, widget type, widget options, widget placement attributes
    # These get split left & right
    with open(os.path.join("resources","app","gui","randomize","enemizer","widgets.json")) as widgetDefns:
        myDict = json.load(widgetDefns)
        for framename,theseWidgets in myDict.items():
            dictWidgets = widgets.make_widgets_from_dict(self, theseWidgets, self.frames[framename])
            for key in dictWidgets:
                self.widgets[key] = dictWidgets[key]
                packAttrs = {"anchor":E}
                if self.widgets[key].type == "checkbox":
                    packAttrs["anchor"] = W
                self.widgets[key].pack(packAttrs)

    ## Enemizer CLI Path
    # This one's more-complicated, build it and stuff it
    # widget ID
    widget = "enemizercli"
    label = "EnemizerCLI path:"

    # Empty object
    self.widgets[widget] = Empty()
    # pieces
    self.widgets[widget].pieces = {}

    # frame
    self.widgets[widget].pieces["frame"] = widgets.make_frame(self.frames["bottomEnemizerFrame"])

    # storage var
    self.widgets[widget].storageVar = StringVar(value=settings["enemizercli"])
    # textbox
    self.widgets[widget].type = "textbox"
    self.widgets[widget].pieces["widget"] = widgets.make_widget(
      self,
      self.widgets[widget].type,
      self.widgets[widget].pieces["frame"], label,
      self.widgets[widget].storageVar,
      "pack",
      {
        "label": {"side": LEFT, "anchor": N},
        "textbox": {"side": LEFT, "anchor": N, "fill": X, "expand": True},
        "entry": {"justify": LEFT}
      }
    )

    def EnemizerSelectPath():
        path = filedialog.askopenfilename(filetypes=[("EnemizerCLI executable", "*EnemizerCLI*")], initialdir=os.path.join("."))
        if path:
            self.widgets[widget].storageVar.set(path)
            settings["enemizercli"] = path
    # dialog button
    self.widgets[widget].pieces["opendialog"] = widgets.make_button(self.widgets[widget].pieces["frame"], label='...', command=EnemizerSelectPath)
    self.widgets[widget].pieces["opendialog"].pack(side=LEFT)

    # get app online
    self.widgets[widget].pieces["online"] = Empty()
    # get app online: label
    self.widgets[widget].pieces["online"].label = Label(self.widgets[widget].pieces["frame"], text="(get online)", fg="blue", cursor="hand2")
    # get app online: open browser
    self.widgets[widget].pieces["online"].label.bind("<Button-1>", open_enemizer_download)
    # get app online: pack
    self.widgets[widget].pieces["online"].label.pack(side=LEFT)

    # frame: pack
    self.widgets[widget].pieces["frame"].pack(fill=X)

    return self,settings
