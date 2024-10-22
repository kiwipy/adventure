"""
This is the messages printed to screen for every in game action that fail.
The "key values" can NOT be changed but the MESSAGES ARE CHANGABLE.
Messages containing "%s" MUST retain this character as it is a placeholder
for an object. The "%s" character can NOT be added to messages that
do not contain it here.
"""
data = {
"go": {
    "nope": "You see the %s from here...",
    "cant": "You can't go there!",
    "self": "..?",
    "backpack": "You can't crawl into your backpack!"
    },
"get": {
    "none": "There is no %s here...",
    "cant": "You can't take that.",
    "have": "You already have a %s.",
    "drop": "You picked up the %s.",
    "self": "..?",
    "backpack": "It's on my back..."
    },
"drop": {
    "need": "You might need that.",
    "none": "You have no %s.",
    "self": "*Mic drop*",
    "backpack": "That would not be a good idea!"
    },
"view": {
    "drop": "There is a %s here..?",
    "none": "There is no %s here...",
    "self": "You look good today!",
    "backpack": "Your bag contains: %s"
    },
"open": {
    "cant": "You can't open that...",
    "what": "What %s?",
    "none": "There is no %s here.",
    "self": "..?",
    "backpack": "What's the point?"
    },
"use": {
    "dont": "That won't work...",
    "cant": "You can't use that.",
    "none": "You have no %s.",
    "self": "..?",
    "backpack": "For what?"
    },
"move": {
    "cant": "You can't move that...",
    "dont": "You can't see any %s here.",
    "none": "There is no %s here...",
    "self": "*Doing a little dance.*",
    "backpack": "..?"
    },
"give": {
    "cant": "You can't give this to %s.",
    "done": "You have already done this.",
    "need": "You should hold on to this.",
    "none": "You have no %s to give.",
    "self": "What..? A christmas present?",
    "backpack": "That's yours..."
    },
"eat": {
    "nope": "Maybe not...",
    "none": "You have no %s.",
    "what": "..?",
    "self": "..?",
    "backpack": "Are you THAT hungry?"
    },
"hit": {
    "nope": "That's not gonna work...",
    "cant": "That's pointless...",
    "self": "You can't do that!",
    "backpack": "That's not a good idea..."
    },
"jump": {
    "nope": "You might be able to later...",
    "cant": "You can't jump that.",
    "self": "*Jumping on one leg.*",
    "backpack": "..?"
    },
"talk": {
    "cant": "..?",
    "none": "There is no %s here.",
    "self": "..?",
    "backpack": "That's a weird thing to do."
    },
}
