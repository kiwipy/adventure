#!/usr/bin/env python3
#
# Application: Compiler
# Comment:     Compile text adventure game into a single json file
# Copyright:   William Andersson 2024
# Website:     https://github.com/william-andersson
# License:     GPL
#
VERSION="0.1.0"
import os
import sys
import shutil
import datetime
import json
import metadata
import message
import locations
import objects
import events
import dialogs

_erro = 0
_warn = 0
_note = 0
_obje = 0
_loca = 0
_npcs = 0

date = datetime.datetime.now()
if sys.version_info < (3, 6):
    print("Requires python 3.6 or higher.")
    sys.exit(1)

# Load all files into main dictionary.
print(f"Assembling files...")
main = {}
main['copyright'] = f"Copyright (C) {date.year} {metadata.data['author']}"
main.update(metadata.data)
main["compatible"] = f"v{VERSION}+"
main["locations"] = locations.data
main["message"] = message.data
main["objects"] = objects.data
main["events"] = events.data
main["dialogs"] = dialogs.data

print(f"Checking for errors...")
# Check for errors in metadata.
if not main["filename"]:
    print(f"\033[31m\033[1mError: missing filename!\033[0m")
    _erro += 1
elif not main["title"]:
    print(f"\033[31m\033[1mError: missing title!\033[0m")
    _erro += 1
elif not main["location"]:
    print(f"\033[31m\033[1mError: missing location!\033[0m")
    _erro += 1
elif not main["version"]:
    print(f"\033[33m\033[1mWarning: missing version.\033[0m")
    _warn += 1
elif not main["author"]:
    print(f"\033[35m\033[1mNote:\033[0m missing author.")
    _note += 1
elif not main["copyright"]:
    print(f"\033[35m\033[1mNote:\033[0m missing copyright.")
    _note += 1

# Check for errors in objects.
for _object in main["objects"]:
    _loca = 0
    _obje += 1
    _passed = False
    if _object != "self":
        for _location in main["locations"]:
            _loca += 1
            if _object in main["locations"][_location]["objects"]:
                _passed = True
        if _passed != True:
            print(f"\033[35m\033[1mNote:\033[0m unused object -> {_object}")
            _note += 1
        if main["objects"][_object]["triggers"] != "None":
            for _trigger in main["objects"][_object]["triggers"]:
                if _trigger not in main["message"][_object]:
                    print(f"\033[35m\033[1mNote:\033[0m missing message for trigger {_object}:{_trigger}")
                    _note += 1
        elif main["objects"][_object]["state"] != "Null":
            print(f"\033[35m\033[1mNote:\033[0m {_object} state not equal Null")
            _note += 1
    else:
        if main["objects"]["self"]["state"] != "Alive":
            print(f"\033[31m\033[1mError: invalid state self:state -> {main["objects"]["self"]["state"]}\033[0m")
            _erro += 1
    for _attr in main["objects"][_object]:
        if _attr != "state" and _attr != "triggers":
            if main["objects"][_object][_attr] != "True" and \
                    main["objects"][_object][_attr] != "False":
                print(f"\033[31m\033[1mError: invalid attribute {_object}:{_attr} -> {main["objects"][_object][_attr]}\033[0m")
                _erro += 1
for npc in main["dialogs"]:
    _npcs += 1

# Summary
print(f"---- stats ----")
print(f"Objects: {_obje}\nStages: {_loca}\nNPCs: {_npcs}")
print(f"--- compiler ---")
print(f"Compiler: v{VERSION}")
print(f"\033[31m\033[1mErrors:\033[0m {_erro}\n\033[33m\033[1mWarnings:\033[0m {_warn}\n\033[35m\033[1mNotes:\033[0m {_note}")

# Write output file.
if _erro != 0:
    print(f"\n\033[31m\033[1mBuild failed!\033[0m")
else:
    with open("%s" % main["filename"], "w") as file:
        json.dump(main, file)
    print(f"---- output ----")
    print(f"Output: {main['filename']}")
    print(f"File size: {os.path.getsize("%s" % main["filename"]) / 1024:0,.2f} kB")
    print(f"Path: {os.getcwd()}")
shutil.rmtree("__pycache__")
