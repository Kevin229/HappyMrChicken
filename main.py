import random

import ScreenWindows
from ScreenWindows import ScreenWindows as appWindows
from MotherChicken import MotherChicken as Hen
import Configuration as config
import threading
from playsound import playsound

state_sound = 'introduce'


def play_sound():
    while True:
        playsound('eggcrack.mp3')
        s_state = state_sound
        if s_state == 'introduce':
            playsound('elsaSong.mp3')

    pass


# import ChickenLayEgg
if __name__ == '__main__':
    # ChickenLayEgg.game_intro()
    screen = appWindows("images/chicken/icon.bmp",
                        "HAPPY CHICKEN",
                        config.screenWidth,
                        config.screenHeight)

    arr = []
    main_windows_thread = threading.Thread(target=appWindows.buildWindows(screen), args=())
    play_sound_thread = threading.Thread(target=play_sound(), args=())

    play_sound_thread.start()
    play_sound_thread.join()
    main_windows_thread.start()
    main_windows_thread.join()
