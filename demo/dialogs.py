"""
All dialogs with NPC's.
The conversation is terminated with "z".
"""
data = {
"john": {
    "Null": "Greetings! My name is John, how may I help you?\n\n"
            "a) Who are you?\n"
            "b) The door is locked\n"
            "z) Bye",
    "a": "I'm John. I have been here for a long time.\n"
         "It's nice to finally get some company...\n\n"
         "b) The door is locked\n"
         "z) Bye",
    "b": "Yes, I can't remember where I left my key...\n\n"
         "c) Where is the key?\n"
         "z) Bye",
    "c": "I can't remember...\n"
         "z) Bye",
    "z": "Bye"
    },
}
