import asyncio
import getpass
import json
import os
import pprint
import websockets

from mapa import Map
from consts import Tiles

import random

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        keys = ["w","a","s","d"]
        
        while True:
            try:
                # receive game update, this must be called timely or your game will get out of sync with the server
                update = json.loads(await websocket.recv())  

                if "map" in update:
                    # we got a new level
                    # only runs at the beginning of a level!!!
                    game_properties = update
                    mapa = Map(update["map"])
                    print("\n###### GAME PROPs ######\n")
                    print(game_properties)

                    print("\n###### UPDATE ######\n")
                    pprint.pprint(update)
                else:
                    # we got a current map state update
                    # runs everytime a message is received
                    state = update
                    
                    print("\n###### STATE ######\n")
                    pprint.pprint(state)

                
                print("\n###### EMPTY GOALS ######\n")
                print(mapa.empty_goals)

                # todos os goals do mapa
                print("\n###### GOALS ######\n")
                print(mapa.filter_tiles([Tiles.GOAL, Tiles.BOX_ON_GOAL]))

                key = random.choice(keys)
                                
                # send key command to server
                await websocket.send(json.dumps({"cmd": "key", "key": key}))
            
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return

# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
