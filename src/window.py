# window.py
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

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Gdk
from . import parser
from . import actions
import json

MAX_ACTIONS = 1
GAME = {}
NPC = ""

css_provider = Gtk.CssProvider()
css_provider.load_from_resource('/com/github/william_andersson/Adventure/style.css')
Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

@Gtk.Template(resource_path='/com/github/william_andersson/Adventure/window.ui')
class AdventureWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'AdventureWindow'

    open_button = Gtk.Template.Child()
    save_button = Gtk.Template.Child()
    main_text = Gtk.Template.Child()
    prompt = Gtk.Template.Child()
    text_input = Gtk.Template.Child()
    run_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        open_action = Gio.SimpleAction(name="open")
        open_action.connect("activate", self.open_file_dialog)
        self.add_action(open_action)

        save_action = Gio.SimpleAction(name="save")
        save_action.connect("activate", self.save_file_dialog)
        self.add_action(save_action)

        self.text_input.set_css_classes(['input'])
        self.main_text.set_css_classes(['textbox'])
        self.prompt.set_css_classes(['prompt'])
        buffer = self.main_text.get_buffer()
        buffer.set_text("\"It runs on the world's most powerful graphics chip, imagination\"\n\t- Sheldon Cooper.")

        # Run exec_command when hitting Enter or pressing the Run button.
        # This is the main application function.
        run_action = Gio.SimpleAction(name="run")
        run_action.connect("activate", self.exec_command)
        self.add_action(run_action)
        self.text_input.connect("activate", self.exec_command, None)

    def dialog(self):
        global GAME
        dialog = Gtk.AlertDialog()
        dialog.set_buttons(["Start"])
        dialog.set_message(GAME["title"])
        dialog.set_detail(f"{GAME['copyright'].center(50)}")
        dialog.show(self)

    def open_file_dialog(self, action, _):
        native = Gtk.FileDialog()
        native.open(self, None, self.on_open_response)

    def on_open_response(self, dialog, result):
        file = dialog.open_finish(result)
        # If the user selected a file...
        if file is not None:
            self.open_file(file)

    def open_file(self, file):
        global GAME
        path = file.peek_path()
        try:
            with open('%s' % path, 'r') as FILE:
                GAME = json.load(FILE)
                buffer = self.main_text.get_buffer()
                #buffer.set_text(GAME[GAME['location']]['text'])
                buffer.set_text(GAME['locations'][GAME['location']]['text'])
                self.dialog()
        except Exception as err:
            print(f"Unable to open {path}: Not JSON format: {err}")
            return
        self.text_input.grab_focus_without_selecting()

    def save_file_dialog(self, action, _):
        native = Gtk.FileDialog()
        native.save(self, None, self.on_save_response)

    def on_save_response(self, dialog, result):
        file = dialog.save_finish(result)
        if file is not None:
            self.save_file(file)

    def save_file(self, file):
        global GAME
        path = file.peek_path()
        try:
            with open('%s' % path, 'w') as FILE:
                json.dump(GAME, FILE)
        except Exception as err:
            print(f"Unable to save as file {path}: {err}")
            return

    def GetObjects(self):
        global GAME
        Objects = GAME['inventory'] + GAME['locations'][GAME['location']]['objects'] + \
            GAME['locations'][GAME['location']]['dropped']
        return Objects

    def exec_command(self, action, _):
        global GAME, MAX_ACTIONS, NPC
        buffer = self.main_text.get_buffer()
        Action = {}

        RUN = {'get': actions.get, 'drop': actions.drop, 'view': actions.view,
               'open': actions.open, 'use': actions.use, 'move': actions.move,
               'give': actions.give, 'eat': actions.eat, 'hit': actions.hit,
               'jump': actions.jump, 'go': actions.go, 'talk': actions.talk}

        if GAME['objects']['self']['state'] == 'Alive':
            try:
                if NPC != "":
                    Command = (self.text_input.get_text())
                else:
                    Command = parser.decode(self.text_input.get_text(), MAX_ACTIONS, self.GetObjects())
                self.text_input.set_text('')

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
                                self.prompt.set_text(output[0])
                                buffer.set_text(GAME['dialogs'][output[1]][GAME['objects'][output[1]]['state']])
                            else:
                                self.prompt.set_text(output)
                                TEXT = GAME['locations'][GAME['location']]['text'] + "\n\n"
                                for item in GAME['locations'][GAME['location']]['dropped']:
                                    TEXT += GAME['events']['view']["drop"] % item.upper()
                                buffer.set_text(TEXT)
                        elif NPC != "":
                            if Command == "z":
                                NPC = ""
                                self.prompt.set_text('')
                                TEXT = GAME['locations'][GAME['location']]['text'] + "\n\n"
                                for item in GAME['locations'][GAME['location']]['dropped']:
                                    TEXT += GAME['events']['view']["drop"] % item.upper()
                                buffer.set_text(TEXT)
                            else:
                                buffer.set_text(GAME['dialogs'][NPC][Command])

                    except Exception as err:
                        print(f"actions.py: {err}")
            except Exception as err:
                self.text_input.set_text('')
                print(f"{err}")
        else:
            return
