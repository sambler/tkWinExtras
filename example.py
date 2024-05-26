#!/usr/bin/env python

import screeninfo
import tkinter as tk
from tkwinextras import tkExtras


class Testwin(tk.Tk, tkExtras):
    def __init__(self):
        super().__init__()
        self.title('Tester Window')
        self.bind('<Control-q>', lambda e: self.destroy())
        self.bind('<Escape>', lambda e: self.destroy())
        self.bind('<F1>', self.show_monitors)
        self.bind('<F4>', self.move_centre)
        self.bind('<F5>', self.toggle_fullscreen)
        self.bind('<F8>', self.switch_monitor)
        self.restore_geom = self.win_geom_int()

    def show_monitors(self, evnt=None):
        mon_list = screeninfo.get_monitors()
        for m in sorted(mon_list, key=lambda x: x.x):
            print(m)


w = Testwin()
w.mainloop()
