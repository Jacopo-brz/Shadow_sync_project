from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from pythonosc.udp_client import SimpleUDPClient
import asyncio
import random
import sys
import time
from datetime import datetime
import builtins as __builtin__
from threading import Thread


# Default Handler
def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")


dispatcher = Dispatcher()
dispatcher.set_default_handler(default_handler)

my_ip = "127.0.0.1"
listen_port = 1255
supercollider_port = 5555
to_me = SimpleUDPClient(my_ip, listen_port)
to_supercollider = SimpleUDPClient(my_ip, supercollider_port)


def send(array):
    to_supercollider.send_message("/correlation", array)


def correlation_controller(correlation, oldDur, dur):
    if correlation <= 0.2:
        value = [1, 0.05, oldDur, 2]
        dur = 0.05
    elif 0.2 < correlation <= 0.4:
        value = [1, 0.1, oldDur, 2]
        dur = 0.1
    elif 0.4 < correlation <= 0.6:
        value = [1, 0.5, oldDur, 1]
        dur = 0.5
    elif 0.6 < correlation < 0.8:
        value = [1, 1, oldDur, 1]
        dur = 1
    else:
        value = [1, 3, oldDur, 1]
        dur = 3
    oldDur = dur
    return oldDur, dur, value


async def app_main():
    BPM = 90
    value = [0, 0]  # play, midinote
    midiNote = 60
    globalDur = 2
    globalOldDur = 2

    send("start")
    for i in range(5):
        correlation = random.uniform(0.0, 1.0)

        [globalOldDur, globalDur, value] = correlation_controller(correlation, globalOldDur, globalDur)
        print(correlation)
        send(value)
        await asyncio.sleep(3)
    send(0)


async def init_main():
    server = AsyncIOOSCUDPServer(("0.0.0.0", listen_port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    await app_main()
    transport.close()


asyncio.run(init_main())
