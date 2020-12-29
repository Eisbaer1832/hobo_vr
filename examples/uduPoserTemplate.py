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
    -T, --tr <loc>          set new location of the tracking reference, format: num,num,num
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

        elif pair[0] == "--udu" and pair[1]:
            # update own udu
            newUduString = pair[1]
            re_s = re.search("([htc][ ])*([htc]$)", newUduString)

            if not newUduString or re_s is None:
                print ('invalid udu string')
                return

            if re_s.group() != newUduString:
                print ('invalid udu string')
                return

            newPoses = []
            new_struct = []
            for i in newUduString.split(' '):
                if i == "h" or i == "t":
                    newPoses.append(templates.Pose())

                elif i == "c":
                    newPoses.append(templates.ControllerState())

                new_struct.append(f"{i}{len(newPoses[-1])}")


            self.poses = newPoses
            new_struct = " ".join(new_struct)
            print (f"new udu settings: {repr(new_struct)}, {len(self.poses)} device(s) total")
            # send new udu
            udu_len = len(self.poses)
            type_d = {'h' : (0, 13), 'c' : (1, 22), 't' : (2, 13)}
            packet = np.array([type_d[i] for i in newUduString.split(' ')], dtype=np.uint32)
            packet = packet.reshape(packet.shape[0]*packet.shape[1])

            data = templates.settManager_Message_t.pack(20, udu_len, *packet, *np.zeros((128-packet.shape[0],), dtype=np.uint32))
            resp = await self._send_manager(data)
            print (resp)


    @templates.PoserTemplate.register_member_thread(1 / 100)
    async def example_thread1(self):
        """moves the headset in a circle"""
        h = 0
        while self.coro_keep_alive["example_thread1"].is_alive:
            try:
                self.poses[0].x = np.sin(h)
                self.poses[0].y = np.cos(h)
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
                self.poses[1].y = 1 + np.cos(h) / 5
                h += 0.01

                time.sleep(self.coro_keep_alive["example_thread2"].sleep_delay)

            except Exception as e:
                print(f"example_thread2 failed: {e}")
                break
        self.coro_keep_alive["example_thread2"].is_alive = False


poser = MyPoser('h c c')

asyncio.run(poser.main())
