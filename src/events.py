"""Event's module

All the game events should take place here
"""
import os
import numpy as np
import pygame as pg
import src.dialog as dialog
import src.settings as settings

def reoccuring_events(zone):
    """List of events that can reoccur anytime

    structure
    {'zone': {}
    """
    shop_items = settings.get_item_list()
    e = {'hero_house': [{'type': 'dialog',
                         'action': [{'text': {'char': dialog.get_char_img('warrior_M'),
                                              'content': get_reoccurring_dialog(0),
                                             }
                                    },
                                    {'repeat'},
                                   ],
                         'area': [4, 6, 64, 64] # Left (32px), Top (32px), Width (px), Height (px)
                         },
                         {'type': 'rest',
                          'action': [{'rest': {'cost': 0,
                                              }
                                     },
                                     {'repeat'},
                                    ],
                          'area': [4, 3, 32, 32]
                         },

                       ],
         'home_village': [{'action': [{'text': {'char': '',
                                                'content': get_reoccurring_dialog(3),
                                               },
                                      },
                                      {'repeat'}
                                     ],
                           'area': [32, 6, 64, 64]
                          },
                         ],
         'home_vill_shops': [{'type': 'shop',
                              'action': [{'text': {'char': '',
                                                   'content': get_reoccurring_dialog(1),
                                                  },
                                         },
                                         {'shop': [shop_items['HP Potion'],   # Item: cost
                                                   shop_items['MP Potion'],
                                                   shop_items['Earth Gem I'],
                                                   shop_items['Fire Gem I'],
                                                   shop_items['Water Gem I'],
                                                   shop_items['Wind Gem I'],
                                                   shop_items['Nature Gem X'],
                                                   {'Exit': 0}
                                                  ],
                                         },
                                         {'repeat'}
                                        ],
                              'area': [11, 4, 92, 32]
                             },
                             {'type': 'shop',
                              'action': [{'text': {'char': '',
                                                   'content': get_reoccurring_dialog(2),
                                                  },
                                         },
                                         {'shop': [shop_items['HP Potion'],   # Item: cost
                                                   shop_items['MP Potion'],
                                                   shop_items['Cloth Armor'],
                                                   shop_items['Wooden Armor'],
                                                   shop_items['Leather Armor'],
                                                   shop_items['Cloth Cap'],
                                                   shop_items['Wooden Cap'],
                                                   shop_items['Leather Cap'],
                                                   {'Exit': 0}
                                                  ],
                                         },
                                         {'repeat'},
                                        ],
                              'area': [2, 4, 92, 32]
                             },
                            ],
         'friends_house': [
                          ],
         'elders_house': [
                         ],
         'world': [
                  ],
         'BLANK': [
                  ],
         'cave_no_gem': [# Add healing at "fountain"
                        ],
         'quiet_forest': [
                         ],
        }
    return e[zone]


def get_reoccurring_dialog(x):
    """
    Notes
    -----
    Use `()` for inner monolog
    Always use double quotes
    """
    z = ["(I've got a long day ahead of me...)",         # 0
         "We many not have a large variety, but we have useful items.",
         "Wearing simple armor is better than running into battle wearing nothing but your knickers.",
         "This year's harvest should be plentiful. The elders will be pleased with the crop yield.",
        ]
    return z[x]


def rest(surface, font, pay=0, imgs_to_blit=[], select=0):
    for img in imgs_to_blit:
        img.draw(surface)

    cwd = os.getcwd()
    params = settings.params()

    gt = "Would you like to rest?"
    if pay > 0:
        gt = "It costs " + pay + " to rest here. Would you like to rest?"


    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck = pg.transform.scale(bck, (params['screen_width'], 200))

    # Display at bottom
    surface.blit(bck, (0, (params['screen_height'] - 200)), bck.get_rect())
    x = 50
    y = params['screen_height'] - 200 + 15
    z = 0

    gt = font.render(gt, 0, (0, 0, 0))
    yes = font.render("Yes", 0, (0, 0, 0))
    no = font.render("No", 0, (0, 0, 0))
    surface.blit(gt, (x, y))
    x = gt.get_size()[0]
    LH = yes.get_size()[1]
    surface.blit(yes, (x, int(y + 1.5 * LH)))
    surface.blit(no, (x, int(y + 3.0 * LH)))

    # Pointer Mechanics
    pointer = pg.image.load(cwd + '/imgs/textbox/arrowBrown_right.png')
    pointer.set_colorkey((255, 255, 255))
    pointer = pg.transform.scale(pointer, (28, 28))
    s_x = gt.get_size()[0] - 40
    s_y = y + 1.5 * LH + select * 1.5 * LH
    surface.blit(pointer, (s_x, s_y))

    pg.display.flip()
    return select


def player_rest(gp, zp, cost=0, itb=[]):
    """Removing from main loop
    """
    params = settings.params()

    # zp = zone parameters
    zone = zp['zone']
    zone_name = zp['name']
    shift_x = zp['x']
    shift_y = zp['y']

    # gp game parameters
    screen = gp['screen']
    font = gp['font']
    clock = gp['clock']
    music = gp['music']
    player = gp['player']
    DIR = gp['DIR']

    rest(screen, font, pay=cost, imgs_to_blit=itb)
    reading = True
    opt = 0
    while reading:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                reading = False
                pg.quit()
                break
            elif e.type == pg.KEYDOWN:
                if e.key in [pg.K_RETURN, pg.K_SPACE]:
                    # Exchange Money, Rest if True
                    if opt == 0:
                        music.stop_music()
                        music.play_music(music.sound_list('rest'), until=1)
                    alpha = 255
                    while alpha > 0 and opt == 0:
                        screen.fill((0, 0, 0))
                        screen.blit(zone, (shift_x, shift_y), zone.get_rect())
                        moving = False
                        player.get_image(DIR, moving).get_rect()
                        player.move(0, 0, stop=True)
                        zone.set_alpha(int(alpha))
                        alpha -= 1.5
                        clock.tick(params['frames_per_second'])
                        pg.display.flip()
                    zone.set_alpha(255)
                    reading = False
                    music.play_music(music.music_list(zone_name))
                    break
                if e.key == pg.K_DOWN:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt += 1
                    if opt == 2:
                        opt = 0
                if e.key == pg.K_UP:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt -= 1
                    if opt == -1:
                        opt = 1
                rest(screen, font, pay=cost, imgs_to_blit=itb, select=opt)
        clock.tick(params['frames_per_second'])


def restore_health(game):
    """Restores HP and MP for all party members to full based on their level

    Parameters
    ----------
    game: dict
    """
    # For each class, easier than by name at the moment

    heros = game['char']

    for i in range(len(heros)):
        # Char Job
        jb = heros[i]['class']
        if '_' in jb:
            jb = heros[i]['class'].split('_')[0]
        base = settings.get_base_stats(jb, heros[i]['level'])
        game['char'][i]['HP'] = base['HP']
        game['char'][i]['MP'] = base['MP']
    return game


def player_shop(gp, zp, shop_items, itb=[]):
    """
    """
    params = settings.params()

    # zp = zone parameters
    zone = zp['zone']
    zone_name = zp['name']
    shift_x = zp['x']
    shift_y = zp['y']

    # gp game parameters
    screen = gp['screen']
    font = gp['font']
    clock = gp['clock']
    player = gp['player']
    DIR = gp['DIR']
    music = gp['music']
    user_items = gp['items']
    heros = gp['char']

    screen.fill((0, 0, 0))
    screen.blit(zone, (shift_x, shift_y), zone.get_rect())
    shop_buy_or_sell(screen, font, shop_items, imgs_to_blit=itb)
    reading = True
    opt = 0
    while reading:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                reading = False
                pg.quit()
                break
            elif e.type == pg.KEYDOWN:
                if e.key in [pg.K_RETURN, pg.K_SPACE]:
                    # Buy
                    if opt == 0:
                        buy_item = ''
                        idx = 0
                        while 'Exit' not in buy_item:
                            buy_item, idx = shop_display_items(gp, shop_items, select=idx)
                            # Perform `buy` action
                            if 'Exit' not in buy_item:
                                for ni in shop_items[idx]:
                                    value = shop_items[idx][ni]
                                if gp['gold'] >= value:
                                    music.play_sound(music.sound_list('buy_sell'), num=1)

                                    # Item list updates, gold does not...
                                    user_items.append(ni)
                                    gp['gold'] = gp['gold'] - value
                                    gp['items'] = user_items
                        screen.fill((0, 0, 0))
                        screen.blit(zone, (shift_x, shift_y), zone.get_rect())
                        pg.display.flip()
                    # Sell
                    if opt == 1:
                        sell_item = ''
                        idx = 0
                        while 'Exit' not in sell_item:
                            sell_item, idx = shop_display_user_items(gp, select=idx)
                            if 'Exit' not in sell_item:
                                music.play_sound(music.sound_list('buy_sell'), num=1)

                                tidx = idx
                                for i in range(idx):
                                    a = user_items[i]
                                    if get_items_for_use(ind=a)['type'] is 'Item':
                                        tidx -= 1
                                # if item equipped, remove it
                                equipped = []
                                ps = ['weapon', 'head', 'body', 'legs']
                                for i in range(len(heros)):
                                    for j in range(len(ps)):
                                        if heros[i][ps[j]]['idx'] is not None:
                                            if heros[i][ps[j]]['idx'] == tidx:
                                                heros[i][ps[j]]['idx'] = None
                                                heros[i][ps[j]]['name'] = None

                                # add gold, remove item
                                gp['gold'] = gp['gold'] + settings.get_item_list(user_items[idx])[user_items[idx]]/2
                                user_items.pop(idx)
                                # update list for pop reasons
                                gp['items'] = user_items


                        screen.fill((0, 0, 0))
                        screen.blit(zone, (shift_x, shift_y), zone.get_rect())
                        pg.display.flip()
                    # Exit
                    if opt == 2:
                        reading = False
                        # Return gold because item does not update?
                        return gp['gold']
                        break
                if e.key == pg.K_DOWN:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt += 1
                    if opt == 3:
                        opt = 0
                if e.key == pg.K_UP:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt -= 1
                    if opt == -1:
                        opt = 2
                shop_buy_or_sell(screen, font, shop_items, imgs_to_blit=itb, select=opt)
        clock.tick(params['frames_per_second'])


def shop_display_items(gp, items, select=0):
    """Black background with 1/3 screen (right side) filled with item list
    """
    cwd = os.getcwd()
    params = settings.params()

    # gp game parameters
    surface = gp['screen']
    font = gp['font']
    clock = gp['clock']
    music = gp['music']
    user_items = gp['items']

    # Black screen
    pg.draw.rect(surface, (0, 0, 0), (0, 0, params['screen_width'], params['screen_height']))

    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [500, params['screen_height']]
    bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))

    surface.blit(bck, (params['screen_width'] - bck_size[0], 0), bck.get_rect())

    FS = font.render('TMP', 0, (0, 0, 0)).get_size()

    # max_x
    mx = 0
    item_list = []
    i = 0
    # I'm sure there's a smarter way to do this....
    for j in range(len(items)):
        for a in items[j]:
            cost = items[j][a]
            if cost == 0:
                cost = ''
        i += 1
        y = FS[1] * 1.5 * i
        item_list.append({a:{'font': font.render(a, 0, (0, 0, 0)),
                             'y': y,
                             'price': font.render(str(cost), 0, (0, 0, 0)),
                            }})
        xl = 40 + item_list[-1][a]['font'].get_size()[0]
        xl += item_list[-1][a]['price'].get_size()[0]
        if xl > mx:
            mx = xl

    user_items_list = []
    for j in range(len(user_items)):
        y = FS[1] * 1.5 * (j + 1)
        user_items_list.append({user_items[j]: {'font': font.render(user_items[j], 0, (0, 0, 0)),
                                                'y': y}})

    msel = 0
    msely = 0
    shop_select_items(surface, font, item_list, user_items_list, mx, gp['gold'], select=select, msel=msel)
    reading = True
    opt = select
    while reading:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                reading = False
                pg.quit()
                break
            elif e.type == pg.KEYDOWN:
                # Buy / exchange funds
                if e.key in [pg.K_RETURN]:
                    if msel == 0:
                        return item_list[opt], opt
                if e.key == pg.K_DOWN:
                    music.play_sound(music.sound_list('menu'), num=1)
                    if msel == 0:
                        opt += 1
                        if opt == i:
                            opt = 0
                    else:
                        msely += 1
                        if msely == len(user_items_list):
                            msely = 0
                if e.key == pg.K_UP:
                    music.play_sound(music.sound_list('menu'), num=1)
                    if msel == 0:
                        opt -= 1
                        if opt == -1:
                            opt = i-1
                    else:
                        msely -= 1
                        if msely == -1:
                            msely = len(user_items_list) - 1
                if len(user_items_list) > 0:
                    if e.key == pg.K_LEFT:
                        msel += 1
                        if msel > 1:
                            msel = 0
                    if e.key == pg.K_RIGHT:
                        msel -= 1
                        if msel < 0:
                            msel = 1
                shop_select_items(surface, font, item_list, user_items_list, mx, gp['gold'],
                                  select=opt, msel=msel, msely=msely)
        clock.tick(params['frames_per_second'])


def shop_select_items(surface, font, item_list, user_items, mx, wallet, select=0, msel=0, msely=0):
    """ Allows the user to scroll up and down an item list

    Parameters
    ----------
    item_list
        dict containing shop items for sale and their price
    user_items
        dict containing items in a user`s inventory and the order
    mx: int
        maximum x 
    wallet: int
        current gold available
    select: int
        current position of pointer
    msel: int
        menu the pointer is at
    """
    cwd = os.getcwd()
    params = settings.params()

    # Black screen
    pg.draw.rect(surface, (0, 0, 0), (0, 0, params['screen_width'], params['screen_height']))

    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [400, params['screen_height'] - 100]
    item_bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))

    # Shop List Background
    surface.blit(item_bck, (params['screen_width'] - bck_size[0], 0), item_bck.get_rect())

    bck_size = [400, params['screen_height']]
    inven_bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))
    # Item List Background
    surface.blit(inven_bck, (0, 0), inven_bck.get_rect())

    # List gold
    bck_size = [400, 100]
    gold_bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))
    surface.blit(gold_bck, (params['screen_width']-bck_size[0], params['screen_height']-bck_size[1]), gold_bck.get_rect())

    FS = font.render('TMP', 0, (0, 0, 0)).get_size()
    for i in range(len(item_list)):
        for a in item_list[i]:
            a_font = item_list[i][a]['font']
            a_y = item_list[i][a]['y']
            a_price = item_list[i][a]['price']

            if i == select:
                if a == 'Exit':
                    desc_txt = font.render('Exit', 0, (0, 0, 0))
                else:
                    desc_txt = font.render(get_items_for_use(ind=a)['desc'], 0, (0, 0, 0))
                

        # Display the item
        surface.blit(a_font, (params['screen_width'] - mx, a_y))

        # Display the price
        px = params['screen_width'] - a_price.get_size()[0] - 15
        surface.blit(a_price, (px, a_y))


    # User inventory max x length
    mx2 = 0
    for i in range(len(user_items)):
        for a in user_items[i]:
            if user_items[i][a]['font'].get_size()[0] > mx2:
                mx2 = user_items[i][a]['font'].get_size()[0]

    mx_show_items = 15
    start = 0
    stop = len(user_items)
    # if the stop point is greater than the maximum allowed displayed
    if stop > mx_show_items:
        # if the user cursur is more than the last position
        if msely + 1 >= mx_show_items:
            start = msely - mx_show_items + 1
            stop = msely + 1
        else:
            stop = mx_show_items

    for i in range(start, stop):
        for a in user_items[i]:
            a_font = user_items[i][a]['font']
            a_y = user_items[i][a]['y']
            if len(user_items) > mx_show_items:
                a_y = (i - start + 1) * FS[1] * 1.5
        surface.blit(a_font, (bck_size[0] - mx2 - 30, a_y))

    gf = font.render('Gold: ' + str(wallet), 0, (0, 0, 0))
    gx = params['screen_width'] - gf.get_size()[0] - 30
    gy = params['screen_height'] - 50
    surface.blit(gf, (gx, gy))

    # Pointer
    pointer = pg.image.load(cwd + '/imgs/textbox/arrowBrown_right.png')
    pointer.set_colorkey((255, 255, 255))
    pointer = pg.transform.scale(pointer, (28, 28))
    s_x = params['screen_width'] - mx - 50
    s_y = (select + 1) * 1.5 * FS[1]
    if msel > 0:
        s_x = 100
        if msely + 1 > mx_show_items:
            msely = mx_show_items - 1
        s_y = (msely + 1) * 1.5 * FS[1]
    surface.blit(pointer, (s_x, s_y))


    # Item description between menus
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [480, 240]
    desc_bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))
    surface.blit(desc_bck, (400, 0), desc_bck.get_rect())

    surface.blit(desc_txt, (430, 18))

    pg.display.flip()


def shop_buy_or_sell(surface, font, items, imgs_to_blit=[], select=0):
    """Prompt player if they want to buy or sell.
    
    Buy -> list of available items
    Sell -> go to inventory
    """
    for img in imgs_to_blit:
        img.draw(surface)

    cwd = os.getcwd()
    params = settings.params()

    buy = font.render('Buy', 0, (0, 0, 0))
    sell = font.render('Sell', 0, (0, 0, 0))
    ex = font.render('Exit', 0, (0, 0, 0))

    LH = buy.get_size()[1]
    LW = sell.get_size()[0]

    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [200, 150]
    bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))

    # Display bottom right
    surface.blit(bck, (params['screen_width'] - bck_size[0], params['screen_height'] - bck_size[1]),
                 bck.get_rect())
    x = params['screen_width'] - LW - 15
    y = params['screen_height'] - bck_size[1] + 15
    surface.blit(buy, (x, y))
    surface.blit(sell, (x, y + 1.5 * LH))
    surface.blit(ex, (x, y + 3.0 * LH))

    # Pointer
    pointer = pg.image.load(cwd + '/imgs/textbox/arrowBrown_right.png')
    pointer.set_colorkey((255, 255, 255))
    pointer = pg.transform.scale(pointer, (28, 28))
    s_x = x - 50
    s_y = y + select * 1.5 * LH
    surface.blit(pointer, (s_x, s_y))

    pg.display.flip()
    return select


def shop_display_user_items(gp, select=0):
    cwd = os.getcwd()
    params = settings.params()

    # gp game parameters
    surface = gp['screen']
    font = gp['font']
    clock = gp['clock']
    music = gp['music']
    user_items = gp['items']
    heros = gp['char']

    # Black screen
    pg.draw.rect(surface, (0, 0, 0), (0, 0, params['screen_width'], params['screen_height']))

    FS = font.render('T', 0, (0, 0, 0)).get_size()

    # Item List Background
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [500, params['screen_height']]
    bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))

    surface.blit(bck, (params['screen_width'] - bck_size[0], 0), bck.get_rect())

    # get equipped items index
    equipped = []
    ps = ['weapon', 'head', 'body', 'legs', 'gem']
    for i in range(len(heros)):
        for j in range(len(ps)):
            if heros[i][ps[j]]['idx'] is not None:
                equipped.append(heros[i][ps[j]]['idx'])

    equipped.sort()
    start = 0
    stop = len(equipped)
    for i in range(len(user_items)):
        a = user_items[i]
        if get_items_for_use(ind=a)['type'] is 'Equipment':
            start += 1
            continue
        if start > stop:
            continue
        for j in range(start, stop):
            equipped[j] += 1

    # To Be Displayed
    user_items_list = []
    mx = 0
    for j in range(len(user_items)):
        y = FS[1] * 1.5 * (j + 1)
        price = settings.get_item_list(ind=user_items[j])[user_items[j]]
        color = (0, 0, 0)
        if j in equipped:
            color = (0, 0, 255)
        user_items_list.append({user_items[j]: {'font': font.render(user_items[j], 0, color),
                                                'y': y,
                                                'price': font.render(str(price/2), 0, (0, 0, 0))
                                                }})
        xl = 40 + user_items_list[-1][user_items[j]]['font'].get_size()[0]
        xl += user_items_list[-1][user_items[j]]['price'].get_size()[0]
        if xl > mx:
            mx = xl
    # Add exit to list
    y = FS[1] * 1.5 * (len(user_items) + 1)
    user_items_list.append({'Exit': {'font': font.render('Exit', 0, (0, 0, 0)),
                                            'y': y,
                                            'price': font.render('', 0, (0, 0, 0))
                                            }})
    if mx == 0:
        mx = font.render('Exit', 0, (0, 0, 0)).get_size()[0] + 30
    shop_select_user_items(surface, font, user_items_list, mx, gp['gold'], select=select)
    reading = True
    opt = select
    while reading:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                reading = False
                pg.quit()
                break
            elif e.type == pg.KEYDOWN:
                # Return value
                if e.key == pg.K_q:
                    # Return exit
                    return user_items_list[-1], len(user_items_list) - 1
                if e.key in [pg.K_RETURN]:
                    return user_items_list[opt], opt
                # Display stuff pointer
                if e.key == pg.K_DOWN:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt += 1
                    if opt == len(user_items_list):
                        opt = 0
                if e.key == pg.K_UP:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt -= 1
                    if opt == -1:
                        opt = len(user_items_list) - 1
                shop_select_user_items(surface, font, user_items_list, mx, gp['gold'], select=opt)
        clock.tick(params['frames_per_second'])
    return


def shop_select_user_items(surface, font, user_items, mx, wallet, select=0):
    """
    """
    cwd = os.getcwd()
    params = settings.params()

    # Black screen
    pg.draw.rect(surface, (0, 0, 0), (0, 0, params['screen_width'], params['screen_height']))

    # Item List Background
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [400, params['screen_height'] - 100]
    item_bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))

    surface.blit(item_bck, (params['screen_width'] - bck_size[0], 0), item_bck.get_rect())

    # List gold
    bck_size = [400, 100]
    gold_bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))
    surface.blit(gold_bck, (params['screen_width']-bck_size[0], params['screen_height']-bck_size[1]), gold_bck.get_rect())

    gf = font.render('Gold: ' + str(wallet), 0, (0, 0, 0))
    gx = params['screen_width'] - gf.get_size()[0] - 30
    gy = params['screen_height'] - 50
    surface.blit(gf, (gx, gy))

    FS = font.render('TMP', 0, (0, 0, 0)).get_size()

    mx_show_items = 13
    start = 0
    stop = len(user_items)
    # if the stop point is greater than the maximum allowed displayed
    if stop > mx_show_items:
        # if the user cursur is more than the last position
        if select + 1 >= mx_show_items:
            start = select - mx_show_items + 1
            stop = select + 1
        else:
            stop = mx_show_items

    for i in range(start, stop):
        for a in user_items[i]:
            a_font = user_items[i][a]['font']
            a_y = user_items[i][a]['y']
        #   a_x = params['screen_width'] - bck_size[0] - mx - 30
            a_price = user_items[i][a]['price']
            if len(user_items) > mx_show_items:
                a_y = (i - start + 1) * FS[1] * 1.5
                # Display the item
        surface.blit(a_font, (params['screen_width'] - mx, a_y))
        px = params['screen_width'] - a_price.get_size()[0] - 15
        surface.blit(a_price, (px, a_y))
        #surface.blit(a_font, (a_x, a_y))

    # Pointer
    pointer = pg.image.load(cwd + '/imgs/textbox/arrowBrown_right.png')
    pointer.set_colorkey((255, 255, 255))
    pointer = pg.transform.scale(pointer, (28, 28))
    s_x = params['screen_width'] - mx - 50
    s_y = (select + 1) * 1.5 * FS[1]
    if select + 1 > mx_show_items:
        select = mx_show_items - 1
    s_y = (select + 1) * 1.5 * FS[1]
    surface.blit(pointer, (s_x, s_y))

    pg.display.flip()


def get_items_for_use(ind=None):
    """
    """
    items = {'HP Potion': {'desc': 'Recover 50 HP',
                           'type': 'Item',
                           'action': give_player_item,
                           'stat': 'HP',
                           'amount': 50},
             'MP Potion': {'desc': 'Recover 10 MP',
                           'type': 'Item',
                           'action': give_player_item,
                           'stat': 'MP',
                           'amount': 10},
             'Cloth Armor': {'desc': 'Light Armor, DEF:1',
                             'type': 'Equipment'},
             'Wooden Armor': {'desc': 'Heavy Armor, DEF:1',
                              'type': 'Equipment'},
             'Leather Armor': {'desc': 'Medium Armor, DEF:1',
                               'type': 'Equipment'},
             'Tin Sword': {'desc': 'Heavy Weapon, END:1 ATT+2',
                           'type': 'Equipment'},
             'Bone Knife': {'desc': 'Medium Weapon, END:1 ATT+2',
                            'type': 'Equipment'},
             'Ash Staff': {'desc': 'Light Weapon, END:1 MATK+1',
                           'type': 'Equipment'},
             'Leather Gloves': {'desc': 'Melee Weapon, STR:1 ATT+1',
                                'type': 'Equipment'},
             'Cloth Cap': {'desc': 'Light Armor, DEF:1',
                             'type': 'Equipment'},
             'Wooden Cap': {'desc': 'Heavy Armor, DEF:1',
                              'type': 'Equipment'},
             'Leather Cap': {'desc': 'Medium Armor, DEF:1',
                               'type': 'Equipment'},
             'Fire Gem I': {'desc': 'Grade I Fire Gem',
                            'type': 'Equipment'},
             'Earth Gem I': {'desc': 'Grade I Earth Gem',
                             'type': 'Equipment'},
             'Water Gem I': {'desc': 'Grade I Water Gem',
                             'type': 'Equipment'},
             'Wind Gem I': {'desc': 'Grade I Wind Gem',
                            'type': 'Equipment'},
             'Nature Gem X': {'desc': 'Grade I Nature Gem',
                              'type': 'Equipment'},
            }
    if ind == None:
        return items
    return items[ind]


def get_equipment_for_use(ind=None):
    """
    """
    items = {'Tin Sword': {'inc': {'END': 1},
                           'type': 'Weapon',
                           'bat': {'ATT': 2},
                           'class': 'heavy'},
            'Bone Knife': {'inc': {'END': 1},
                           'type': 'Weapon',
                           'bat': {'ATT': 2},
                           'class': 'medium'},
            'Ash Staff': {'inc': {'END': 1},
                          'type': 'Weapon',
                          'bat': {'MATK': 1},
                          'class': 'light'},
            'Leather Gloves': {'inc': {'STR': 1},
                               'type': 'Weapon',
                               'bat': {'ATT': 1},
                               'class': 'melee'},
             'Cloth Armor': {'inc': {'END': 1},
                             'type': 'body',
                             'bat': {'DEF': 1},
                             'class': 'light'},
             'Wooden Armor': {'inc': {'END': 1},
                              'type': 'body',
                              'bat': {'DEF': 3},
                              'class': 'heavy'},
             'Leather Armor': {'inc': {'END': 2},
                               'type': 'body',
                               'bat': {'DEF': 2},
                               'class': 'medium'},
             'Cloth Cap': {'inc': {'END': 1},
                           'type': 'head',
                           'bat': {'DEF': 1},
                           'class': 'light'},
             'Wooden Cap': {'inc': {'END': 1},
                            'type': 'head',
                            'bat': {'DEF': 2},
                            'class': 'heavy'},
             'Leather Cap': {'inc': {'END': 2},
                             'type': 'head',
                             'bat': {'DEF': 1},
                             'class': 'medium'},
             'Fire Gem I': {'inc': None,
                            'type': 'gem',
                            'bat': None,
                            'class': 'Fire'},
             'Earth Gem I': {'inc': None,
                             'type': 'gem',
                             'bat': None,
                             'class': 'Earth'},
             'Water Gem I': {'inc': None,
                             'type': 'gem',
                             'bat': None,
                             'class': 'Water'},
             'Wind Gem I': {'inc': None,
                            'type': 'gem',
                            'bat': None,
                            'class': 'Wind'},
             'Nature Gem X': {'inc': None,
                            'type': 'gem',
                            'bat': None,
                            'class': 'Nature'},
            }
    if ind == None:
        return items
    return items[ind]


def give_player_item(gp, item, select):
    """Change the HP or MP (stats) of a player (select) by a set
    amount (delta)
    """
    # Get hero list
    heros = gp['char'][select]

    # Get limits
    jb = heros['class']
    if '_' in jb:
        jb = heros['class'].split('_')[0]
    base = settings.get_base_stats(jb, heros['level'])
    hp_lim = base['HP']
    mp_lim = base['MP']

    # Get item stats
    stat = item['stat']
    delta = item['amount']

    # Increase MP
    if stat == 'MP':
        heros['MP'] += delta
        if heros['MP'] > mp_lim:
            heros['MP'] = mp_lim

    # Increase HP (only if hp > 0)
    if stat == 'HP' and heros['HP'] > 0:
        heros['HP'] += delta
        if heros['HP'] > hp_lim:
            heros['HP'] = hp_lim

    # RISE revives a player
    if stat == 'RISE' and heros['HP'] == 0: 
        heros['HP'] = int(float(hp_lim) * 0.5)
    return heros

