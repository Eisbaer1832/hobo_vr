"""
this is a hobo_vr poser, enough said ┐(￣ヘ￣)┌

expects this serial data:
w,x,y,z\r\n

here is an example arduino sketch this will work with
https://gist.github.com/okawo80085/76d1b0cfbbd1ec8c6dbd825c109f59a5

this poser expects hobovr driver to have this udu setting:
h13

"""

import asyncio
import time
import numpy as np
import pyrr
from pyrr import Quaternion
import serial
import serial.threaded

from virtualreality import templates
from virtualreality.util import utilz as u

SERIAL_PORT = "/dev/ttyUSB0" # serial port

SERIAL_BAUD = 115200 # baud rate of the serial port

poser = templates.UduPoserClient("h")

@poser.thread_register(1 / 100)
async def serial_listener():
    try:
        irl_rot_off = Quaternion.from_x_rotation(0)  # supply your own imu offsets here, has to be a Quaternion object

        with serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1 / 4) as ser:
            with serial.threaded.ReaderThread(ser, u.SerialReaderFactory) as protocol:
                protocol.write_line("nut")
                await asyncio.sleep(5)

                print ('serial_listener: starting tracking thread')

                while poser.coro_keep_alive["serial_listener"].is_alive:
                    gg = u.get_numbers_from_text(protocol.last_read, ",")

                    if len(gg) >= 4:
                        w, x, y, z, *_ = gg
                        my_q = Quaternion([-y, z, -x, w])

                        my_q = Quaternion(my_q * irl_rot_off).normalised
                        poser.poses[0].r_w = round(my_q[3], 5)
                        poser.poses[0].r_x = round(my_q[0], 5)
                        poser.poses[0].r_y = round(my_q[1], 5)
                        poser.poses[0].r_z = round(my_q[2], 5)

                    await asyncio.sleep(poser.coro_keep_alive["serial_listener"].sleep_delay)

    except Exception as e:
        print (f'serial_listener: failed {e}')

    poser.coro_keep_alive["serial_listener"].is_alive = False

asyncio.run(poser.main())
