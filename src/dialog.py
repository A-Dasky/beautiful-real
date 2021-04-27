"""Dialog
"""
import os
import pygame as pg

import src.settings as settings


def get_char_sheets(x):
    cs = [
          '/chars/48x48_Faces_1st_Sheet_Update_CharlesGabriel_OGA_u.png',
          '/chars/48x48_Faces_2nd_Sheet_Update_CharlesGabriel_OGA_u.png',
          '/chars/48x48_Faces_3rd_Sheet_Update_CharlesGabriel_OGA_u.png',
          '/chars/48x48_Faces_4th_Sheet_Update_CharlesGabriel_OGA_u.png',
         ]
    return cs[x]


def get_char_img(x):
    dx = 48
    char_list = {'warrior_M': {'sheet': 0, 'pos': [0, 3]},
                 'magician_M': {'sheet': 0, 'pos': [1, 3]},
                 'healer_M': {'sheet': 0, 'pos': [2, 3]},
                 'ninja_M': {'sheet': 0, 'pos': [3, 3]},
                 'ranger_M': {'sheet': 0, 'pos': [4, 3]},
                 'npc_M': {'sheet': 0, 'pos': [5, 3]},
                 'warrior_F': {'sheet': 0, 'pos': [0, 4]},
                 'magician_F': {'sheet': 0, 'pos': [1, 4]},
                 'healer_F': {'sheet': 0, 'pos': [2, 4]},
                 'ninja_F': {'sheet': 0, 'pos': [3, 4]},
                 'ranger_F': {'sheet': 0, 'pos': [4, 4]},
                 'npc_F': {'sheet': 0, 'pos': [5, 4]},
                 'monk_M': {'sheet': 1, 'pos': [0, 4]},
                 'berserk_M': {'sheet': 1, 'pos': [1, 4]},
                 'darkknight_M': {'sheet': 1, 'pos': [2, 4]},
                 'soldier_M': {'sheet': 1, 'pos': [3, 4]},
                 'npc1_M': {'sheet': 1, 'pos': [4, 4]},
                 'npc2_M': {'sheet': 1, 'pos': [5, 4]},
                 'monk_F': {'sheet': 1, 'pos': [0, 5]},
                 'berserk_F': {'sheet': 1, 'pos': [1, 5]},
                 'darkknight_F': {'sheet': 1, 'pos': [2, 5]},
                 'soldier_F': {'sheet': 1, 'pos': [3, 5]},
                 'npc1_F': {'sheet': 1, 'pos': [4, 5]},
                 'npc2_F': {'sheet': 1, 'pos': [5, 5]},
                 'fire_E': {'sheet': 2, 'pos': [0, 3]},
                 'water_E': {'sheet': 2, 'pos': [1, 3]},
                 'wind_E': {'sheet': 2, 'pos': [2, 3]},
                 'earth_E': {'sheet': 2, 'pos': [3, 3]},
                 'light_E': {'sheet': 2, 'pos': [4, 3]},
                 'dark_E': {'sheet': 2, 'pos': [5, 3]},
                 'priest_M': {'sheet': 2, 'pos': [0, 4]},
                 'nun_F': {'sheet': 2, 'pos': [1, 4]},
                 'merchant_M': {'sheet': 2, 'pos': [2, 4]},
                 'cultist_M': {'sheet': 2, 'pos': [3, 4]},
                 'pirate_M': {'sheet': 2, 'pos': [4, 4]},
                 'captain_M': {'sheet': 2, 'pos': [5, 4]},
                 'samari_M': {'sheet': 3, 'pos': [0, 6]},
                 'child_M': {'sheet': 3, 'pos': [1, 6]},
                 'angel_M': {'sheet': 3, 'pos': [2, 6]},
                 'king_M': {'sheet': 3, 'pos': [3, 6]},
                 'old_M': {'sheet': 3, 'pos': [4, 6]},
                 'dancer_F': {'sheet': 3, 'pos': [5, 6]},
                 'samari_F': {'sheet': 3, 'pos': [0, 7]},
                 'child_F': {'sheet': 3, 'pos': [1, 7]},
                 'angel_F': {'sheet': 3, 'pos': [2, 7]},
                 'princess_F': {'sheet': 3, 'pos': [3, 7]},
                 'princess_O': {'sheet': 3, 'pos': [3, 7]},
                 'old_F': {'sheet': 3, 'pos': [4, 7]},
                 'bunny_F': {'sheet': 3, 'pos': [5, 7]},
                 'vampire_M': {'sheet': 3, 'pos': [0, 8]},
                 'bard_M': {'sheet': 3, 'pos': [1, 8]},
                 'paladin_M': {'sheet': 3, 'pos': [2, 8]},
                }
    return char_list[x]

def blit_text(surface, text, pos, font, color=pg.Color('black'), imgs_to_blit=[], char_pos=[500, 500], char_name=''):
    cwd = os.getcwd()
    params = settings.params()

    MSIZE = params['char_img_factor']

    # Get Char
    x, y = char_pos
    move_y = 0
    if y < 200:
        move_y = params['screen_height'] - 200

    gt = text
    words = [word.split(' ') for word in gt['content'].splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()

    # Get background
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck = pg.transform.scale(bck, (params['screen_width'], 200))
    # Display background
    surface.blit(bck, (0, move_y), bck.get_rect())

    # Get Arrow
    arrow = pg.image.load(cwd + '/imgs/textbox/arrowBrown_right.png')
    arrow = pg.transform.rotate(arrow, -90)

    if gt['char'] != '':
        print(text)
        ci = pg.image.load(cwd + '/' + get_char_sheets(gt['char']['sheet'])).convert()

        ch_x, ch_y = gt['char']['pos']
        char = pg.transform.rotozoom(ci, 0, MSIZE)
        char.set_colorkey((254, 255, 254))

        # Display Char
        surface.blit(char,
                     (50, move_y + (200-48*MSIZE)/2),
                     (ch_x*48*MSIZE, ch_y*48*MSIZE, 48*MSIZE, 48*MSIZE))
        x = 230
    else:
        x = 40
    y = 15

    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            # new line
            if x + word_width >= max_width - 5:
                #                x = pos[0] + 5 # Reset the x.
                # If there's an image, use 190
                x = 40
                if gt['char'] != '':
                    x = 230
                y += word_height  # Start on new row.
            for letter in word:
                letter_surface = font.render(letter, 0, color)
                letter_width, letter_height = letter_surface.get_size()
                surface.blit(letter_surface, (x, move_y + y))
                x += letter_width
                pg.time.delay(30)
                for img in imgs_to_blit:
                    img.draw(surface)
                pg.display.flip()
            x += space
        # Reset the x.
        x = 40
        if gt['char'] != '':
            x = 230
        y += word_height  # Start on new row.
    surface.blit(arrow, (params['screen_width']-100, move_y + 150), arrow.get_rect())
    pg.display.flip()
    return