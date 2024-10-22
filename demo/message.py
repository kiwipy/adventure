"""
All monologues displayed when examining objects or performs actions.
Monologue will get removed from the lists when used, leaving the last one.

Keys correspond to object attribute "state"
Null = monologue for inactive objects
Done = objects that have served it's purpose
"""
data = {
"bed": {
    "Null": ["It's a bed with a person sitting on it."]
    },
"table": {
    "Null": ["This small table has a drawer.",
             "It's a small table with a drawer."],
    },
"drawer": {
    "Null": ["You can put things in drawers.",
             "Maybe someone left something in here...",
             "Just open the drawer already!"],
    "open": ["There is a key here!",
             "This key might be useful..."],
    "done": ["This drawer looks empty.",
             "You have already looked in this drawer."]
    },
"key": {
    "Null": ["Keys usually unlockes things.",
             "This key might unlock the door..."],
    "get": ["You picked up the key.",
            "You have a key."],
    "use": ["The door is open.",
            "You have already used the key."]
    },
"door": {
    "Null": ["This door is locked.",
             "You need a key to open this door."],
    "open": ["The door is open.",
             "It's an open door..."]
    },
"john": {
    "Null": ["Looks like a man.",
             "It's a man sitting on a bed.",
             "Have you not seen a man before?"]
    },
}
