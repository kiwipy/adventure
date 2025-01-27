# Adventure
> [!IMPORTANT]
> This entire project is set for complete re-write sometime in the future and will not recieve any updates untill then.<br>

Adventure is a client for classic text adventure games. Just load a compatible json gamefile to start playing! There is a small demo game in the demo directory wich can be modified and extended to create a fantastic text adventure for the enthusiast.

![Screenshot](https://github.com/william-andersson/adventure/blob/main/Screenshot.png)

## Make it work
**Requirements: meson, ninja-build, cmake, glib2-devel**<br>
Build and install with **`./build.sh --install`** and then run **`adventure`** or **`adventure-cli /path/to/gamefile`** if you prefer the terminal :slightly_smiling_face:
Game progress can be saved using the gui application's save function or by typing **`/save /path/to/savefile`** from the terminal interface.
> [!NOTE]
> Keep in mind that the save function saves the entire game to a new file or overwrites the original if chosen. To resume, all you have to do is loading the created save file.

## Creating you own game
The files in the demo directory have descriptive comments in the header. To prepare the files as a gamefile run: **`./compile.py`**

> [!IMPORTANT]
> :purple_square: Adventure is still in heavy development and things might change or break along the way!<br>
> :purple_square: You should **NOT** create any full sized games until version 1 is released.

## Features planned for the future
> - [ ] First stable release.<br>
> - [ ] Write a more extensive documentation.<br>
> - [ ] Add GUI for easy game creation.<br>
