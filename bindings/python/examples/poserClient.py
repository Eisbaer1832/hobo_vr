# (c) 2021 Okawo
# This code is licensed under MIT license (see LICENSE for details)

"""
this is an example of using virtualreality.templates

to get basic overview of virtualreality.templates.PoserClient run this in your python interpreter:
    help(virtualreality.templates.PoserClient)

to get more info on virtualreality.templates.PoserTemplate run this in your python interpreter:
    help(virtualreality.templates.PoserTemplate)

or visit https://github.com/okawo80085/hobo_vr/blob/master/examples/poserTemplate.py

more examples/references:
    https://github.com/okawo80085/hobo_vr/blob/master/virtualreality/trackers/color_tracker.py

"""

import asyncio
import time
import numpy as np
import pyrr

from virtualreality import templates

poser = templates.PoserClient()


@poser.thread_register(1 / 60)
async def example_thread():
    h = 0
    while poser.coro_keep_alive["example_thread"].is_alive:
        # poser.pose.y = round(np.sin(h/2)-2, 4)
        poser.pose.y = 0
        # poser.pose.x = round(np.cos(h/2), 4)
        poser.pose.z = 0.3
        poser.pose_controller_l.x = round(0.5 - np.cos(h * 2) / 5, 4)
        poser.pose_controller_l.y = 0
        poser.pose_controller_r.z = round(-1 - np.cos(h * 2) / 5, 4)
        poser.pose_controller_r.y = 0.2

        x, y, z, w = pyrr.Quaternion.from_y_rotation(h)
        poser.pose.r_x = round(x, 4)
        poser.pose.r_y = round(y, 4)
        poser.pose.r_z = round(z, 4)
        poser.pose.r_w = round(w, 4)

        x, y, z, w = pyrr.Quaternion.from_z_rotation(h * 3)
        poser.pose_controller_r.r_x = round(x, 4)
        poser.pose_controller_r.r_y = round(y, 4)
        poser.pose_controller_r.r_z = round(z, 4)
        poser.pose_controller_r.r_w = round(w, 4)

        x, y, z, w = pyrr.Quaternion.from_z_rotation(-h * 3)
        poser.pose_controller_l.r_x = round(x, 4)
        poser.pose_controller_l.r_y = round(y, 4)
        poser.pose_controller_l.r_z = round(z, 4)
        poser.pose_controller_l.r_w = round(w, 4)

        h += 0.01

        await asyncio.sleep(poser.coro_keep_alive["example_thread"].sleep_delay)


# @poser.thread_register(1, runInDefaultExecutor=True)
# def example_thread2():
#     while poser.coro_keep_alive["example_thread2"].is_alive:
#         poser.pose.x += 0.2

#         time.sleep(poser.coro_keep_alive["example_thread2"].sleep_delay)


asyncio.run(poser.main())
