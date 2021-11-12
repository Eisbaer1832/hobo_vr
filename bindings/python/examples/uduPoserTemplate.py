# SPDX-License-Identifier: GPL-2.0-only

# Copyright (C) 2020 Oleg Vorobiov <oleg.vorobiov@hobovrlabs.org>

"""
this is an example of using virtualreality.templates

to get detailed overview of virtualreality.templates.PoserTemplate run this in your python interpreter:
	help(virtualreality.templates.PoserTemplate)

more examples/references:
	https://github.com/okawo80085/hobo_vr/blob/master/virtualreality/trackers/color_tracker.py

"""

import asyncio
import time
import numpy as np
from fractions import Fraction
import re
import pyrr

from virtualreality import templates


class MyPoser(templates.UduPoserTemplate):
    _CLI_SETTS = '''hobo_vr poser

Usage: poser [-h | --help] [options]

Options:
    -h, --help              shows this message
    -q, --quit              exits the poser
    -t, --test <pair>       test
    -e, --ipd <millim>      ipd in meters, float
    -u, --udu <string>      new udu string
    -T, --tr <loc>          set new location of the tracking reference, format float: x,y,z
    -d, --dist <val>        new distortion parameters, format float: k1,k2,zw,zh
    -i, --eyeGap <val>      new eye gap in pixels, int
'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.coro_keep_alive['send'].is_alive = False
        # self.coro_keep_alive['send'].sleep_delay = 1

    async def _cli_arg_map(self, pair):
        if pair[0] == "--test" and pair[1]:
            a, b = pair[1].split(',')
            a, b = int(a), int(b)
            data = templates.settManager_Message_t.pack(a, b, *np.zeros((128,), dtype=np.uint32))
            resp = await self._send_manager(data)
            print (resp)

        elif pair[0] == "--tr" and pair[1]:
            f1, f2, f3 = [Fraction(i).limit_denominator(10000000) for i in pair[1].split(',')]
            data = templates.settManager_Message_t.pack(60, int(f1.numerator), int(f1.denominator), int(f2.numerator), int(f2.denominator), int(f3.numerator), int(f3.denominator), *np.zeros((123,), dtype=np.uint32))
            resp = await self._send_manager(data)
            print (resp)

        elif pair[0] == "--ipd" and pair[1]:
            f = Fraction(pair[1]).limit_denominator(10000000)
            data = templates.settManager_Message_t.pack(10, int(f.numerator), int(f.denominator), *np.zeros((127,), dtype=np.uint32))
            resp = await self._send_manager(data)
            print (resp)

        elif pair[0] == "--dist" and pair[1]:
            k1, k2, zw, zh = [Fraction(i).limit_denominator(10000000) for i in pair[1].split(',')]
            data = templates.settManager_Message_t.pack(40, int(k1.numerator), int(k1.denominator), int(k2.numerator), int(k2.denominator), int(zw.numerator), int(zw.denominator), int(zh.numerator), int(zh.denominator), *np.zeros((121,), dtype=np.uint32))
            resp = await self._send_manager(data)
            print (resp)

        elif pair[0] == "--eyeGap" and pair[1]:
            newGap = int(pair[1])
            data = templates.settManager_Message_t.pack(50, newGap, *np.zeros((128,), dtype=np.uint32))
            resp = await self._send_manager(data)
            print (resp)

        elif pair[0] == "--udu" and pair[1]:
            res = await self._sync_udu(pair[1])
            if res:
                print (res)


    @templates.PoserTemplate.register_member_thread(1 / 100)
    async def example_thread1(self):
        """moves the headset in a circle"""
        h = 0
        while self.coro_keep_alive["example_thread1"].is_alive:
            try:
                self.poses[0].z = np.sin(h)/3
                self.poses[0].x = np.cos(h/2)/3
                self.poses[0].y = np.cos(h/2)/3
                x, y, z, w = pyrr.Quaternion.from_z_rotation(h/5)
                self.poses[0].r_x = x
                self.poses[0].r_y = y
                self.poses[0].r_z = z
                self.poses[0].r_w = w
                h += 0.01

                await asyncio.sleep(self.coro_keep_alive["example_thread1"].sleep_delay)

            except Exception as e:
                print(f"example_thread1 failed: {e}")
                break
        self.coro_keep_alive["example_thread1"].is_alive = False

    @templates.PoserTemplate.register_member_thread(1 / 100, runInDefaultExecutor=True)
    def example_thread2(self):
        """moves the controller up and down"""
        h = 0
        while self.coro_keep_alive["example_thread2"].is_alive:
            try:
                if len(self.poses) > 1:
                    for i in range(1, len(self.poses)):
                        self.poses[i].y = 1 + np.cos(h+i) / 5
                    h += 0.01

                time.sleep(self.coro_keep_alive["example_thread2"].sleep_delay)

            except Exception as e:
                print(f"example_thread2 failed: {e}")
                break
        self.coro_keep_alive["example_thread2"].is_alive = False


poser = MyPoser('h c c')

asyncio.run(poser.main())
