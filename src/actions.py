"""
File:        actions.py
Comment:     Library for text adventure
Copyright:   William Andersson 2024
Website:     https://github.com/william-andersson
License:     GPLv3

Description: Manages all the actions taken by the player.
"""
import textwrap

def UpdateObjects(Object, Attr, Action, GAME):
    # Updates object attributes from object triggers.
    for action in Attr['triggers']:
        if action == Action:
            #print("---------------")
            for _next in Attr['triggers'][Action].keys():
                for obj in Attr['triggers'][Action][_next].keys():
                    if obj == 'paths':
                        for path in Attr['triggers'][Action][_next][obj].keys():
                            state = Attr['triggers'][Action][_next][obj][path]
                            key = next(iter(GAME['locations'][GAME['location']]['paths'][path]))
                            GAME['locations'][GAME['location']]['paths'][path][key] = state
                            Attr['state'] = Action
                            #print(f"Debug: '{Object}' state = '{Attr['state']}'")
                            #print(f"Debug: {GAME['locations'][GAME['location']]['paths'][path]}")
                    else:
                        if Action != 'view':
                            Attr['state'] = Action
                            #print(f"Debug: '{Object}' state = '{Attr['state']}'")
                        for attr in Attr['triggers'][Action][_next][obj].keys():
                            GAME['objects'][obj][attr] = Attr['triggers'][Action][_next][obj][attr]
                            #print(f"Debug: {obj}: {attr} = {GAME['objects'][obj][attr]}")
            if Action != 'talk':
                if len(GAME['message'][Object][Attr['state']]) < 2:
                    feedback = GAME['message'][Object][Attr['state']][0]
                else:
                    feedback = GAME['message'][Object][Attr['state']].pop(0)
                return feedback

def go(Path, GAME):
    Location = GAME['locations'][GAME['location']]
    path = Path[0].lower()

    if path == 'self':
        RESULT = (GAME['events']['go']["self"])
        return RESULT
    if path in Location['paths']:
        location = next(iter(Location['paths'][path]))
        if Location['paths'][path][location] == 'True':
            GAME['location'] = location
            #print(f"\n{textwrap.fill(GAME['locations'][GAME['location']]['text'])}")
            RESULT = "Go %s" % path
        else:
            RESULT = (GAME['events']['go']["cant"])
    elif path == 'inventory':
        RESULT = (GAME['events']['go']["backpack"])
    elif path not in Location['paths']:
        RESULT = (GAME['events']['go']["nope"] % path)
    return RESULT

def view(Objects, GAME):
    Inventory = GAME['inventory']
    Location = GAME['locations'][GAME['location']]
    Object = Objects[0].lower()

    if Object in Location['npc']:
        # Translate item into NPC name
        Attr = GAME['objects'][Location['npc'][Object]]
    elif Object == 'inventory':
        pass
    else:
        Attr = GAME['objects'][Object]

    if Object == 'self':
        RESULT = (GAME['events']['view']["self"])
        return RESULT

    if Object in Location['objects'] or Object in Inventory:
        if Object in Location['npc']:
            Object = Location['npc'][Object]
        if Attr['visible'] == 'True':
            if 'view' not in Attr['triggers']:
                # Print object details
                if len(GAME['message'][Object][Attr['state']]) < 2:
                    RESULT = (GAME['message'][Object][Attr['state']][0])
                else:
                    RESULT = (GAME['message'][Object][Attr['state']].pop(0))
            else:
                RESULT = UpdateObjects(Object, Attr, 'view', GAME)
        else:
            RESULT = (GAME['events']['view']["none"] % Object)
    else:
        if Object == 'inventory':
            RESULT = (GAME['events']['view']["backpack"] % GAME['inventory'])
        else:
            RESULT = (GAME['events']['view']["none"] % Object)
    return RESULT

def get(Objects, GAME):
    Inventory = GAME['inventory']
    Location = GAME['locations'][GAME['location']]
    Object = Objects[0].lower()

    if Object in Location['npc']:
        # Translate item into NPC name
        Attr = GAME['objects'][Location['npc'][Object]]
    elif Object == 'inventory':
        pass
    else:
        Attr = GAME['objects'][Object]

    if Object == 'self':
        RESULT = (GAME['events']['get']["self"])
        return RESULT

    if Object in Inventory:
        RESULT = (GAME['events']['get']["have"] % Object)
    elif Object in Location['objects']:
        if Attr['visible'] == 'True':
            if Attr['collectable'] == 'True':
                Inventory.append(Location['objects'].pop( \
                    Location['objects'].index(Object)))
                RESULT = UpdateObjects(Object, Attr, 'get', GAME)
            else:
                RESULT = (GAME['events']['get']["cant"])
        else:
            RESULT = (GAME['events']['get']["none"] % Object)
    elif Object in Location['dropped']:
        Inventory.append(Location['dropped'].pop(Location['dropped'].index(Object)))
        RESULT = (GAME['events']['get']["drop"] % Object)
    else:
        if Object == 'inventory':
            RESULT = (GAME['events']['get']["backpack"])
        else:
            RESULT = (GAME['events']['get']["none"] % Object)
    return RESULT

def drop(Objects, GAME):
    Inventory = GAME['inventory']
    Location = GAME['locations'][GAME['location']]
    Object = Objects[0].lower()

    if Object in Location['npc']:
        # Translate item into NPC name
        Attr = GAME['objects'][Location['npc'][Object]]
    elif Object == 'inventory':
        pass
    else:
        Attr = GAME['objects'][Object]

    if Object == 'self':
        RESULT = (GAME['events']['drop']["self"])
        return RESULT

    if Object in Inventory:
        if Attr['droppable'] == 'True':
            Location['dropped'].append(Inventory.pop(Inventory.index(Object)))
            RESULT = UpdateObjects(Object, Attr, 'drop', GAME)
        else:
            RESULT = (GAME['events']['drop']["need"])
    else:
        if Object == 'inventory':
            RESULT = (GAME['events']['drop']["backpack"])
        else:
            RESULT = (GAME['events']['drop']["none"] % Object)
    return RESULT

def use(Objects, GAME):
    Inventory = GAME['inventory']
    Location = GAME['locations'][GAME['location']]
    Object = Objects[0].lower()

    if Object in Location['npc']:
        # Translate item into NPC name
        Attr = GAME['objects'][Location['npc'][Object]]
    elif Object == 'inventory':
        pass
    else:
        Attr = GAME['objects'][Object]

    if Object == 'self':
        RESULT = (GAME['events']['use']["self"])
        return RESULT

    if Object in Inventory:
        if Attr['usable'] == 'True':
            if Objects[1].lower() in Attr['triggers']['use'].keys():
                RESULT = UpdateObjects(Object, Attr, 'use', GAME)
            else:
                RESULT = (GAME['events']['use']["dont"])
        else:
            RESULT = (GAME['events']['use']["cant"])
    else:
        if Object == 'inventory':
            RESULT = (GAME['events']['use']["backpack"])
        elif Attr['usable'] == 'True':
            RESULT = (GAME['events']['use']["none"] % Object)
    return RESULT

def give(Objects, GAME):
    Inventory = GAME['inventory']
    Location = GAME['locations'][GAME['location']]
    Object = Objects[0].lower()

    if Object in Location['npc']:
        # Translate item into NPC name
        Attr = GAME['objects'][Location['npc'][Object]]
    elif Object == 'inventory':
        pass
    else:
        Attr = GAME['objects'][Object]

    if Object == 'self':
        RESULT = (GAME['events']['give']["self"])
        return RESULT

    if Object in Inventory:
        if Attr['offerable'] == 'True':
            if Objects[1].lower() in Attr['triggers']['give'].keys():
                RESULT = UpdateObjects(Object, Attr, 'give', GAME)
            else:
                RESULT = (GAME['events']['give']["cant"] % obj)
        else:
            RESULT = (GAME['events']['give']["need"])
    else:
        if Object == 'inventory':
            RESULT = (GAME['events']['give']["backpack"])
        elif Attr['offerable'] == 'True':
            RESULT = (GAME['events']['give']["none"] % Object)
    return RESULT

def open(Objects, GAME):
    Inventory = GAME['inventory']
    Location = GAME['locations'][GAME['location']]
    Object = Objects[0].lower()

    if Object in Location['npc']:
        # Translate item into NPC name
        Attr = GAME['objects'][Location['npc'][Object]]
    elif Object == 'inventory':
        pass
    else:
        Attr = GAME['objects'][Object]

    if Object == 'self':
        RESULT = (GAME['events']['open']["self"])
        return RESULT

    if Object in Location['objects']:
        if Attr['visible'] == 'True':
            if Attr['openable'] == 'True':
                RESULT = UpdateObjects(Object, Attr, 'open', GAME)
            else:
                RESULT = (GAME['events']['open']["cant"])
        else:
            RESULT = (GAME['events']['open']["what"] % Object)
    elif Object == 'inventory':
        RESULT = (GAME['events']['open']["backpack"])
    else:
        RESULT = (GAME['events']['open']["none"] % Object)
    return RESULT

def move(Objects, GAME):
    Inventory = GAME['inventory']
    Location = GAME['locations'][GAME['location']]
    Object = Objects[0].lower()

    if Object in Location['npc']:
        # Translate item into NPC name
        Attr = GAME['objects'][Location['npc'][Object]]
    elif Object == 'inventory':
        pass
    else:
        Attr = GAME['objects'][Object]

    if Object == 'self':
        RESULT = (GAME['events']['move']["self"])
        return RESULT

    if Object in Location['objects']:
        if Attr['visible'] == 'True':
            if Attr['movable'] == 'True':
                RESULT = UpdateObjects(Object, Attr, 'move', GAME)
            else:
                RESULT = (GAME['events']['move']["cant"])
        else:
            RESULT = (GAME['events']['move']["dont"] % Object)
    elif Object == 'inventory':
        RESULT = (GAME['events']['move']["backpack"])
    else:
        RESULT = (GAME['events']['move']["none"] % Object)
    return RESULT

def eat(Objects, GAME):
    Inventory = GAME['inventory']
    Location = GAME['locations'][GAME['location']]
    Object = Objects[0].lower()

    if Object in Location['npc']:
        # Translate item into NPC name
        Attr = GAME['objects'][Location['npc'][Object]]
    elif Object == 'inventory':
        pass
    else:
        Attr = GAME['objects'][Object]

    if Object == 'self':
        RESULT = (GAME['events']['eat']["self"])
        return RESULT

    if Object in Location['objects'] or Object in Inventory:
        if Attr['visible'] == 'True':
            if Attr['eatable'] == 'True':
                RESULT = UpdateObjects(Object, Attr, 'eat', GAME)
            else:
                RESULT = (GAME['events']['eat']["nope"])
        else:
            if Attr['eatable'] == 'True':
                RESULT = (GAME['events']['eat']["none"] % Object)
            else:
                RESULT = (GAME['events']['eat']["what"])
    elif Object == 'inventory':
        RESULT = (GAME['events']['eat']["backpack"])
    return RESULT

def hit(Objects, GAME):
    Inventory = GAME['inventory']
    Location = GAME['locations'][GAME['location']]
    Object = Objects[0].lower()

    if Object in Location['npc']:
        # Translate item into NPC name
        Attr = GAME['objects'][Location['npc'][Object]]
    elif Object == 'inventory':
        pass
    else:
        Attr = GAME['objects'][Object]

    if Object == 'self':
        RESULT = (GAME['events']['hit']["self"])
        return RESULT

    if Object in Location['objects']:
        if Attr['hittable'] == 'True':
            if Objects[1].lower() in Attr['triggers']['hit'].keys():
                RESULT = UpdateObjects(Object, Attr, 'hit', GAME)
            else:
                RESULT = (GAME['events']['hit']["nope"])
        else:
            RESULT = (GAME['events']['hit']["cant"])
    elif Object == 'inventory':
        RESULT = (GAME['events']['hit']["backpack"])
    return RESULT

def jump(Objects, GAME):
    Inventory = GAME['inventory']
    Location = GAME['locations'][GAME['location']]
    Object = Objects[0].lower()

    if Object in Location['npc']:
        # Translate item into NPC name
        Attr = GAME['objects'][Location['npc'][Object]]
    elif Object == 'inventory':
        pass
    else:
        Attr = GAME['objects'][Object]

    if Object == 'self':
        RESULT = (GAME['events']['jump']["self"])
        return RESULT

    if Object in Location['objects']:
        if Attr['visible'] == 'True':
            if Attr['jumpable'] == 'True':
                if Attr['usable'] == 'True':
                    RESULT = UpdateObjects(Object, Attr, 'jump', GAME)
                else:
                    RESULT = (GAME['events']['jump']["nope"])
            else:
                RESULT = (GAME['events']['jump']["cant"])
    elif Object == 'inventory':
        RESULT = (GAME['events']['jump']["backpack"])
    return RESULT

def talk(Objects, GAME):
    Inventory = GAME['inventory']
    Location = GAME['locations'][GAME['location']]
    Object = Objects[0].lower()

    if Object in Location['npc']:
        # Translate item into NPC name
        Attr = GAME['objects'][Location['npc'][Object]]
        Object = Location['npc'][Object]
    elif Object == 'inventory':
        pass
    else:
        Attr = GAME['objects'][Object]

    if Object == 'self':
        RESULT = (GAME['events']['talk']["self"])
        return RESULT

    if Object in Location['objects']:
        if Attr['visible'] == 'True':
            if Attr['speechable'] == 'True':
                #UpdateObjects(Object, Attr, 'talk', GAME)
                RESULT = ("NPC", Object)
            else:
                RESULT = (GAME['events']['talk']["cant"])
        else:
            RESULT = (GAME['events']['talk']["none"] % Object)
    elif Object == 'inventory':
        RESULT = (GAME['events']['talk']["backpack"])
    return RESULT
