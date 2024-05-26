#!/usr/bin/env python3
#
#  Copyright (c)2024 Shane Ambler <Develop@ShaneWare.biz>
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the  nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


import screeninfo

from . import __version__ as vers

class tkExtras:
    def move_centre(self, evnt=None):
        w, h = list(map(int, self.geometry().split('+')[0].split('x')))
        self.geometry(self.center_on_monitor(self.mouse_on_monitor(), w, h))

    def toggle_fullscreen(self, evnt=None):
        self.update_idletasks()
        if self.attributes('-fullscreen'):
            self.attributes('-fullscreen', 0)
        else:
            self.attributes('-fullscreen', 1)
            self.attributes('-topmost', 1)

    def point_on_monitor_index(self, xy):
        for i, m in enumerate(sorted(screeninfo.get_monitors(), key=lambda m: m.x)):
            mon = [ int(getattr(m, 'x')),
                    int(getattr(m, 'y')),
                    int(getattr(m, 'x')) + int(getattr(m, 'width')),
                    int(getattr(m, 'y')) + int(getattr(m, 'height')),
                    ]
            if mon[0] < xy[0] and xy[0] < mon[2]:
                if mon[1] < xy[1] and xy[1] < mon[3]:
                    return i
        return 0

    def point_on_monitor(self, xy):
        for m in sorted(screeninfo.get_monitors(), key=lambda m: m.x):
            mon = [ int(getattr(m, 'x')),
                    int(getattr(m, 'y')),
                    int(getattr(m, 'x')) + int(getattr(m, 'width')),
                    int(getattr(m, 'y')) + int(getattr(m, 'height')),
                    ]
            if mon[0] < xy[0] and xy[0] < mon[2]:
                if mon[1] < xy[1] and xy[1] < mon[3]:
                    return mon
        return None

    def mouse_on_monitor(self):
        xy = self.winfo_pointerxy()
        return self.point_on_monitor(xy)

    def win_on_monitor(self):
        xy = list(map(int, self.geometry().split('+')[1:]))
        return self.point_on_monitor(xy)

    def win_geom_int(self):
        w, h = list(map(int, self.geometry().split('+')[0].split('x')))
        x, y = list(map(int, self.geometry().split('+')[1:]))
        return x, y, w, h

    def switch_monitor(self, evnt=None):
        km = sorted(screeninfo.get_monitors(), key=lambda m: m.x)
        if len(km) == 1: return
        fs = self.attributes('-fullscreen') == 1
        if fs:
            self.attributes('-fullscreen', 0)
        x, y, w, h = self.win_geom_int()
        tm = self.point_on_monitor_index((x+2,y+2)) + 1
        if tm >= len(km): tm = 0
        xpos = (km[tm].width // 2) + km[tm].x
        ypos = (km[tm].height // 2) + km[tm].y
        mon_point = self.point_on_monitor((xpos, ypos))
        ng = self.center_on_monitor(mon_point, w, h)
        self.geometry(ng)
        if fs:
            self.attributes('-fullscreen', 1)
            self.attributes('-topmost', 1)

    def center_on_monitor(self, mon, w, h):
        # mon is rectangle [x1, y1, x2, y2]
        xpos = (((mon[2] - mon[0]) - w) // 2) + mon[0]
        ypos = (((mon[3] - mon[1]) - h) // 2) + mon[1]
        return f'{w}x{h}+{xpos}+{ypos}'

