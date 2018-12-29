#!/usr/bin/env python3
#
# Author: Soft9000.com
# 2018/11/24: Project Begun

# Mission: Create a graphical user interface to PyDAO.
# Status: WORK IN PROGRESS

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from collections import OrderedDict

from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.CodeGen01.SqlSyntax import SqliteCrud
from SqltDAO.SchemaDef.Order import OrderDef
from SqltDAO.CodeGen01.CodeGen import DaoGen

from SqltDAO.Gui.Data2Code import Data2Code
from SqltDAO.Gui.StandardEntry import LabelEntry
from SqltDAO.Gui.TableDef import TableDef as TableDef2
from SqltDAO.SchemaDef.Table import TableDef as TableDef1


class Main(Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bSaved = False
        self.ztitle = "PyDAO 0.1"
        self.d2c = None
        self.project = None
        self.zoptions = (
            ("Projects",    [("Open Project...", self._on_open),
                             ("Save Project...", self._on_save),
                             ("Create Code", self._on_create)],),
            ("Tools",       [("Data2Code...", self._on_d2c),
                             ("Data2Project...", self._on_d2p)]),
            ("About",       [("About PyDao...", self._on_about),
                             ("Quit", self.destroy)]),
            )
        self.order_info = OrderedDict()

        '''
        activeBackground, foreground, selectColor,
        activeForeground, highlightBackground, selectBackground,
        background, highlightColor, selectForeground,
        disabledForeground, insertBackground, troughColor.
        '''
        self.tk_setPalette(
                background="Light Green",# e.g. Global
                foreground="dark blue",  # e.g. Font color
                insertBackground="blue", # e.g. Entry cursor
                selectBackground="gold", # e.g. Editbox selections
                activeBackground="gold", # e.g. Menu selections
                )
        self.table_frame = None
    
    def _on_open(self):
        self.project = askopenfilename()
        if not self.project:
            return
        zdef = OrderDef.LoadFile(self.project)
        if not zdef:
            messagebox.showerror(
                "Schema File / Format Error",
                "Unable to import " + self.project)
        else:
            self.title(self.project)
            self.order_info = zdef
            self._show_order()

    def _on_save(self):
        if not self.order_info:
            messagebox.showerror(
                "No Data",
                "Schema Definition Required.")
        self._on_about()

    def _on_create(self):
        self._on_about()

    def _on_d2c(self):
        Data2Code(self, verbose=True)

    def _on_d2p(self):
        Data2Code(self, gendef=True, verbose=True)

    def _on_about(self):
        messagebox.showinfo(
            self.ztitle,
            "Work In Progress - Not For Use")

    def _show_order(self):
        if not self.order_info:
            return False
        for key in self.order_info.zdict_tables:
            td1 = self.order_info.zdict_tables[key]
            if self.table_frame.put_results(td1) is False:
                return False
            return True

    def _set_frame(self):
        zframe = Frame(self)
        self.table_frame = TableDef2(zframe)
        zframe.pack(fill=BOTH)

    def begin(self):
        self.title(self.ztitle)
        try:
            image = PhotoImage(file="zicon.png")
            self.wm_iconphoto(self, image)
        except:
            pass
        zmain = Menu(self)
        for zsub in self.zoptions:
            zdrop = Menu(zmain, tearoff=False)
            zmain.add_cascade(label=zsub[0], menu=zdrop)
            for zz in zsub[1]:
                zdrop.add_command(label=zz[0], command=zz[1])
        self.config(menu=zmain)
        self._set_frame()
        return True

    def run(self):
        self.mainloop()
        return True

    def end(self):
        return True


if __name__ == "__main__":
    main = Main()
    try:
        if main.begin():
            main.run()
    except Exception as ex:
        print(str(ex))
    finally:
        try:
            main.end()
        except:
            pass

