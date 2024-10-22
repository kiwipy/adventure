"""
This is the main body of the game, containing all data for each stage.
NOTE: NPC's should be in both "objects" and "npc". In the objects list
the NPC should be reffered to as in the story "text" and optionally also
by name, then referenced to the correct object in "npc". As "john" is the
object here there is no need to map other than "person".

Available directions are located in "paths" where direction correspend to
a new area or "None". If set to "False" the player can not go there until
set to "True" by object attribute "triggers".
"""
data = {
"001": {
"dropped": [],
"paths": {"north": {"None": "False"},
          "south": {"None": "False"},
          "east": {"None": "False"},
          "west": {"002": "False"}},
"npc": {"person": "john"},
"objects": ["key", "drawer", "door", "bed", "table", "person", "john"],
"text": "You are standing in a small room. There is a door to your right and a bed with a small table next to it. There is a person sitting on the bed."
},

"002": {
"dropped": [],
"paths": {"north": {"None": "False"},
          "south": {"None": "False"},
          "east": {"None": "False"},
          "west": {"None": "False"}},
"npc": {},
"objects": [],
"text": "*** Congratulations! You have won the game... ***"
}
}
