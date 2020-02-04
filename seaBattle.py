#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from tkinter import *

from globalVars import *
from battleField import *
from startBoard import *
from battleBoard import *

#main loop
#begin from creating gamer field
root = Tk()
app = StartBoard(master=root)
app.mainloop()

