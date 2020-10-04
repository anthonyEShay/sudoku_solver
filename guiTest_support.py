#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 5.2
#  in conjunction with Tcl version 8.6
#    May 29, 2020 01:32:09 PM PDT  platform: Windows NT

import sys
import Main
import time

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def set_Tk_var():
    global SudSize
    SudSize = tk.IntVar()
    global SudType
    SudType = tk.StringVar()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def fillBlank(Text1):
    #Get current IntVar or set to 3 if none exist
    #Create a nxn array of -'s and print it to Text1
    print('guiTest_support.fillBlank')
    sys.stdout.flush()

def runSudoku(Text1, maxCount):
    #print('guiTest_support.runSudoku')
    boxInput = Text1.get("1.0", 'end-1c')
    #print("Input:\n", boxInput, sep = "")
    boxInput = boxInput.strip()
    boxInput = boxInput.replace("\n", " ")
    nArray = boxInput.split(" ")
    #print(len(nArray))
    #print("array:", nArray)
    startTime = time.process_time()
    returnValue = Main.main(SudSize.get(), SudType.get(), nArray, maxCount)
    endTime = time.process_time()
    returnValue += "\n\nTime:  " + str(endTime - startTime) + "s"
    Text1.delete("1.0", tk.END)
    Text1.insert(tk.END, returnValue)
    sys.stdout.flush()

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import guiTest
    guiTest.vp_start_gui()




