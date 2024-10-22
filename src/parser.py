"""
File:        parser.py
Comment:     Library for text adventure
Copyright:   William Andersson 2024
Website:     https://github.com/william-andersson
License:     GPLv3

Description: Parse user input and return actions as lowercase
             and objects as uppercase. Takes exactly 2 arguments,
             (STRING, LIST) where STRING is user input and LIST is
             a combined single dimension list of e.g.
             backpack content and tokens from current location.
             The function returns type tuple.
"""
VerbList = (
    # where to put 'poke' (in 'talk')?
    (('look', 'watch', 'inspect', 'examine', 'list', 'view', 'search'), 'view'),
    (('hit', 'kick', 'punch', 'slap', 'stab', 'fight', 'smash'), 'hit'),
    (('get', 'take', 'pick', 'pickup', 'grab'), 'get'),
    (('drop', 'toss', 'loose', 'throw'), 'drop'),
    (('use', 'sit', 'sleep', 'unlock'), 'use'),
    (('talk', 'ask', 'speak', 'say'), 'talk'),
    (('go', 'walk', 'run', 'climb'), 'go'),
    (('give', 'offer',), 'give'),
    (('move', 'push'), 'move'),
    (('eat', 'drink'), 'eat'),
    (('jump',), 'jump'),
    (('open',), 'open')
    )
NounList = (
    (('hand', 'fist', 'foot', 'feet', 'head', 'body', 'me', 'myself', 'i', 'self'), 'SELF'),
    (('up', 'north', 'forward', 'forth', 'n'), 'NORTH'),
    (('down', 'south', 'backward', 'back', 's'), 'SOUTH'),
    (('left', 'east', 'e'), 'EAST'),
    (('right', 'west', 'w'), 'WEST'),
    (('bag', 'backpack', 'inventory'), 'INVENTORY')
    )

def decode(InputString, Max, Objects):
    OutputString = []
    max_count = 0
    
    for word in InputString.split():
        # Adds all Objects
        if word.lower() in Objects:
            OutputString.append(word.upper())
        else:
            for List in VerbList:
                # Adds as many verbs (actions) as Max value allows.
                for Word in List[0]:
                    if word.upper() == Word.upper():
                        if VerbList[VerbList.index(List)][1] not in OutputString:
                            if max_count < Max:
                                OutputString.append(VerbList[VerbList.index(List)][1])
                                max_count += 1
            for List in NounList:
                # Adds all nouns from InputString
                for Word in List[0]:
                    if word.upper() == Word.upper():
                        if NounList[NounList.index(List)][1] not in OutputString:
                            OutputString.append(NounList[NounList.index(List)][1])

    if len(OutputString) < 2:
        raise Exception("parser.py: return value should be more than 1, not '%s'" % len(OutputString))
    else:
        return tuple(OutputString)
