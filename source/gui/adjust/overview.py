from tkinter import filedialog, StringVar, E, W, LEFT, RIGHT, X, BOTTOM, N
from AdjusterMain import adjust
from argparse import Namespace
from source.classes.SpriteSelector import SpriteSelector
import source.gui.widgets as widgets
import json
import logging
import os

def adjust_page(top, parent, settings):
    # Adjust page
    self = widgets.make_frame(parent)

    # Adjust options
    self.widgets = {}

    # Adjust option sections
    self.frames = {}
    self.frames["checkboxes"] = widgets.make_frame(self)
    self.frames["checkboxes"].pack(anchor=W)

    # Adjust option frames
    self.frames["selectOptionsFrame"] = widgets.make_frame(self)
    self.frames["leftAdjustFrame"] = widgets.make_frame(self.frames["selectOptionsFrame"])
    self.frames["rightAdjustFrame"] = widgets.make_frame(self.frames["selectOptionsFrame"])
    self.frames["bottomAdjustFrame"] = widgets.make_frame(self)
    self.frames["selectOptionsFrame"].pack(fill=X)
    self.frames["leftAdjustFrame"].pack(side=LEFT)
    self.frames["rightAdjustFrame"].pack(side=RIGHT)
    self.frames["bottomAdjustFrame"].pack(fill=X)

    # Load Adjust option widgets as defined by JSON file
    # Defns include frame name, widget type, widget options, widget placement attributes
    with open(os.path.join("resources","app","gui","adjust","overview","widgets.json")) as widgetDefns:
        myDict = json.load(widgetDefns)
        for framename,theseWidgets in myDict.items():
            dictWidgets = widgets.make_widgets_from_dict(self, theseWidgets, self.frames[framename])
            for key in dictWidgets:
                self.widgets[key] = dictWidgets[key]
                packAttrs = {"anchor":E}
                if self.widgets[key].type == "checkbox":
                    packAttrs["anchor"] = W
                self.widgets[key].pack(packAttrs)

    # Sprite Selection
    # This one's more-complicated, build it and stuff it
    self.spriteNameVar2 = StringVar()
    spriteDialogFrame2 = widgets.make_frame(self.frames["leftAdjustFrame"])
    baseSpriteLabel2 = widgets.make_label(spriteDialogFrame2, label='Sprite:')
    spriteEntry2 = widgets.make_textbox(self, spriteDialogFrame2, self.spriteNameVar2, "Sprite:", None, {})
    # spriteEntry2 = widgets.make_widget(self, "textbox", spriteDialogFrame2, self.spriteNameVar2, "Sprite:", None, {})
    self.sprite = None

    def set_sprite(sprite_param, random_sprite=False):
        if sprite_param is None or not sprite_param.valid:
            self.sprite = None
            self.spriteNameVar2.set('(unchanged)')
        else:
            self.sprite = sprite_param
            self.spriteNameVar2.set(self.sprite.name)
        top.randomSprite.set(random_sprite)

    def SpriteSelectAdjuster():
        SpriteSelector(parent, set_sprite, adjuster=True)

    spriteSelectButton2 = widgets.make_button(spriteDialogFrame2, label='...', command=SpriteSelectAdjuster)

    baseSpriteLabel2.pack(side=LEFT)
    # spriteEntry2.pack(side=LEFT)
    spriteSelectButton2.pack(side=LEFT)
    spriteDialogFrame2.pack(anchor=E)

    # Path to game file to Adjust
    # This one's more-complicated, build it and stuff it
    label = "Rom to adjust:"
    adjustRomFrame = widgets.make_frame(self.frames["bottomAdjustFrame"])
    self.romVar2 = StringVar(value=settings["rom"])
    romEntry2 = widgets.make_widget(
      self,
      "textbox",
      adjustRomFrame,
      label,
      self.romVar2,
      "pack",
      {
        "label": {"side": LEFT, "anchor": N},
        "textbox": {"side": LEFT, "anchor": N, "fill": X, "expand": True},
        "entry": {"justify": LEFT}
      }
    )

    def RomSelect2():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".sfc", ".smc")), ("All Files", "*")])
        if rom:
            settings["rom"] = rom
            self.romVar2.set(rom)
    romSelectButton2 = widgets.make_button(adjustRomFrame, label='Select Rom', command=RomSelect2)

    # romEntry2.pack(side=LEFT, fill=X, expand=True)
    romSelectButton2.pack(side=LEFT)
    adjustRomFrame.pack(fill=X)

    # These are the options to Adjust
    def adjustRom():
        options = {
          "heartbeep": "heartbeep",
          "heartcolor": "heartcolor",
          "menuspeed": "fastmenu",
          "owpalettes": "ow_palettes",
          "uwpalettes": "uw_palettes",
          "quickswap": "quickswap",
          "nobgm": "disablemusic"
        }
        guiargs = Namespace()
        for option in options:
            arg = options[option]
            setattr(guiargs, arg, self.widgets[option].storageVar.get())
        guiargs.rom = self.romVar2.get()
        guiargs.baserom = top.pages["randomizer"].pages["generation"].widgets["rom"].storageVar.get()
        guiargs.sprite = self.sprite
        try:
            adjust(args=guiargs)
        except Exception as e:
            logging.exception(e)
            widgets.make_messagebox.showerror(type="error", title="Error while creating seed", body=str(e))
        else:
            widgets.make_messagebox(type="info", title="Success", body="Rom patched successfully")

    adjustButton = widgets.make_button(self.frames["bottomAdjustFrame"], label='Adjust Rom', command=adjustRom)
    adjustButton.pack(side=BOTTOM, padx=(5, 0))

    return self,settings
