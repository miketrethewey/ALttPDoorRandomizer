from tkinter import IntVar, StringVar, LEFT, RIGHT, X, YES
from tkinter import ttk
from source.classes.Empty import Empty

global bgcolor
global fgcolor
bgcolor = "black"
fgcolor = "white"

# Override Spinbox to include mousewheel support for changing value
class mySpinbox(ttk.Spinbox):
    def __init__(self, *args, **kwargs):
        ttk.Spinbox.__init__(self, *args, **kwargs)
        self.bind('<MouseWheel>', self.mouseWheel)
        self.bind('<Button-4>', self.mouseWheel)
        self.bind('<Button-5>', self.mouseWheel)

    def mouseWheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.invoke('buttondown')
        elif event.num == 4 or event.delta == 120:
            self.invoke('buttonup')

def make_button(parent, text=None, image=None, command=None):
    global bgcolor
    global fgcolor

    self = ttk.Frame(parent)
    self.button = ttk.Button(self, command=command)
    if text is not None:
        self.button.configure(text=text)
    if image is not None:
        self.button.configure(image=image)
    self.button.pack()

    return self

# Make a Checkbutton with a label
def make_checkbox(self, parent, label, storageVar, manager, managerAttrs):
    global bgcolor
    global fgcolor

    self = ttk.Frame(parent)
    self.storageVar = storageVar
    if managerAttrs is not None and "default" in managerAttrs:
        if managerAttrs["default"] == "true" or managerAttrs["default"] == True:
            self.storageVar.set(True)
        elif managerAttrs["default"] == "false" or managerAttrs["default"] == False:
            self.storageVar.set(False)
        del managerAttrs["default"]
    self.checkbox = ttk.Checkbutton(self, text=label, variable=self.storageVar)
    # self.checkbox.configure(background=bgcolor, foreground=fgcolor)
    # self.checkbox.configure(activebackground=bgcolor, activeforeground=fgcolor)
    # self.checkbox.configure(highlightbackground=bgcolor, highlightcolor=fgcolor)
    # self.checkbox.configure(selectcolor=bgcolor)
    if managerAttrs is not None:
        self.checkbox.pack(managerAttrs)
    else:
        self.checkbox.pack()
    return self

# Make an OptionMenu with a label and pretty option labels
def make_selectbox(self, parent, label, options, storageVar, manager, managerAttrs, config=None):
    global bgcolor
    global fgcolor

    self = ttk.Frame(parent)

    labels = options

    if isinstance(options,dict):
        labels = options.keys()

    self.labelVar = StringVar()
    self.storageVar = storageVar
    self.selectbox = ttk.OptionMenu(self, self.labelVar, *labels)
    self.selectbox.configure(width=config['width'] if config and config['width'] else 20) # width
    # self.selectbox.configure(background=bgcolor, foreground=fgcolor)                      # dormant colors
    # self.selectbox.configure(activebackground=bgcolor, activeforeground=fgcolor)          # hover colors
    self.selectbox["menu"].configure( # optionlist colors
        background=bgcolor,
        foreground=fgcolor
    )
    self.selectbox.options = {}

    if isinstance(options,dict):
        self.selectbox.options["labels"] = list(options.keys())
        self.selectbox.options["values"] = list(options.values())
    else:
        self.selectbox.options["labels"] = ["" for i in range(0,len(options))]
        self.selectbox.options["values"] = options

    def change_thing(thing, *args):
        labels = self.selectbox.options["labels"]
        values = self.selectbox.options["values"]
        check = ""
        lbl = ""
        val = ""
        idx = 0

        if thing == "storage":
            check = self.labelVar.get()
        elif thing == "label":
            check = self.storageVar.get()

        if check in labels:
            idx = labels.index(check)
        if check in values:
            idx = values.index(check)

        lbl = labels[idx]
        val = values[idx]

        if thing == "storage":
            self.storageVar.set(val)
        elif thing == "label":
            self.labelVar.set(lbl)
        self.selectbox["menu"].entryconfigure(idx, label=lbl)
        self.selectbox.configure(state="active")


    def change_storage(*args):
        change_thing("storage", *args)
    def change_selected(*args):
        change_thing("label", *args)

    self.storageVar.trace_add("write",change_selected)
    self.labelVar.trace_add("write",change_storage)
    self.label = make_label(self, text=label)

    if managerAttrs is not None and "label" in managerAttrs:
        self.label.pack(managerAttrs["label"])
    else:
        self.label.pack(side=LEFT)

    idx = 0
    default = self.selectbox.options["values"][idx]
    if managerAttrs is not None and "default" in managerAttrs:
        default = managerAttrs["default"]
    labels = self.selectbox.options["labels"]
    values = self.selectbox.options["values"]
    if default in values:
        idx = values.index(default)
    if not labels[idx] == "":
        self.labelVar.set(labels[idx])
        self.selectbox["menu"].entryconfigure(idx,label=labels[idx])
    self.storageVar.set(values[idx])

    if managerAttrs is not None and "selectbox" in managerAttrs:
        self.selectbox.pack(managerAttrs["selectbox"])
    else:
        self.selectbox.pack(side=RIGHT)
    return self

# Make a Spinbox with a label, limit 1-100
def make_spinbox(self, parent, label, storageVar, manager, managerAttrs):
    global bgcolor
    global fgcolor

    self = ttk.Frame(parent)
    self.storageVar = storageVar
    self.label = make_label(self, text=label)
    if managerAttrs is not None and "label" in managerAttrs:
        self.label.pack(managerAttrs["label"])
    else:
        self.label.pack(side=LEFT)
    fromNum = 1
    toNum = 100
    if managerAttrs is not None and "spinbox" in managerAttrs:
        if "from" in managerAttrs:
            fromNum = managerAttrs["spinbox"]["from"]
        if "to" in managerAttrs:
            toNum = managerAttrs["spinbox"]["to"]
    self.spinbox = mySpinbox(self, from_=fromNum, to=toNum, width=5, textvariable=self.storageVar)
    # self.spinbox.configure(background=bgcolor, foreground=fgcolor)
    # self.spinbox.configure(selectbackground=bgcolor, selectforeground=fgcolor)
    # self.spinbox.configure(insertbackground=fgcolor)
    if managerAttrs is not None and "spinbox" in managerAttrs:
        self.spinbox.pack(managerAttrs["spinbox"])
    else:
        self.spinbox.pack(side=RIGHT)
    return self

# Make an Entry box with a label
# Support for Grid or Pack so that the Custom Item Pool & Starting Inventory pages don't look ugly
def make_labelledtextbox(self, parent, label, storageVar, manager, managerAttrs):
    global bgcolor
    global fgcolor

    widget = Empty()
    widget.frame = ttk.Frame(parent)
    widget.label = make_label(widget.frame, text=label)
    textbox = make_textbox(self, widget.frame, None, storageVar, None, managerAttrs)
    widget.storageVar = textbox.storageVar
    widget.textbox = textbox

    # grid
    if manager == "grid":
        widget.label.grid(managerAttrs["label"] if managerAttrs is not None and "label" in managerAttrs else None, row=parent.thisRow, column=parent.thisCol)
        if managerAttrs is not None and "label" not in managerAttrs:
            widget.label.grid_configure(sticky="w")
        parent.thisCol += 1
        widget.textbox.grid(managerAttrs["textbox"] if managerAttrs is not None and "textbox" in managerAttrs else None, row=parent.thisRow, column=parent.thisCol)
        if managerAttrs is not None and "textbox" not in managerAttrs:
            widget.textbox.grid_configure(sticky="w")
        parent.thisRow += 1
        parent.thisCol = 0

    # pack
    elif manager == "pack":
        widget.label.pack(managerAttrs["label"] if managerAttrs is not None and "label" in managerAttrs else None)
        widget.textbox.pack(managerAttrs["textbox"] if managerAttrs is not None and "textbox" in managerAttrs else None)
    return widget

# Make an Entry box
def make_textbox(self, parent=None, junk=None, storageVar=None, junk2=None, managerAttrs=None):
    textbox = ttk.Entry(parent, justify=RIGHT, textvariable=storageVar, width=3, style="EntryStyle.TEntry")
    textbox.storageVar = storageVar
    if managerAttrs is not None and "default" in managerAttrs:
        textbox.storageVar.set(managerAttrs["default"])
    return textbox

# Make a Label
def make_label(self, text=None, textvariable=None, fg=None, bg=None, cursor=None):
    global bgcolor
    global fgcolor

    if bg is None:
        bg = bgcolor
    if fg is None:
        fg = fgcolor
    elif fg == "blue" and bg == "black":
        fg = "#AAAAFF"
    if cursor is None:
        cursor = "arrow"

    lbl = ttk.Label(self, text=text, background=bg, foreground=fg, cursor=cursor)
    if textvariable is not None:
        lbl.configure(textvariable=textvariable)

    return lbl

# Make a generic widget
def make_widget(self, type, parent, label, storageVar=None, manager=None, managerAttrs=dict(),
                options=None, config=None):
    widget = None
    if manager is None:
        manager = "pack"
    thisStorageVar = storageVar
    if isinstance(storageVar,str):
        if storageVar == "int" or storageVar == "integer":
            thisStorageVar = IntVar()
        elif storageVar == "str" or storageVar == "string":
            thisStorageVar = StringVar()

    if type == "checkbox":
        if thisStorageVar is None:
            thisStorageVar = IntVar()
        widget = make_checkbox(self, parent, label, thisStorageVar, manager, managerAttrs)
    elif type == "selectbox":
        if thisStorageVar is None:
            thisStorageVar = StringVar()
        widget = make_selectbox(self, parent, label, options, thisStorageVar, manager, managerAttrs, config)
    elif type == "spinbox":
        if thisStorageVar is None:
            thisStorageVar = StringVar()
        widget = make_spinbox(self, parent, label, thisStorageVar, manager, managerAttrs)
    elif type == "textbox":
        if thisStorageVar is None:
            thisStorageVar = StringVar()
        if label != "":
            widget = make_labelledtextbox(self, parent, label, thisStorageVar, manager, managerAttrs)
        else:
            widget = make_textbox(self, parent, None, thisStorageVar, manager, managerAttrs)
    widget.type = type
    return widget

# Make a generic widget from a dict
def make_widget_from_dict(self, defn, parent):
    type = defn["type"] if "type" in defn else None
    label = defn["label"]["text"] if "label" in defn and "text" in defn["label"] else ""
    manager = defn["manager"] if "manager" in defn else None
    managerAttrs = defn["managerAttrs"] if "managerAttrs" in defn else None
    options = defn["options"] if "options" in defn else None
    config = defn["config"] if "config" in defn else None

    if managerAttrs is None and "default" in defn:
        managerAttrs = {}
    if "default" in defn:
        managerAttrs["default"] = defn["default"]

    widget = make_widget(self, type, parent, label, None, manager, managerAttrs, options, config)
    widget.type = type
    return widget

# Make a set of generic widgets from a dict
def make_widgets_from_dict(self, defns, parent):
    widgets = {}
    for key,defn in defns.items():
        widgets[key] = make_widget_from_dict(self, defn, parent)
    return widgets
