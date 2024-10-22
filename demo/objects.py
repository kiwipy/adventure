"""
All objects that appears in the game including NPC's.
The attributes controls what can be done with the object.
The "state" attribute should always be set to "Null" as starting point.

The "self" object:
Not to be confused with "self" in the triggers attribute.
This is the player, the game loop is active as long as the self attribute
"state" is set to "Alive". The "visible" and "movable" attributes can be used
to hide the player from enemies or rendered immovable by setting "movable" to
"False". The "energy" and "health" can be set to "False" if not in use (this
functionality is not yet implemented).

Jumpable objects:
An object with "jumpable" set to "True" can ONLY be jumped if "usable" also
is set to "True". This way the jump can be performed later.

Droppable objects:
Objects with attribute "droppable" set to "True" allows the player to drop
the object. However the object is dropped in THAT specific location and CAN
be picked up again if found UNLESS "collectable" is set to "False".

Triggers:
The "triggers" attribute is important for a functional gameplay.
The following example is the triggers for the "table" object:

    "triggers": {"view": {"self": {"drawer": {"visible": "True"}}}}

This means that when "table" is examined the "drawer" visible attribute is
set to "True". The "drawer" can NOT be examined before it is set to visible 
"True". (Triggers can be set to "None" for some objects, usually NPC's.)
Valid triggers are: (view,hit,get,drop,use,go,give,move,eat,jump,open and *talk)

All attributes except "state" and "triggers" use "True" or "False" values.
"""
data = {
"self": {
    "visible": "True",
    "movable": "True",
    "energy": "False",
    "health": "False",
    "state": "Alive"
    },
"bed": {
    "visible": "True",
    "collectable": "False",
    "openable": "False",
    "eatable": "False",
    "movable": "False",
    "droppable": "False",
    "offerable": "False",
    "speechable": "False",
    "hittable": "False",
    "jumpable": "False",
    "usable": "False",
    "state": "Null",
    "triggers": "None"
    },
"table": {
    "visible": "True",
    "collectable": "False",
    "openable": "False",
    "eatable": "False",
    "movable": "False",
    "droppable": "False",
    "offerable": "False",
    "speechable": "False",
    "hittable": "False",
    "jumpable": "False",
    "usable": "False",
    "state": "Null",
    "triggers": {"view": {"self": {"drawer": {"visible": "True"}}}}
    },
"drawer": {
    "visible": "False",
    "collectable": "False",
    "openable": "True",
    "eatable": "False",
    "movable": "False",
    "droppable": "False",
    "offerable": "False",
    "speechable": "False",
    "hittable": "False",
    "jumpable": "False",
    "usable": "False",
    "state": "Null",
    "triggers": {"open": {"self": {"key": {"visible": "True"},
                                   "table": {"triggers": "None"}}}}
    },
"key": {
    "visible": "False",
    "collectable": "True",
    "openable": "False",
    "eatable": "False",
    "movable": "False",
    "droppable": "False",
    "offerable": "False",
    "speechable": "False",
    "hittable": "False",
    "jumpable": "False",
    "usable": "True",
    "state": "Null",
    "triggers": {"get": {"self": {"drawer": {"state": "done", "triggers": "None"}}},
                 "use": {"door": {"door": {"openable": "True", "state": "open"},
                                  "paths": {"west": "True"}}}}
    },
"door": {
    "visible": "True",
    "collectable": "False",
    "openable": "False",
    "eatable": "False",
    "movable": "False",
    "droppable": "False",
    "offerable": "False",
    "speechable": "False",
    "hittable": "False",
    "jumpable": "False",
    "usable": "False",
    "state": "Null",
    "triggers": "None"
    },
"john": {
    "visible": "True",
    "collectable": "False",
    "openable": "False",
    "eatable": "False",
    "movable": "False",
    "droppable": "False",
    "offerable": "False",
    "speechable": "True",
    "hittable": "False",
    "jumpable": "False",
    "usable": "False",
    "state": "Null",
    "triggers": "None"
    }
}
