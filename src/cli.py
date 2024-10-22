# cli.py
#
# Copyright 2024 William Andersson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys
import os.path
import json
import textwrap
import readline
from . import parser
from . import actions

MAX_ACTIONS = 1
GAME = {}
NPC = ""


def load(path):
    global GAME
    if os.path.exists('%s' % path):
        try:
            with open('%s' % path, 'r') as FILE:
                GAME = json.load(FILE)
                os.system('clear')
                print(f"{textwrap.fill(GAME['locations'][GAME['location']]['text'])}\n\n")
        except Exception as err:
            print(f"Unable to open {path}: Not JSON format: {err}")
            return

def save(path):
    global GAME
    if os.path.exists('%s' % path):
        if input("File exists, overwrite y/n? ").lower() == 'y':
            try:
                with open('%s' % path, 'w') as FILE:
                    json.dump(GAME, FILE)
                print(f"file saved: {path}")
            except Exception as err:
                print(f"Unable to save as file {path}: {err}")
                return
        else:
            print("Aborted.")
            return
    else:
        try:
            with open('%s' % path, 'w') as FILE:
                json.dump(GAME, FILE)
                print(f"file saved: {path}")
        except Exception as err:
            print(f"Unable to save as file {path}: {err}")
            return

def GetObjects():
    global GAME
    Objects = GAME['inventory'] + GAME['locations'][GAME['location']]['objects'] + \
        GAME['locations'][GAME['location']]['dropped']
    return Objects

def main(version, path):
    global GAME, MAX_ACTIONS, NPC
    load(path)

    RUN = {'get': actions.get, 'drop': actions.drop, 'view': actions.view,
           'open': actions.open, 'use': actions.use, 'move': actions.move,
           'give': actions.give, 'eat': actions.eat, 'hit': actions.hit,
           'jump': actions.jump, 'go': actions.go, 'talk': actions.talk}

    while GAME['objects']['self']['state'] == 'Alive':
        Action = {}
        try:
            Input = input(">>> ").lower()
            if NPC != "":
                Command = Input
            elif '/save' in Input:
                save(Input.split()[1])
            else:
                Command = parser.decode(Input, MAX_ACTIONS, GetObjects())
        except Exception as err:
            print(err)
        else:
            for item in Command:
                if item.islower():
                    key=item
                    Action[key] = []
                else:
                    try:
                        Action[key].append(item)
                    except Exception as err:
                        Action['view'] = []
                        Action['view'].append(item)
            for key in Action.keys():
                try:
                    if NPC == "":
                        output = RUN[key](Action[key], GAME)
                        if output[0] == "NPC":
                            NPC = output[1]
                            os.system('clear')
                            print(GAME['dialogs'][output[1]][GAME['objects'][output[1]]['state']])
                        else:
                            os.system('clear')
                            TEXT = GAME['locations'][GAME['location']]['text'] + "\n\n"
                            for item in GAME['locations'][GAME['location']]['dropped']:
                                TEXT += GAME['events']['view']["drop"] % item.upper()
                            print(TEXT)
                            print(output)
                    elif NPC != "":
                        if Command == "z":
                            NPC = ""
                            os.system('clear')
                            TEXT = GAME['locations'][GAME['location']]['text'] + "\n\n"
                            for item in GAME['locations'][GAME['location']]['dropped']:
                                TEXT += GAME['events']['view']["drop"] % item.upper()
                            print(TEXT)
                        else:
                            os.system('clear')
                            print(GAME['dialogs'][NPC][Command])
                except Exception as err:
                    print(f"actions.py: {err}")
