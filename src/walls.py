import pygame as pg
import src.settings as settings


class WALL(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([width,height])
        self.image.fill((254, 255, 254))

        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x


def make_wall(val, x, y):
    params = settings.params()
    walls = {'1': [WALL(x, y, 32, 4, params['bck_color']),    # Up
                  ],
             '2': [WALL(x, y+32, 32, 4, params['bck_color']),  # Down
                  ],
             '3': [WALL(x, y, 32, 4, params['bck_color']),    # Up
                   WALL(x, y+32, 32, 4, params['bck_color']),  # Down
                  ],
             '4': [WALL(x, y, 4, 32, params['bck_color']),    # Left
                  ],
             '5': [WALL(x, y, 32, 4, params['bck_color']),    # Up
                   WALL(x, y, 4, 32, params['bck_color']),    # Left
                  ],
             '6': [WALL(x, y+32, 32, 4, params['bck_color']),  # Down
                   WALL(x, y, 4, 32, params['bck_color']),    # Left
                  ],
             '7': [WALL(x, y, 32, 4, params['bck_color']),    # Up
                   WALL(x, y+32, 32, 4, params['bck_color']),  # Down
                   WALL(x, y, 4, 32, params['bck_color']),    # Left
                  ],
             '8': [WALL(x+32, y, 4, 32, params['bck_color'])  # Right
                  ],
             '9': [WALL(x, y, 32, 4, params['bck_color']),    # Up
                   WALL(x+32, y, 4, 32, params['bck_color'])  # Right
                  ],
             'A': [WALL(x, y+32, 32, 4, params['bck_color']),  # Down
                   WALL(x+32, y, 4, 32, params['bck_color'])  # Right
                  ],
             'B': [WALL(x, y, 32, 4, params['bck_color']),    # Up
                   WALL(x, y+32, 32, 4, params['bck_color']),  # Down
                   WALL(x+32, y, 4, 32, params['bck_color'])  # Right
                  ],
             'C': [WALL(x, y, 4, 32, params['bck_color']),    # Left
                   WALL(x+32, y, 4, 32, params['bck_color'])  # Right
                  ],
             'D': [WALL(x, y, 32, 4, params['bck_color']),    # Up
                   WALL(x, y, 4, 32, params['bck_color']),    # Left
                   WALL(x+32, y, 4, 32, params['bck_color'])  # Right
                  ],
             'E': [WALL(x, y+32, 32, 4, params['bck_color']),  # Down
                   WALL(x, y, 4, 32, params['bck_color']),    # Left
                   WALL(x+32, y, 4, 32, params['bck_color'])  # Right
                  ],

             'G': [
                    WALL(x, y+16, 32, 4, params['bck_color']),  # Down 1/2
                  ],
             'H':[
                    WALL(x+16, y, 4, 32, params['bck_color']),  # Right 1/2
                 ],
             'I':[
                    WALL(x+16, y, 4, 16, params['bck_color']),  # Down 1/2
                 ],
             'J':[
                    WALL(x+16, y, 4, 16, params['bck_color']),  # Right 1/2
                    WALL(x+16, y+16, 16, 4, params['bck_color']),  # Down 1/2
                 ],
             'K':[
                    WALL(x+16, y+16, 4, 16, params['bck_color']),  # Down 1/2
                 ],
             '0': [WALL(x, y, 32, 4, params['bck_color']),    # Up
                   WALL(x, y+32, 32, 4, params['bck_color']),  # Down
                   WALL(x, y, 4, 32, params['bck_color']),    # Left
                   WALL(x+32, y, 4, 32, params['bck_color'])  # Right
                  ],
             }
    return walls[val]


def set_walls(wall_file, shift_x, shift_y):
    out = []
    with open(wall_file, 'r') as r:
        walls = r.read()
    walls = walls.strip('\r').split('\n')
    # height
    for r in range(len(walls)):
        # width
        for c in range(len(walls[r])):
            if walls[r][c] is not 'F':
                x = c * 32 + shift_x
                y = r * 32 + shift_y
                out.extend(make_wall(walls[r][c], x, y))
    return out


def update_walls(wall_list, shift_x, shift_y):
     for w in wall_list:
          w.rect.left += shift_x
          w.rect.top += shift_y
#     return wall_list