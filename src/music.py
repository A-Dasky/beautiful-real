import os
import pygame as pg


def music_list(ind):
    """

    Parameters
    ----------
    ind: key
        key identifying path to the music file
    """
    music = {'hero_house': '/music/towns/TownTheme.mp3',
             'home_village': '/music/towns/TownTheme.mp3',
             'friends_house': '/music/towns/TownTheme.mp3',
             'home_vill_shops': '/music/towns/TownTheme.mp3',
             'elders_house': '/music/towns/TownTheme.mp3',
             'world': '/music/world/Plains03.ogg',
             'cave_no_gem': '/music/world/MysticalCaverns.ogg',
             'quiet_forest': '/music/world/Forest 02.ogg',
             'rest': '/music/rest/sleep_inn.ogg',
             'Sadness': '/music/story/Sadness.ogg',
             'Heiral': '/music/story/Last Minute.mp3',
             'BLANK': None,
             'memories': '/music/story/solomelodypiano1.ogg',
    }
    return music[ind]


def play_music(ind, until=-1):
    """

    """
    if ind == None:
        return
    pg.init()
    cwd = os.getcwd()
    pg.mixer.music.load(cwd + ind)
    pg.mixer.music.play(until, 0.0)
    return


def sound_list(ind):
    """

    Parameters
    ----------
    ind: key
        key identifying path to the sound file
    """
    sounds = {'menu': '/misc/menu/Menu_Selection_Click.wav',
              'rest': '/music/rest/sleep_inn.ogg',
              'buy_sell': '/misc/menu/sell_buy_item.wav',
              'change_equip': '/misc/menu/leather_inventory.wav',
              'menu_heal': '/misc/menu/piano.wav',
              'magicfail': '/misc/menu/magicfail.ogg',
              'door_open': '/misc/sounds/doorOpen_1.ogg',
              'pickaxe': '/misc/sounds/metal-clash.wav',
              'flash': '/misc/sounds/heal.ogg',
             }
    return sounds[ind]


def play_sound(sound_file, num=1):
    cwd = os.getcwd()
    sound = pg.mixer.Sound(cwd + sound_file)
    pg.mixer.Sound.play(sound, loops=num)


def pause_music():
    pg.mixer.music.pause()


def unpause_music():
    pg.mixer.music.unpause()

def stop_music():
    pg.mixer.music.stop()
