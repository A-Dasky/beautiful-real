import pygame as pg


def params():
    """Game params stored in a dic
    """
    game_params = {
                   'screen_width': 1280,
                   'screen_height': 720,
#                   'screen_width': 1500,
#                   'screen_height': 800,
                   'frames_per_second': 30,
                   'bck_color': (254, 255, 254),
                   'speed': 2,
                   'char_img_factor': 3.5,
                   'text_padding': 6,
                   'font_size': 28,
                  }
    return game_params


def get_screen(params):
    """Get screen
    """
    return pg.display.set_mode((params['screen_width'], params['screen_height']))


def get_screen_rect(screen):
    return screen.get_rect()


def get_screen_shift(screen):
    param = params()
    r = get_screen_rect(screen)
    shift_x = 0
    shift_y = 0
    if r.width < param['screen_width']:
        shift_x = (param['screen_width'] - r.width) / 2
    if r.height < param['screen_height']:
        shift_y = (param['screen_height'] - r.height) / 2
    return shift_x, shift_y


def get_move_background(zone, mx, my, top=0, left=0):
    """
    mx, my - current shift in background
    top, left - player rect.topleft
    """
    param = params()
    h = param['screen_height']
    w = param['screen_width']
    r = get_screen_rect(zone)
    move_x = mx
    move_y = my


    if r.width > w:
        dx = r.width - w

        if left > w / 2:
            move_x = move_x - 2

            if abs(move_x) > dx:
                move_x = dx * (-1)

        if left < w / 2:
            move_x = move_x + 2

            if move_x > 0:
                move_x = 0

    # if the height is greater than the default screen height
    if r.height > h:
        # total amount of height allowed to shift
        dy = r.height - h

        # If walking down and the top goes past 75 of screen
        if top > h / 2:
            move_y = move_y - 2

            # If move is more than boarder
            if abs(move_y) > dy:
                move_y = dy * (-1)

        # if walking up and the avatar goes above 25% of avail
        if top < h / 2:
            move_y = move_y + 2

            # Cannot pass 0
            if move_y > 0:
                move_y = 0

    return move_x, move_y


def get_game_clock():
    return pg.time.Clock()


def new_game():
    start = {'zone': 'world',
             'x': 49,
             'y': 138,
             'gold': 100,
             'event_num': 0,
             # Each playable char values, start with one char
             'char': [
                      {'name': 'Kralean',
                       'class': 'warrior_M',
                       'HP': 50,
                       'MP': 10,
                       'level': 1,
                       'exp': 0,
                       'gem':  {'name': None, 'idx': None},
                       'weapon': {'name': None, 'idx': None},
                       'head': {'name': None, 'idx': None},
                       'body': {'name': None, 'idx': None},
                       'arms': {'name': None, 'idx': None},
                       'legs': {'name': None, 'idx': None},
                       'gemlvl': {'Fire': 0, 'Water':0, 'Earth': 0,
                                  'Wind': 0, 'Nature': 0}
                      },
                     ],
             'not_char': [ # Characters not in menu
                          {'name': 'Melhay',
                           'class': 'warrior_M',
                           'HP': 50,
                           'MP': 10,
                           'level': 1,
                           'exp': 0,
                           'gem':  {'name': None, 'idx': None},
                           'weapon': {'name': None, 'idx': None},
                           'head': {'name': None, 'idx': None},
                           'body': {'name': None, 'idx': None},
                           'arms': {'name': None, 'idx': None},
                           'legs': {'name': None, 'idx': None},
                           'gemlvl': {'Fire': 0, 'Water':0, 'Earth': 0,
                                      'Wind': 0, 'Nature': 0}
                          },
                          {'name': 'Myhal',
                           'class': 'warrior_M',
                           'HP': 50,
                           'MP': 10,
                           'level': 1,
                           'exp': 0,
                           'gem':  {'name': None, 'idx': None},
                           'weapon': {'name': None, 'idx': None},
                           'head': {'name': None, 'idx': None},
                           'body': {'name': None, 'idx': None},
                           'arms': {'name': None, 'idx': None},
                           'legs': {'name': None, 'idx': None},
                           'gemlvl': {'Fire': 0, 'Water':0, 'Earth': 0,
                                      'Wind': 0, 'Nature': 0}
                          },
                         ],
             'items': [],
             'key_items': [],
             'quests': [],
             'mission': 18,
            }
    return start


def exp_to_level(lvl):
    if lvl == 99:
        return 1e24
    return int(500 * (lvl + (lvl - 1) * 1.5))


def calc_hero_att(a, st, d):
    """
    Atk and
    M. Att

    ATTACK + STR * 2 + DEX
    """
    der = int(a + st * 2 + d)
    if der > 9999:
        return 9999
    return der


def calc_hero_def(d, vt, c):
    """
    DEF and
    M. DEF

    d + vt * 2 + c * 2
    """
    der = int(d + vt * 2 + c * 2)
    if der > 9999:
        return 9999
    return der


def get_base_stats(char, level):
    x = {'warrior': {'base': {
                              'HP': 50,  # Health Points
                              'MP': 10,  # Magic Points
                              'STR': 5,  # Strength (p. att)
                              'END': 6,  # Endurance (p. def)
                              'DEX': 5,  # Dexterity (speed / agility)
                              'WSD': 4,  # Wisdom (m. def)
                              'INT': 3,  # Intelligence (m. att)
                              'CHR': 4,  # Charisma ( )
                             },
                     'incr': {
                              'HP': 2,      # Health Points
                              'MP': 1.7,    # Magic Points
                              'STR': 1.1,   # Strength (p. att)
                              'END': 1.15,  # Endurance (p. def)
                              'DEX': 1.05,  # Dexterity (speed / agility)
                              'WSD': 1.02,  # Wisdom (m. def)
                              'INT': 1,     # Intelligence (m. att)
                              'CHR': 1.04,  # Charisma ( )
                             }
                     },
        }
    y = {}
    for a in x[char]['base']:
        y[a] = int(x[char]['base'][a] + (level - 1) ** x[char]['incr'][a])
    return y


def load_shift_zone(r, shift_x, shift_y, tmp_x, tmp_y):
    param = params()
    h2 = param['screen_height'] / 2
    w2 = param['screen_width'] / 2

    shift_x -= tmp_x - w2
    shift_y -= tmp_y - h2

    if shift_x > 0:
        if r.width > w2 * 2:
            shift_x = 0
        else:
            shift_x = (w2 * 2 - r.width) / 2
    if shift_y > 0:
        if r.height > h2 * 2:
            shift_y = 0
        else:
            shift_y = (h2 * 2 - r.height) / 2
    if abs(shift_y) > r.height - h2:
        shift_y = (h2 * 2 - r.height) / 2

    return shift_x, shift_y


def get_item_list(ind=None):
    """
    """
    items = {'HP Potion': {'HP Potion': 2},
             'MP Potion': {'MP Potion': 2},
             'Cloth Armor': {'Cloth Armor': 8},
             'Wooden Armor': {'Wooden Armor': 8},
             'Leather Armor': {'Leather Armor': 8},
             'Cloth Cap': {'Cloth Cap': 8},
             'Wooden Cap': {'Wooden Cap': 8},
             'Leather Cap': {'Leather Cap': 8},
             'Ash Staff': {'Ash Staff': 8},
             'Leather Gloves': {'Leather Gloves': 8},
             'Tin Sword': {'Copper Sword': 8},
             'Straw Bow': {'Straw Bow': 8},
             'Bone Knife': {'Bone Knife': 8},
             'Fire Gem I': {'Fire Gem I': 1000},
             'Earth Gem I': {'Earth Gem I': 1000},
             'Water Gem I': {'Water Gem I': 1000},
             'Wind Gem I': {'Wind Gem I': 1000},
             'Nature Gem X': {'Nature Gem I': 1000},
            }
    
    if ind == None:
        return items
    return items[ind]


def get_gem_level(ind, name=None):
    gems = [ind + ' Gem I', ind + ' Gem II', ind + ' Gem III', ind + ' Gem IV', ind + ' Gem V',
            ind + ' Gem VI', ind + ' Gem VII', ind + ' Gem VIII', ind + ' Gem IX', ind + ' Gem X',
            ind + ' Gem XI', ind + ' Gem XII']
    if name is None:
        return gems
    for i in range(len(gems)):
        if gems[i] == name:
            return i+1
    return -1


def gem_spells(pts, ind=None):
    """
    """
    gems = {'Fire': [
                     {'name': 'Fire I', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Minor Fire Damage To Target'},
                     {'name': 'STR Boost I', 'spell': 0,
                      'cost': 35,
                      'desc': 'Gives Minor Bonus to STR'},
                     {'name': 'Status Bonus', 'spell': None,
                      'cost': 35,
                      'desc': 'Minor Increase To Base STR And INT'},
                     {'name': 'Fira I', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Minor Fire Damage To All'},
                     {'name': 'Fire II', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Moderate Fire Damage To Target'},
                     {'name': 'STR Boost II', 'spell': 0,
                      'cost': 35,
                      'desc': 'Gives Moderate Bonus to STR'},
                     {'name': 'Status Bonus', 'spell': None,
                      'cost': 35,
                      'desc': 'Moderate Increase To Base STR And INT'},
                     {'name': 'Fira II', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Moderate Fire Damage To All'},
                     {'name': 'Fire III', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Major Fire Damage To Target'},
                     {'name': 'STR Boost III', 'spell': 0,
                      'cost': 35,
                      'desc': 'Gives Major Bonus To STR'},
                     {'name': 'Status Bonus', 'spell': None,
                      'cost': 35,
                      'desc': 'Major Increase To Base STR And INT'},
                     {'name': 'Fira III', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Major Fire Damage To All'}
                    ],
            'Water': [
                     {'name': 'Water I', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Minor Water Damage To Target'},
                     {'name': 'CHR+ I', 'spell': 0,
                      'cost': 35,
                      'desc': 'Gives Minor Bonus to CHR'},
                     {'name': 'Status Bonus', 'spell': None,
                      'cost': 35,
                      'desc': 'Minor Increase To Base WSD And CHR'},
                     {'name': 'Watera I', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Minor Water Damage To All'},
                     {'name': 'Water II', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Moderate Water Damage To Target'},
                     {'name': 'CHR+ II', 'spell': 0,
                      'cost': 35,
                      'desc': 'Gives Moderate Bonus to CHR'},
                     {'name': 'Status Bonus', 'spell': None,
                      'cost': 35,
                      'desc': 'Moderate Increase To Base WSD And CHR'},
                     {'name': 'Watera II', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Moderate Water Damage To All'},
                     {'name': 'Water III', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Major Water Damage To Target'},
                     {'name': 'CHR+ III', 'spell': 0,
                      'cost': 35,
                      'desc': 'Gives Major Bonus To CHR'},
                     {'name': 'Status Bonus', 'spell': None,
                      'cost': 35,
                      'desc': 'Major Increase To Base WSD And CHR'},
                     {'name': 'Watera III', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Major Water Damage To All'}
                    ],
            'Earth': [
                     {'name': 'Earth I', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Minor Earth Damage To Target'},
                     {'name': 'END+ I', 'spell': 0,
                      'cost': 35,
                      'desc': 'Gives Minor Bonus to END'},
                     {'name': 'Status Bonus', 'spell': None,
                      'cost': 35,
                      'desc': 'Minor Increase To Base END And WSD'},
                     {'name': 'Earthra I', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Minor Earth Damage To All'},
                     {'name': 'Earth II', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Moderate Earth Damage To Target'},
                     {'name': 'END+ II', 'spell': 0,
                      'cost': 35,
                      'desc': 'Gives Moderate Bonus to END'},
                     {'name': 'Status Bonus', 'spell': None,
                      'cost': 35,
                      'desc': 'Moderate Increase To Base END And WSD'},
                     {'name': 'Earthra II', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Moderate Earth Damage To All'},
                     {'name': 'Earth III', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Major Earth Damage To Target'},
                     {'name': 'END+ III', 'spell': 0,
                      'cost': 35,
                      'desc': 'Gives Major Bonus To END'},
                     {'name': 'Status Bonus', 'spell': None,
                      'cost': 35,
                      'desc': 'Major Increase To Base END And WSD'},
                     {'name': 'Earthra III', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Major Earth Damage To All'}
            ],
            'Wind': [
                     {'name': 'Wind I', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Minor Wind Damage To Target'},
                     {'name': 'DEX+ I', 'spell': 0,
                      'cost': 35,
                      'desc': 'Gives Minor Bonus to DEX'},
                     {'name': 'Status Bonus', 'spell': None,
                      'cost': 35,
                      'desc': 'Minor Increase To Base DEX And CHR'},
                     {'name': 'Windra I', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Minor Wind Damage To All'},
                     {'name': 'Wind II', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Moderate Wind Damage To Target'},
                     {'name': 'DEX+ II', 'spell': 0,
                      'cost': 35,
                      'desc': 'Gives Moderate Bonus to DEX'},
                     {'name': 'Status Bonus', 'spell': None,
                      'cost': 35,
                      'desc': 'Moderate Increase To Base DEX And CHR'},
                     {'name': 'Windra II', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Moderate Wind Damage To All'},
                     {'name': 'Wind III', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Major Wind Damage To Target'},
                     {'name': 'DEX+ III', 'spell': 0,
                      'cost': 35,
                      'desc': 'Gives Major Bonus To DEX'},
                     {'name': 'Status Bonus', 'spell': None,
                      'cost': 35,
                      'desc': 'Major Increase To Base DEX And CHR'},
                     {'name': 'Windra III', 'spell': 0,
                      'cost': 35,
                      'desc': 'Deals Major Wind Damage To All'}
            ],
            'Nature': [
                     {'name': 'Heal', 'spell': 0,
                      'cost': 35,
                      'desc': 'Heals A Minor Amount Of Heath To Target'},
                     {'name': 'Wisdom Boost', 'spell': 0,
                      'cost': 35,
                      'desc': 'Gives Minor Bonus to WSD'},
                     {'name': 'Status Bonus', 'spell': None,
                      'cost': 35,
                      'desc': 'Minor Increase To Base WSD And CHR'},
                     {'name': 'Healra', 'spell': 0,
                      'cost': 35,
                      'desc': 'Heals A Minor Amount Of Heath To All'},
                     {'name': 'Heal II', 'spell': 0,
                      'cost': 35,
                      'desc': 'Heals A Moderate Amount Of Heath To Target'},
                     {'name': 'Wisdom Boost II', 'spell': 0,
                      'cost': 35,
                      'desc': 'Gives Moderate Bonus to WSD'},
                     {'name': 'Status Bonus', 'spell': None,
                      'cost': 35,
                      'desc': 'Moderate Increase To Base WSD And CHR'},
                     {'name': 'Rise', 'spell': 0,
                      'cost': 35,
                      'desc': 'Revives a KO Char. to 50% HP and MP'},
                     {'name': 'Heal III', 'spell': 0,
                      'cost': 35,
                      'desc': 'Heals A Major Amount Of Heath To Target'},
                     {'name': 'Wisdom Boost III', 'spell': 0,
                      'cost': 35,
                      'desc': 'Gives Major Bonus To WSD'},
                     {'name': 'Status Bonus', 'spell': None,
                      'cost': 35,
                      'desc': 'Major Increase To Base WSD And CHR'},
                     {'name': 'Healra II', 'spell': 0,
                      'cost': 35,
                      'desc': 'Heals A Moderate Amount Of Heath To All'}
            ]}
    if pts < 10:
        return gems[ind][:1]
    if pts < 30:
        return gems[ind][:2]
    if pts < 80:
        return gems[ind][:3]
    if pts < 180:
        return gems[ind][:4]
    if pts < 380:
        return gems[ind][:5]
    if pts < 880:
        return gems[ind][:6]
    if pts < 1880:
        return gems[ind][:7]
    if pts < 3880:
        return gems[ind][:8]
    if pts < 8880:
        return gems[ind][:9]
    if pts < 18880:
        return gems[ind][:10]
    if pts < 38880:
        return gems[ind][:11]
    return gems[ind]
