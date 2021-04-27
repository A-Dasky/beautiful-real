import os
import numpy as np
import pygame as pg
import src.settings as settings
import src.events as ge
import src.dialog as dialog

def show_menu(gp, select=0):
    """

    Menu options
    ------------
    inventory
    equipment (currently in inventory, equip / unequip)
    gems (currently in inventory, equip / unequip)
    spells
    stats
    save
    exit

    display gold
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

    # Get font height
    FS = font.render('T', 0, (0, 0, 0)).get_size()


    # To Be Displayed
    menu_list = []
    mx = 0
    menu_opts = menu_options()
    for j in range(len(menu_opts)):
        y = FS[1] * 1.5 * (j + 1)
        menu_list.append({menu_opts[j]: {'font': font.render(menu_opts[j], 0, (0, 0, 0)),
                                                'y': y
                                        }})
        xl = 40 + menu_list[-1][menu_opts[j]]['font'].get_size()[0]
        if xl > mx:
            mx = xl
    # Add exit to list
    y = FS[1] * 1.5 * (len(menu_opts) + 1)
    menu_list.append({'Exit': {'font': font.render('Exit', 0, (0, 0, 0)),
                               'y': y
                              }})

    display_menu(gp, menu_list, mx, select=0)
    reading = True
    opt = select
    while reading:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                reading = False
                pg.quit()
                break
            elif e.type == pg.KEYDOWN:
                if e.key in [pg.K_RETURN]:
                    if 'Items' in menu_list[opt]:
                        display_menu_items(gp)
                    if 'Equipment' in menu_list[opt]:
                        display_menu_equipment(gp)
                    if 'Status' in menu_list[opt]:
                        display_menu_status(gp)
                    if 'Gems' in menu_list[opt]:
                        display_menu_gem(gp)
                    if 'Magic' in menu_list[opt]:
                        display_menu_magic(gp)
                    if 'Exit' in menu_list[opt]:
                        return
                if e.key == pg.K_q:
                    return
                if e.key == pg.K_UP:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt -= 1
                    if opt == -1:
                        opt = len(menu_list) - 1
                if e.key == pg.K_DOWN:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt += 1
                    if opt == len(menu_list):
                        opt = 0
                display_menu(gp, menu_list, mx, select=opt)
        clock.tick(params['frames_per_second'])


def display_menu(gp, menu_list, mx, select=0):
    """Display the menu
    """
    cwd = os.getcwd()
    params = settings.params()

    # gp game parameters
    surface = gp['screen']
    font = gp['font']
    clock = gp['clock']
    music = gp['music']
    user_items = gp['items']
    wallet = gp['gold']

    # Black screen
    pg.draw.rect(surface, (0, 0, 0), (0, 0, params['screen_width'], params['screen_height']))

    # Item List Background
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [400, params['screen_height'] - 100]
    menu_bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))

    surface.blit(menu_bck, (params['screen_width'] - bck_size[0], 0), menu_bck.get_rect())

    # List gold
    bck_size = [400, 100]
    gold_bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))
    surface.blit(gold_bck, (params['screen_width']-bck_size[0], params['screen_height']-bck_size[1]), gold_bck.get_rect())

    gf = font.render('Gold: ' + str(wallet), 0, (0, 0, 0))
    gx = params['screen_width'] - gf.get_size()[0] - 30
    gy = params['screen_height'] - 50
    surface.blit(gf, (gx, gy))

    FS = font.render('TMP', 0, (0, 0, 0)).get_size()

    for i in range(len(menu_list)):
        for a in menu_list[i]:
            a_font = menu_list[i][a]['font']
            a_y = menu_list[i][a]['y']
                # Display the item
        surface.blit(a_font, (params['screen_width'] - mx, a_y))


    # Pointer
    pointer = pg.image.load(cwd + '/imgs/textbox/arrowBrown_right.png')
    pointer.set_colorkey((255, 255, 255))
    pointer = pg.transform.scale(pointer, (28, 28))
    s_x = params['screen_width'] - mx - 50
    s_y = (select + 1) * 1.5 * FS[1]

    surface.blit(pointer, (s_x, s_y))
    pg.display.flip()


def display_menu_items(gp):
    """List user items that are type items.
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

    # Item list full length
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [400, params['screen_height'] - 150]
    bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))

    surface.blit(bck, (params['screen_width'] - bck_size[0], 0), bck.get_rect())

    item_list, mx = return_only_item(user_items, font)

    opt = 0
    display_menu_items_scroll(surface, font, item_list, mx, select=opt)
    reading = True
    while reading:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                reading = False
                pg.quit()
                break
            elif e.type == pg.KEYDOWN:
                # Exit Menu
                if e.key == pg.K_q:
                    return False
                # Use item
                if e.key in [pg.K_RETURN]:
                    if 'Exit' in item_list[opt]:
                        return
                    else:
                        use_item = use_or_cancel(gp, item_list[opt])
                        if use_item[0]:
                            # Need logic here for items that heal entire group (maybe battle only?)
                            tmp_item = ge.get_items_for_use(user_items[opt])
                            gp['char'][use_item[1]] = tmp_item['action'](gp, tmp_item, use_item[1])
                            user_items.pop(opt)
                            item_list, mx = return_only_item(user_items, font)
                            del tmp_item
                if e.key == pg.K_DOWN:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt += 1
                    if opt == len(item_list):
                        opt = 0
                if e.key == pg.K_UP:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt -= 1
                    if opt == -1:
                        opt = len(item_list) - 1
            display_menu_items_scroll(surface, font, item_list, mx, select=opt)
        clock.tick(params['frames_per_second'])


def return_only_item(user_items, font, item_type='Item', ei=[]):
    FS = font.render('TMP', 0, (0, 0, 0)).get_size()

    item_list = []
    i = 0
    mx = 0
    # Only list "Item" items...
    for i in range(len(user_items)):
        a = user_items[i]
        if ge.get_items_for_use(ind=a)['type'] is not item_type:
            continue
        y = FS[1] * 1.5 * (len(item_list) + 1)
        color = (0, 0, 0)
        if i in ei:
            color = (0, 0, 255)
        item_list.append({a:{'font': font.render(a, 0, color),
                             'y': y
                            }})
        xl = 40 + item_list[-1][a]['font'].get_size()[0]
        if xl > mx:
            mx = xl
    # Add exit to list
    y = FS[1] * 1.5 * (len(item_list) + 1)
    item_list.append({'Exit': {'font': font.render('Exit', 0, (0, 0, 0)),
                               'y': y
                              }})
    if mx == 0:
        mx = 40 + item_list[-1]['Exit']['font'].get_size()[0]

    return item_list, mx


def return_only_equipment(gp, user_items, font, item_type):
    FS = font.render('TMP', 0, (0, 0, 0)).get_size()

    item_list = []
    item_idx = []
    i = 0
    mx = 0

    equip_list = ge.get_equipment_for_use()

    heros = gp['char']

    ei = []
    # get list of equipment idx
    for i in range(len(heros)):
        if heros[i][item_type]['idx'] is not None:
            ei.append(heros[i][item_type]['idx'])

    for i in range(len(user_items)):
        a = user_items[i]
        k = a.keys()[0] 
        if k is 'Exit':
            continue
        if k not in equip_list.keys():
            continue
        if equip_list[k]['type'] is not item_type:
            continue
        y = FS[1] * 1.5 * (len(item_list) + 1)
        # Check if item is equipped
        color = (0, 0, 0)
        if i in ei:
            color = (0, 0, 255)
        item_list.append({k:{'font': font.render(k, 0, color),
                             'y': y
                            }})
        item_idx.append(i)
        xl = 40 + item_list[-1][k]['font'].get_size()[0]
        if xl > mx:
            mx = xl
    # Add exit to list
    y = FS[1] * 1.5 * (len(item_list) + 1)
    item_list.append({'Exit': {'font': font.render('Exit', 0, (0, 0, 0)),
                               'y': y
                              }})
    if mx == 0:
        mx = 40 + item_list[-1]['Exit']['font'].get_size()[0]

    return item_list, item_idx, mx


def display_menu_items_scroll(surface, font, item_list, mx, select=0):
    """

    """
    cwd = os.getcwd()
    params = settings.params()

    # Black screen
    pg.draw.rect(surface, (0, 0, 0), (0, 0, params['screen_width'], params['screen_height']))

    # Item list full length
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [400, params['screen_height'] - 150]
    bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))

    surface.blit(bck, (params['screen_width'] - bck_size[0], 0), bck.get_rect())

    FS = font.render('TMP', 0, (0, 0, 0)).get_size()

    # maximum number of items to show
    mx_show_items = 12
    start = 0
    stop = len(item_list)
    # if the stop point is greater than the maximum allowed displayed
    if stop > mx_show_items:
        # if the user cursur is more than the last position
        if select + 1 >= mx_show_items:
            start = select - mx_show_items + 1
            stop = select + 1
        else:
            stop = mx_show_items

    for i in range(start, stop):
        for a in item_list[i]:
            a_font = item_list[i][a]['font']
            a_y = item_list[i][a]['y']
            a_x = params['screen_width'] - mx
            if len(item_list) > mx_show_items:
                a_y = (i - start + 1) * FS[1] * 1.5
        surface.blit(a_font, (a_x, a_y))

    # Pointer
    pointer = pg.image.load(cwd + '/imgs/textbox/arrowBrown_right.png')
    pointer.set_colorkey((255, 255, 255))
    pointer = pg.transform.scale(pointer, (28, 28))
    s_x = params['screen_width'] - mx - 50
    s_y = (select + 1) * 1.5 * FS[1]
    if select + 1 > mx_show_items:
        s_y = (mx_show_items) * 1.5 * FS[1]
    surface.blit(pointer, (s_x, s_y))
    pg.display.flip()


def use_or_cancel(gp, item):
    """ Keep old screen, just up/down area
    """
    cwd = os.getcwd()
    params = settings.params()

    # gp game parameters
    surface = gp['screen']
    font = gp['font']
    clock = gp['clock']
    music = gp['music']

    # Black screen over bottom left
    pg.draw.rect(surface, (0, 0, 0), (params['screen_width'] - 400, params['screen_height'] - 150, 400, 150))

    # Display use or cancel option
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [400, 150]
    bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))

    surface.blit(bck, (params['screen_width'] - bck_size[0], params['screen_height'] - bck_size[1]), bck.get_rect())

    FS = font.render('TMP', 0, (0, 0, 0)).get_size()

    item_list = []
    y = params['screen_height'] - bck_size[1] + FS[1] * 1.5
    item_list.append({'Use': {'font': font.render('Use', 0, (0, 0, 0)),
                               'y': y
                              }})
    y = params['screen_height'] - bck_size[1] + FS[1] * 3.0
    item_list.append({'Cancel': {'font': font.render('Cancel', 0, (0, 0, 0)),
                               'y': y
                              }})
    mx = 40 + item_list[-1]['Cancel']['font'].get_size()[0]

    # while loop for select option
    reading = True
    opt = 0
    use_or_cancel_move(gp, item_list, mx, select=opt)
    while reading:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                reading = False
                pg.quit()
                break
            elif e.type == pg.KEYDOWN:
                # Use item
                if e.key == pg.K_q:
                    return False
                if e.key in [pg.K_RETURN]:
                    if opt == 1:
                        return False
                    else:
                        return display_heros_for_item_use(gp, item)
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
                use_or_cancel_move(gp, item_list, mx, select=opt)
        clock.tick(params['frames_per_second'])
    return False


def use_or_cancel_move(gp, item_list, mx, select=0):
    """
    """
    cwd = os.getcwd()
    params = settings.params()

    # gp game parameters
    surface = gp['screen']
    font = gp['font']
    clock = gp['clock']
    music = gp['music']

    # Black screen over bottom left
    pg.draw.rect(surface, (0, 0, 0), (params['screen_width'] - 400, params['screen_height'] - 150, 400, 150))

    # Display use or cancel option
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [400, 150]
    bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))

    surface.blit(bck, (params['screen_width'] - bck_size[0], params['screen_height'] - bck_size[1]), bck.get_rect())

    FS = font.render('TMP', 0, (0, 0, 0)).get_size()
    for i in range(len(item_list)):
        a_x = params['screen_width'] - mx
        for a in item_list[i]:
            a_font = item_list[i][a]['font']
            a_y = item_list[i][a]['y']
            if i == select:
                s_y = a_y
        surface.blit(a_font, (a_x, a_y))

    # Pointer
    pointer = pg.image.load(cwd + '/imgs/textbox/arrowBrown_right.png')
    pointer.set_colorkey((255, 255, 255))
    pointer = pg.transform.scale(pointer, (28, 28))
    s_x = params['screen_width'] - mx - 50

    surface.blit(pointer, (s_x, s_y))
    pg.display.flip()


def display_heros_for_item_use(gp, item):
    """Display the list of heros from settings
    """
    cwd = os.getcwd()
    params = settings.params()

    # gp game parameters
    clock = gp['clock']
    music = gp['music']
    heros = gp['char']

    opt = 0
    reading = True
    display_give_item_to_hero(gp, item, select=opt)
    while reading:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                reading = False
                pg.quit()
                break
            elif e.type == pg.KEYDOWN:
                # Exit Menu
                if e.key == pg.K_q:
                    return False, None
                if e.key == pg.K_RETURN:
                    # Use potion
                    return True, opt
                if e.key == pg.K_DOWN:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt += 1
                    if opt == len(heros):
                        opt = 0
                if e.key == pg.K_UP:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt -= 1
                    if opt == -1:
                        opt = len(heros) - 1
                display_give_item_to_hero(gp, item, select=opt)
        clock.tick(params['frames_per_second'])


def display_give_item_to_hero(gp, item, select=0):
    """
    """
    MSIZE = 3.5

    cwd = os.getcwd()
    params = settings.params()

    # gp game parameters
    surface = gp['screen']
    font = gp['font']
    clock = gp['clock']
    music = gp['music']
    heros = gp['char']

    # Black screen over left-hand portion
    pg.draw.rect(surface, (0, 0, 0), (0, 0, params['screen_width'] - 400, params['screen_height']))

    # Display bkg for each hero
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [params['screen_width'] - 400,  240]
    bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))

    # Hero Name not normal font size
    hn = pg.font.Font('misc/Anonymous_Pro.ttf', params['font_size'] + 4)
    hn.set_underline(True)

    mx_show_items = 3
    start = 0
    stop = len(heros)

    if stop > mx_show_items:
        # if the user cursur is more than the last position
        if select + 1 >= mx_show_items:
            start = select - mx_show_items + 1
            stop = select + 1
        else:
            stop = mx_show_items

    # Needs to be displayed for each hero
    for i in range(start, stop):
        ii = i - start
        surface.blit(bck, (0, ii * bck_size[1]), bck.get_rect())

        # Char Name
        hero_name = hn.render(heros[i]['name'], 0, (0, 0, 0))
        s_y = ii * bck_size[1] + 8
        surface.blit(hero_name, (100, s_y))

        # Display Image
        ci = dialog.get_char_img(heros[i]['class'])
        cj = pg.image.load(cwd + dialog.get_char_sheets(ci['sheet'])).convert()
        char = pg.transform.rotozoom(cj, 0, MSIZE)
        char.set_colorkey((254, 255, 254))
        if i == select:
            surface.blit(char, (50, hero_name.get_size()[1] + ii * bck_size[1] + int((bck_size[1] - 180.)/2.)), (ci['pos'][0]*48*MSIZE, ci['pos'][1]*MSIZE*48, (48-1)*MSIZE, (48)*MSIZE))
        else:
            surface.blit(char, (100, hero_name.get_size()[1] + ii * bck_size[1] + int((bck_size[1] - 180.)/2.)), (ci['pos'][0]*48*MSIZE, ci['pos'][1]*MSIZE*48, (48-1)*MSIZE, (48)*MSIZE))

        s_x = 325


        # Char Level
        lv = font.render('Level: ', 0, (0, 0, 255))
        s_y = s_y + hero_name.get_size()[1] + 8
        surface.blit(lv, (s_x, s_y))

        lv_l = lv.get_size()[0]
        lv = font.render(str(heros[i]['level']), 0, (0, 0, 0))
        surface.blit(lv, (s_x + lv_l, s_y))

        # Char Job
        jb = heros[i]['class']
        if '_' in jb:
            jb = heros[i]['class'].split('_')[0]
        job = font.render(jb.capitalize(), 0, (0, 0, 0))
        s_y = s_y + hero_name.get_size()[1] + 8
        surface.blit(job, (s_x, s_y))

        s_x = 700

        # Char HP / MP
        cur_hp = heros[i]['HP']
        cur_mp = heros[i]['MP']
        base = settings.get_base_stats(jb, heros[i]['level'])
        max_hp = base['HP']
        max_mp = base['MP']

        s_y = ii * bck_size[1] + 60
        pg.draw.rect(surface, (0, 0, 0), (s_x, s_y - 8, 126, 26))
        cr = float(cur_hp)/float(max_hp)
        HEALTH = (int(255.*(1.-cr)), int(255. * cr),  0)
        for j in range(1, 101):
            if float(j) <= cr * 100.:
                pg.draw.circle(surface,
                               HEALTH,
                               (s_x + j + 12, s_y + 5), 10, 10)

        HEALTH = font.render(str(cur_hp) + '/' + str(max_hp), 0, (0, 0, 0))
        surface.blit(HEALTH, (s_x - 140, s_y - 10))


        s_y += job.get_size()[1] + 18
        pg.draw.rect(surface, (0, 0, 0), (s_x, s_y - 8, 126, 26))
        cr = float(cur_mp)/float(max_mp)

        HEALTH = (int(255.*(1.-cr)), int(255. * cr), 255)
        for j in range(1, 101):
            if float(j) <= cr * 100.:
                pg.draw.circle(surface,
                               HEALTH,
                               (s_x + j + 12, s_y + 5), 10, 10)
        HEALTH = font.render(str(cur_mp) + '/' + str(max_mp), 0, (0, 0, 0))
        surface.blit(HEALTH, (s_x - 140 , s_y - 10))

    pg.display.flip()


def display_menu_equipment(gp):
    """Display equipment and playable characters

    pointer is on the list of available equipment.

    """
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
        if ge.get_items_for_use(ind=a)['type'] is 'Equipment':
            start += 1
            continue
        if start > stop:
            continue
        for j in range(start, stop):
            equipped[j] += 1

    # return only equipment w/ max length
    item_list, mx = return_only_item(user_items, font, item_type='Equipment', ei=equipped)

    opt = 0
    msel = 0
    h_opt = 0
    display_hero_equipment_scroll(gp, item_list, mx, select=opt, hs=msel, col=h_opt)
    reading = True
    while reading:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                reading = False
                pg.quit()
                break
            elif e.type == pg.KEYDOWN:
                # Exit Menu
                if e.key == pg.K_q:
                    return False
                # Use item
                if e.key in [pg.K_RETURN]:
                    if h_opt == 0:
                        if 'Exit' in item_list[opt]:
                            return
                    else:
                        equip_item = go_to_equipment_menu(gp, item_list, mx, msel)
                        # Select hero
                        if equip_item is not False:
                            if equip_item[0] is not False:
                                # equip_item (true, item idx), hero idx
                                add_equip_to_player(gp, equip_item, msel)

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
                                    if ge.get_items_for_use(ind=a)['type'] is 'Equipment':
                                        start += 1
                                        continue
                                    if start > stop:
                                        continue
                                    for j in range(start, stop):
                                        equipped[j] += 1

                                print(equipped, 'equipped')
                                # return only equipment w/ max length
                                item_list, mx = return_only_item(user_items, font, item_type='Equipment', ei=equipped)

                if e.key == pg.K_DOWN:
                    music.play_sound(music.sound_list('menu'), num=1)
                    if h_opt == 0:
                        opt += 1
                        if opt == len(item_list):
                            opt = 0
                    else:
                        msel += 1
                        if msel == len(heros):
                            msel = 0
                elif e.key == pg.K_UP:
                    music.play_sound(music.sound_list('menu'), num=1)
                    if h_opt == 0:
                        opt -= 1
                        if opt == -1:
                            opt = len(item_list) - 1
                    else:
                        msel -= 1
                        if msel == -1:
                            msel = len(heros) - 1
                elif e.key == pg.K_LEFT:
                    music.play_sound(music.sound_list('menu'), num=1)
                    h_opt += 1
                    if h_opt == 2:
                        h_opt = 0
                elif e.key == pg.K_RIGHT:
                    music.play_sound(music.sound_list('menu'), num=1)
                    h_opt -= 1
                    if h_opt == -1:
                        h_opt = 1
                display_hero_equipment_scroll(gp, item_list, mx, select=opt, hs=msel, col=h_opt)
        clock.tick(params['frames_per_second'])


def go_to_equipment_menu(gp, item_list, mx, msel):
    """Select a player, and allow user to scroll between weapon, head, body, and legs
    """
    cwd = os.getcwd()
    params = settings.params()

    # gp game parameters
    surface = gp['screen']
    clock = gp['clock']
    music = gp['music']

    opt = 0
    reading = True
    change_equipment(gp, item_list, msel, select=opt)
    while reading:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                reading = False
                pg.quit()
                break
            elif e.type == pg.KEYDOWN:
                # Exit Menu
                if e.key == pg.K_q:
                    return False, None
                if e.key == pg.K_RETURN:
                    # Change equipment
                    # Returns True, item index (use item index to find type)
                    return update_equip_list(gp, item_list, select=opt)
                if e.key == pg.K_DOWN:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt += 1
                    if opt == 5:
                        opt = 0
                if e.key == pg.K_UP:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt -= 1
                    if opt == -1:
                        opt = 4
                change_equipment(gp, item_list, msel, select=opt)
        clock.tick(params['frames_per_second'])


def update_equip_list(gp, user_items, select=0):
    """scroll through equipment list for equipment of a certain type
    """
    cwd = os.getcwd()
    params = settings.params()

    font = gp['font']
    clock = gp['clock']
    music = gp['music']
    heros = gp['char']

    x = ['weapon', 'head', 'body', 'legs', 'gem']

    # return only equipment w/ max length of item_type (i.e., 'head' or 'body')
    item_list, item_idx, mx = return_only_equipment(gp, user_items, font, item_type=x[select])

    opt = 0
    select_item_to_equip(gp, item_list, mx, select=opt)
    reading = True
    while reading:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                reading = False
                pg.quit()
                break
            elif e.type == pg.KEYDOWN:
                # Exit Menu
                if e.key == pg.K_q:
                    return False
                if e.key == pg.K_RETURN:
                    if 'Exit' in item_list[opt]:
                        return False, None
                    music.play_sound(music.sound_list('change_equip'), num=1)
                    return True, item_idx[opt]
                if e.key == pg.K_DOWN:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt += 1
                    if opt == len(item_list):
                        opt = 0
                if e.key == pg.K_UP:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt -= 1
                    if opt == -1:
                        opt = len(item_list) - 1
            select_item_to_equip(gp, item_list, mx, select=opt)
        clock.tick(params['frames_per_second'])


def select_item_to_equip(gp, item_list, mx, select=0):
    """
    """
    cwd = os.getcwd()
    params = settings.params()

    # gp game parameters
    surface = gp['screen']
    font = gp['font']
    clock = gp['clock']
    music = gp['music']
    heros = gp['char']

    # Display new menu list
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [400,  params['screen_height']]
    bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))
    surface.blit(bck, (params['screen_width'] - bck_size[0], 0), bck.get_rect())

    FS = font.render('TMP', 0, (0, 0, 0)).get_size()

    # maximum number of items to show
    mx_show_items = 15
    start = 0
    stop = len(item_list)
    # if the stop point is greater than the maximum allowed displayed
    if stop > mx_show_items:
        # if the user cursur is more than the last position
        if select + 1 >= mx_show_items:
            start = select - mx_show_items + 1
            stop = select + 1
        else:
            stop = mx_show_items

    for i in range(start, stop):
        for a in item_list[i]:
            a_font = item_list[i][a]['font']
            a_y = item_list[i][a]['y']
            a_x = params['screen_width'] - mx
            if len(item_list) > mx_show_items:
                a_y = (i - start + 1) * FS[1] * 1.5
        surface.blit(a_font, (a_x, a_y))

    # Pointer
    pointer = pg.image.load(cwd + '/imgs/textbox/arrowBrown_right.png')
    pointer.set_colorkey((255, 255, 255))
    pointer = pg.transform.scale(pointer, (28, 28))
    s_x = params['screen_width'] - mx - 50
    s_y = (select + 1) * 1.5 * FS[1]
    if select + 1 > mx_show_items:
        s_y = (mx_show_items) * 1.5 * FS[1]
    surface.blit(pointer, (s_x, s_y))
    pg.display.flip()


def change_equipment(gp, item, msel, select=0):
    """ Display the equipment list and the heros
    """
    cwd = os.getcwd()
    params = settings.params()
    MSIZE = 3.5

    # gp game parameters
    surface = gp['screen']
    font = gp['font']
    clock = gp['clock']
    music = gp['music']
    heros = gp['char']

    bck_size = [params['screen_width'] - 400,  240]
    # do not change msel, might need variable for equiping item
    if msel > 2:
        pg.draw.rect(surface, (0, 0, 0), (0, 2 * bck_size[1], bck_size[0], bck_size[1]))
    else:
        pg.draw.rect(surface, (0, 0, 0), (0, msel * bck_size[1], bck_size[0], bck_size[1]))

    FS = font.render('TMP', 0, (0, 0, 0)).get_size()

    # Display hero
    hn = pg.font.Font('misc/Anonymous_Pro.ttf', params['font_size'] + 4)
    hn.set_underline(True)

    # Display bkg for each hero
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))


    i = msel
    ii = msel
    if msel > 2:
        ii = 2
    surface.blit(bck, (0, ii * bck_size[1]), bck.get_rect())

    # Char Name
    hero_name = hn.render(heros[i]['name'], 0, (0, 0, 0))
    s_y = ii * bck_size[1] + 8
    surface.blit(hero_name, (100, s_y))

    # Display Image
    ci = dialog.get_char_img(heros[i]['class'])
    cj = pg.image.load(cwd + dialog.get_char_sheets(ci['sheet'])).convert()
    char = pg.transform.rotozoom(cj, 0, MSIZE)
    char.set_colorkey((254, 255, 254))
    surface.blit(char, (50, hero_name.get_size()[1] + ii * bck_size[1] + int((bck_size[1] - 180.)/2.)), (ci['pos'][0]*48*MSIZE, ci['pos'][1]*48*MSIZE, (48-1)*MSIZE, (48)*MSIZE))

    s_x = 285


    addl = {'STR': 0, 'END': 0, 'DEX': 0,
        'WSD': 0, 'INT': 0, 'CHR': 0}

    ps = ['weapon', 'head', 'body', 'legs', 'gem']
    qs = ['Weapon', 'Head Armor', 'Body Armor', 'Leg Armor', 'Gem']

    for s in range(len(ps)):
        eq = font.render(qs[s] + ': ', 0, (0, 0, 0))
        s_y = s_y + eq.get_size()[1] + 8
        surface.blit(eq, (s_x, s_y))
        eq = font.render('None', 0, (255, 0, 0))
        if heros[i][ps[s]]['name'] is not None:
            eq = font.render(heros[i][ps[s]]['name'], 0, (0, 0, 255))
            armor_stat = ge.get_equipment_for_use(heros[i][ps[s]]['name'])
            if armor_stat['inc'] is not None:
                for stat in armor_stat['inc']:
                    addl[stat] += armor_stat['inc'][stat]
        surface.blit(eq, (s_x + 175, s_y))
 
    s_x = 680
    # Char Job
    jb = heros[i]['class']
    if '_' in jb:
        jb = heros[i]['class'].split('_')[0]
    base = settings.get_base_stats(jb, heros[i]['level'])

    ps = ['STR', 'END', 'DEX', 'WSD', 'INT', 'CHR']
    for s in range(len(ps)):
        eq = font.render(ps[s] + ': ', 0, (0, 0, 0))
        peq = eq.get_size()[0]
        if s == 0:
            s_y = ii * bck_size[1] + 12
        else:
            s_y += (eq.get_size()[1] + 8)
        surface.blit(eq, (s_x, s_y))

        eq = font.render(str(base[ps[s]]), 0, (0, 0, 0))
        surface.blit(eq, (s_x + peq, s_y))

        if addl[ps[s]] != 0:
            if addl[ps[s]] > 0:
                stat = font.render('+' + str(addl[ps[s]]), 0, (0, 0, 255))
            elif addl[ps[s]] < 0:
                stat = font.render('+' + str(addl[ps[s]]), 0, (0, 0, 255))
            surface.blit(stat, (s_x + peq + eq.get_size()[0], s_y))

    # Pointer
    pointer = pg.image.load(cwd + '/imgs/textbox/woa_items1.png')
    pointer.set_colorkey((255, 255, 255))
    s_x = 245
    s_y = msel * bck_size[1] + (FS[1] + 8) * (select + 1)
    if msel > 2:
        s_y = 2 * bck_size[1] + (FS[1] + 8) * (select + 1)
    if select == 4:
        surface.blit(pointer, (s_x, s_y), (4 * 32, 3 * 32, 32, 32))
    elif select > 0:
        surface.blit(pointer, (s_x, s_y), (1 * 32, 2 * 32, 32, 32))
    else:
        surface.blit(pointer, (s_x, s_y), (5 * 32, 0 * 32, 32, 32))
    pg.display.flip()


def display_hero_equipment_scroll(gp, item_list, mx, select=0, hs=0, col=0):
    """ Display the equipment list and the heros

    Update the pointer location based on the select (for col=0) and hs (based on col=1)

    """
    cwd = os.getcwd()
    params = settings.params()
    MSIZE = 3.5

    # gp game parameters
    surface = gp['screen']
    font = gp['font']
    clock = gp['clock']
    music = gp['music']
    heros = gp['char']

    # Black screen
    pg.draw.rect(surface, (0, 0, 0), (0, 0, params['screen_width'], params['screen_height']))

    # Item list full length
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [400, params['screen_height']]
    bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))

    surface.blit(bck, (params['screen_width'] - bck_size[0], 0), bck.get_rect())

    FS = font.render('TMP', 0, (0, 0, 0)).get_size()

    # maximum number of items to show
    mx_show_items = 15
    start = 0
    stop = len(item_list)
    # if the stop point is greater than the maximum allowed displayed
    if stop > mx_show_items:
        # if the user cursur is more than the last position
        if select + 1 >= mx_show_items:
            start = select - mx_show_items + 1
            stop = select + 1
        else:
            stop = mx_show_items

    for i in range(start, stop):
        for a in item_list[i]:
            a_font = item_list[i][a]['font']
            a_y = item_list[i][a]['y']
            a_x = params['screen_width'] - mx
            if len(item_list) > mx_show_items:
                a_y = (i - start + 1) * FS[1] * 1.5
        surface.blit(a_font, (a_x, a_y))

    # Display heros
    hn = pg.font.Font('misc/Anonymous_Pro.ttf', params['font_size'] + 4)
    hn.set_underline(True)

    # Display bkg for each hero
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [params['screen_width'] - 400,  240]
    bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))

    mx_show_heros = 3
    start = 0
    stop = len(heros)

    if stop > mx_show_heros:
        # if the user cursur is more than the last position
        if hs + 1 >= mx_show_heros:
            start = hs - mx_show_heros + 1
            stop = hs + 1
        else:
            stop = mx_show_heros

    # Needs to be displayed for each hero
    for i in range(start, stop):
        ii = i - start
        surface.blit(bck, (0, ii * bck_size[1]), bck.get_rect())

        # Char Name
        hero_name = hn.render(heros[i]['name'], 0, (0, 0, 0))
        s_y = ii * bck_size[1] + 8
        surface.blit(hero_name, (100, s_y))

        # Display Image
        ci = dialog.get_char_img(heros[i]['class'])
        cj = pg.image.load(cwd + dialog.get_char_sheets(ci['sheet'])).convert()
        char = pg.transform.rotozoom(cj, 0, MSIZE)
        char.set_colorkey((254, 255, 254))
        surface.blit(char, (100, hero_name.get_size()[1] + ii * bck_size[1] + int((bck_size[1] - 180.)/2.)), (ci['pos'][0]*48*MSIZE, ci['pos'][1]*48*MSIZE, (48-1)*MSIZE, (48)*MSIZE))
        s_x = 285

        # add. to base stats
        addl = {'STR': 0, 'END': 0, 'DEX': 0,
                'WSD': 0, 'INT': 0, 'CHR': 0}

        ps = ['weapon', 'head', 'body', 'legs', 'gem']
        qs = ['Weapon', 'Head Armor', 'Body Armor', 'Leg Armor', 'Gem']
        for s in range(len(ps)):
            eq = font.render(qs[s] + ': ', 0, (0, 0, 0))
            s_y += eq.get_size()[1] + 8
            surface.blit(eq, (s_x, s_y))
            eq = font.render('None', 0, (255, 0, 0))
            if heros[i][ps[s]]['name'] is not None:
                eq = font.render(heros[i][ps[s]]['name'], 0, (0, 0, 255))
                armor_stat = ge.get_equipment_for_use(heros[i][ps[s]]['name'])
                if armor_stat['inc'] is not None:
                    for stat in armor_stat['inc']:
                        addl[stat] += armor_stat['inc'][stat]
            surface.blit(eq, (s_x + 175, s_y))

        s_x = 680
        # Char Job
        jb = heros[i]['class']
        if '_' in jb:
            jb = heros[i]['class'].split('_')[0]
        base = settings.get_base_stats(jb, heros[i]['level'])

        ps = ['STR', 'END', 'DEX', 'WSD', 'INT', 'CHR']
        for s in range(len(ps)):
            eq = font.render(ps[s] + ': ', 0, (0, 0, 0))
            peq = eq.get_size()[0]
            if s == 0:
                s_y = ii * bck_size[1] + 12
            else:
                s_y += (eq.get_size()[1] + 8)
            surface.blit(eq, (s_x, s_y))

            eq = font.render(str(base[ps[s]]), 0, (0, 0, 0))
            surface.blit(eq, (s_x + peq, s_y))

            if addl[ps[s]] != 0:
                if addl[ps[s]] > 0:
                    stat = font.render('+' + str(addl[ps[s]]), 0, (0, 0, 255))
                elif addl[ps[s]] < 0:
                    stat = font.render('+' + str(addl[ps[s]]), 0, (0, 0, 255))
                surface.blit(stat, (s_x + peq + eq.get_size()[0], s_y))


    # Pointer
    pointer = pg.image.load(cwd + '/imgs/textbox/arrowBrown_right.png')
    pointer.set_colorkey((255, 255, 255))
    pointer = pg.transform.scale(pointer, (28, 28))
    if col == 0:
        s_x = params['screen_width'] - mx - 50
        s_y = (select + 1) * 1.5 * FS[1]
        if select + 1 > mx_show_items:
            s_y = (mx_show_items) * 1.5 * FS[1]
    if col == 1:
        s_x = 50
        s_y = hs * bck_size[1] + 104
        if hs + 1 > mx_show_heros:
            s_y = (mx_show_heros - 1) * bck_size[1] + 104
    surface.blit(pointer, (s_x, s_y))
    pg.display.flip()


def add_equip_to_player(gp, item, msel):
    """Actually equip an item
    """
    heros = gp['char']
    all_items = gp['items']

    all_equipment = ge.get_equipment_for_use()

    # only equipment
    equip_items = []
    for i in range(len(all_items)):
        if all_items[i] in all_equipment.keys():
            equip_items.append(all_items[i])

    idx = item[1]
    item_type = ge.get_equipment_for_use(equip_items[idx])

    # type to equip
    x = item_type['type']

    # Equip hero
    if heros[msel][x]['idx'] != idx:
        heros[msel][x]['name'] = equip_items[idx]
        heros[msel][x]['idx'] = idx
    else:
        heros[msel][x]['name'] = None
        heros[msel][x]['idx'] = None
    # Remove item from other hero if equipped
    for i in range(len(heros)):
        if i == msel:
            continue
        if heros[i][x]['idx'] == idx:
            heros[i][x]['idx'] = None
            heros[i][x]['name'] = None
    return


def display_menu_status(gp):
    """Display the status of each player,
    including  exp / exp next level, att, def, m. att, m.def
    level, class
    exp shown as a bar
    """
    cwd = os.getcwd()
    params = settings.params()

    # gp game parameters
    clock = gp['clock']
    music = gp['music']
    heros = gp['char']

    opt = 0
    reading = True
    display_status(gp, select=opt)
    while reading:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                reading = False
                pg.quit()
                break
            elif e.type == pg.KEYDOWN:
                # Exit Menu
                if e.key == pg.K_q:
                    return False, None
                if e.key == pg.K_DOWN:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt += 1
                    if opt == len(heros):
                        opt = 0
                if e.key == pg.K_UP:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt -= 1
                    if opt == -1:
                        opt = len(heros) - 1
                display_status(gp, select=opt)
        clock.tick(params['frames_per_second'])


def display_status(gp, select=0):
    """
    """
    cwd = os.getcwd()
    params = settings.params()
    MSIZE = 3.5

    # gp game parameters
    surface = gp['screen']
    font = gp['font']
    clock = gp['clock']
    music = gp['music']
    heros = gp['char']

    # Black screen
    pg.draw.rect(surface, (0, 0, 0), (0, 0, params['screen_width'], params['screen_height']))

    # Regular font
    FS = font.render('TMP', 0, (0, 0, 0)).get_size()

    # Display heros
    hn = pg.font.Font('misc/Anonymous_Pro.ttf', params['font_size'] + 4)
    hn.set_underline(True)

    mx_show_heros = 3
    start = 0
    stop = len(heros)

    if stop > mx_show_heros:
        # if the user cursur is more than the last position
        if select + 1 >= mx_show_heros:
            start = select - mx_show_heros + 1
            stop = select + 1
        else:
            stop = mx_show_heros

    # Item list full width
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [params['screen_width'], 240]
    bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))

    for i in range(start, stop):
        ii = i - start
        surface.blit(bck, (0, ii * bck_size[1]), bck.get_rect())

        # Char Name
        hero_name = hn.render(heros[i]['name'], 0, (0, 0, 0))
        s_y = ii * bck_size[1] + 8
        surface.blit(hero_name, (100, s_y))

        # Display Image
        ci = dialog.get_char_img(heros[i]['class'])
        cj = pg.image.load(cwd + dialog.get_char_sheets(ci['sheet'])).convert()

        char = pg.transform.rotozoom(cj, 0, MSIZE)
        char.set_colorkey((254, 255, 254))
        if i == select:
            surface.blit(char, (50, hero_name.get_size()[1] + ii * bck_size[1] + int((bck_size[1] - 180.)/2.)), (ci['pos'][0]*48*MSIZE, ci['pos'][1]*48*MSIZE, (48-1)*MSIZE, (48)*MSIZE))
        else:
            surface.blit(char, (100, hero_name.get_size()[1] + ii * bck_size[1] + int((bck_size[1] - 180.)/2.)), (ci['pos'][0]*48*MSIZE, ci['pos'][1]*48*MSIZE, (48-1)*MSIZE, (48)*MSIZE))
        s_x = 285


        # Char Level
        lv = font.render('Level: ', 0, (0, 0, 255))
        s_y = s_y + hero_name.get_size()[1] + 8
        surface.blit(lv, (s_x, s_y))

        lv_l = lv.get_size()[0]
        lv = font.render(str(heros[i]['level']), 0, (0, 0, 0))
        surface.blit(lv, (s_x + lv_l, s_y))

        # Char Job
        jb = heros[i]['class']
        if '_' in jb:
            jb = heros[i]['class'].split('_')[0]
        job = font.render(jb.capitalize(), 0, (0, 0, 0))
        s_y = s_y + hero_name.get_size()[1] + 8
        surface.blit(job, (s_x, s_y))

        # Char Exp
        cur_exp = heros[i]['exp']
        cur_lvl_exp = settings.exp_to_level(heros[i]['level'])
        base = settings.get_base_stats(jb, heros[i]['level'])

        eq = font.render('Gem: ', 0, (0, 0, 0))
        s_y = s_y + eq.get_size()[1] + 8
        surface.blit(eq, (s_x, s_y))

        eq = font.render('None', 0, (255, 0, 0))
        if heros[i]['gem']['name'] is not None:
            eq = font.render(heros[i]['gem']['name'], 0, (0, 0, 255))
        surface.blit(eq, (s_x + 100, s_y))

        if heros[i]['gem']['name'] is not None:
            gt = ge.get_equipment_for_use(ind=heros[i]['gem']['name'])['class']
            gemexp = [10, 30, 80, 180, 380, 880, 1880, 3880, 8880, 18880, 38880]
            cur_exp = heros[i]['gemlvl'][gt]
            cur_skill = 0
            for g in range(len(gemexp)):
                if gemexp[g] > cur_exp:
                    cur_skill = g + 1
                    break
            eq = font.render(gt.capitalize() +  ' Lv: ' + str(cur_skill), 0, (0, 0, 0))
            s_y = s_y + eq.get_size()[1] + 8
            surface.blit(eq, (s_x, s_y))


        s_x = 680
        if heros[i]['gem']['name'] is not None:
            s_y += int(job.get_size()[1] * 1.25) + 8
        else:
            s_y += int(job.get_size()[1] * 1.25) * 2 + 8

        pg.draw.rect(surface, (0, 0, 0), (s_x, s_y - 8, 126, 26))

        cr = float(cur_exp) / float(cur_lvl_exp)
        TILEXP = (int(255.*(1.-cr)), 0,  255)

        for j in range(1, 101):
            if float(j) <= cr * 100.:
                pg.draw.circle(surface,
                               TILEXP,
                               (s_x + j + 12, s_y + 5), 10, 10)

        t_s_x = 395
        if heros[i]['level'] < 99:
            HEALTH = font.render('Exp To Lvl: ' + str(cur_exp) + '/' + str(cur_lvl_exp), 0, (0, 0, 0))
            surface.blit(HEALTH, (s_x - t_s_x, s_y - 10))
            print(s_x, s_y, TILEXP, ii)
        else:
            hn.set_underline(False)
            rot = hn.render('Exp To Lvl: ' + u'\u221E', 0, (0, 0, 0))
            rot_l = rot.get_size()[0]
            surface.blit(rot, (s_x - t_s_x, s_y - 10))
            ro = font.render('/', 0, (0, 0, 0))
            surface.blit(ro, (s_x - t_s_x + rot_l, s_y - 10))
            rot_l += ro.get_size()[0]
            surface.blit(rot, (s_x - t_s_x + rot_l, s_y - 10))


        b1s = {
            'ATT': 0,
            'DEF': 0,
            'MATK': 0,
            'MDEF': 0
        }

        addl = {'STR': base['STR'], 'END': base['END'], 'DEX': base['DEX'],
        'WSD': base['WSD'], 'INT': base['INT'], 'CHR': base['CHR']}

        ps = ['weapon', 'head', 'body', 'legs', 'gem']
        for s in range(len(ps)):
            if heros[i][ps[s]]['name'] is not None:
                armor_stat = ge.get_equipment_for_use(heros[i][ps[s]]['name'])
                if armor_stat['inc'] is not None:
                    for stat in armor_stat['inc']:
                        addl[stat] += armor_stat['inc'][stat]
                if armor_stat['bat'] is not None:
                    for stat in armor_stat['bat']:
                        b1s[stat] += armor_stat['bat'][stat]
        bstats = {
            'Attack': settings.calc_hero_att(b1s['ATT'], addl['STR'], addl['DEX']),
            'Defense': settings.calc_hero_def(b1s['DEF'], addl['END'], addl['DEX']),
            'M. Att': settings.calc_hero_att(b1s['MATK'], addl['INT'], addl['CHR']),
            'M. Def': settings.calc_hero_def(b1s['MDEF'], addl['WSD'], addl['CHR'])
        }

        s_x = 680
        bsl = ['Attack', 'Defense', 'M. Att', 'M. Def']
        peq = font.render('Defense' + ': ', 0, (0, 0, 0)).get_size()[0]
        for s in range(len(bsl)):
            eq = font.render(bsl[s] + ': ', 0, (0, 0, 0))
            if s == 0:
                s_y = ii * bck_size[1] + 12 + hero_name.get_size()[1]
            else:
                s_y += (eq.get_size()[1] + 8)
            surface.blit(eq, (s_x, s_y))

            eq = font.render(str(bstats[bsl[s]]), 0, (0, 0, 255))
            surface.blit(eq, (s_x + peq, s_y))

    pg.display.flip()


def display_menu_gem(gp):
    """Display each hero's gem status
    """
    cwd = os.getcwd()
    params = settings.params()

    # gp game parameters
    clock = gp['clock']
    music = gp['music']
    heros = gp['char']

    opt = 0
    reading = True
    display_gem_status(gp, select=opt)
    while reading:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                reading = False
                pg.quit()
                break
            elif e.type == pg.KEYDOWN:
                # Exit Menu
                if e.key == pg.K_q:
                    return False, None
                if e.key == pg.K_DOWN:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt += 1
                    if opt == len(heros):
                        opt = 0
                if e.key == pg.K_UP:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt -= 1
                    if opt == -1:
                        opt = len(heros) - 1
                display_gem_status(gp, select=opt)
        clock.tick(params['frames_per_second'])


def display_gem_status(gp, select=0):
    """Allow user to scroll through different heros
    """
    cwd = os.getcwd()
    params = settings.params()
    MSIZE = 3.5

    # gp game parameters
    surface = gp['screen']
    font = gp['font']
    clock = gp['clock']
    music = gp['music']
    heros = gp['char']

    # Black screen
    pg.draw.rect(surface, (0, 0, 0), (0, 0, params['screen_width'], params['screen_height']))

    # Regular font
    FS = font.render('TMP', 0, (0, 0, 0)).get_size()

    # Display heros
    hn = pg.font.Font('misc/Anonymous_Pro.ttf', params['font_size'] + 4)
    hn.set_underline(True)

    mx_show_heros = 3
    start = 0
    stop = len(heros)

    if stop > mx_show_heros:
        # if the user cursur is more than the last position
        if select + 1 >= mx_show_heros:
            start = select - mx_show_heros + 1
            stop = select + 1
        else:
            stop = mx_show_heros

    # Item list full width
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [params['screen_width'], 240]
    bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))
    for i in range(start, stop):
        ii = i - start
        surface.blit(bck, (0, ii * bck_size[1]), bck.get_rect())

        # Char Name
        hero_name = hn.render(heros[i]['name'], 0, (0, 0, 0))
        s_y = ii * bck_size[1] + 8
        surface.blit(hero_name, (100, s_y))

        # Display Image
        ci = dialog.get_char_img(heros[i]['class'])
        cj = pg.image.load(cwd + dialog.get_char_sheets(ci['sheet'])).convert()

        char = pg.transform.rotozoom(cj, 0, MSIZE)
        char.set_colorkey((254, 255, 254))
        if i == select:
            surface.blit(char, (50, hero_name.get_size()[1] + ii * bck_size[1] + int((bck_size[1] - 180.)/2.)), (ci['pos'][0]*48*MSIZE, ci['pos'][1]*48*MSIZE, (48-1)*MSIZE, (48)*MSIZE))
        else:
            surface.blit(char, (100, hero_name.get_size()[1] + ii * bck_size[1] + int((bck_size[1] - 180.)/2.)), (ci['pos'][0]*48*MSIZE, ci['pos'][1]*48*MSIZE, (48-1)*MSIZE, (48)*MSIZE))
        s_x = 285

        gemlvl = ['Fire', 'Water', 'Earth', 'Wind', 'Nature']
        gemexp = [10, 30, 80, 180, 380, 880, 1880, 3880, 8880, 18880, 38880]
        for k in range(len(gemlvl)):
            eq = font.render(gemlvl[k] + ': ', 0, (0, 0, 0))
            # Gem Exp
            cur_exp = heros[i]['gemlvl'][gemlvl[k]]
            cur_lvl_exp = -1
            cr = 1
            for g in range(len(gemexp)):
                if gemexp[g] > cur_exp:
                    cur_lvl_exp = gemexp[g]
                    if g > 0:
                        cr = (float(cur_exp) - float(gemexp[g-1]))/(float(gemexp[g]) - float(gemexp[g-1]))
                    else:
                        cr = float(cur_exp)/float(gemexp[g])
                    break
            s_x = 285
            if k == 0:
                s_y =  ii * bck_size[1] + eq.get_size()[1] + 16
            else:
                s_y += (eq.get_size()[1] + 8)
            surface.blit(eq, (s_x, s_y))
            s_x = 625
            pg.draw.rect(surface, (0, 0, 0), (s_x, s_y, 126, 26))
            TILEXP = (255, int(255 * cr), int(255 * cr))
            for j in range(1, 101):
                if float(j) <= cr * 100.:
                    pg.draw.circle(surface,
                                   TILEXP,
                                   (s_x + j + 12, s_y + 13), 10, 10)
            s_x = 450
            if cur_lvl_exp > 0:
                eq = font.render(str(cur_exp) + '/' + str(cur_lvl_exp), 0, (0, 0, 0))
            else:
                eq = font.render(u'\u221E' + '/' + u'\u221E', 0, (0, 0, 255))
            surface.blit(eq, (s_x, s_y))
    pg.display.flip()


def display_menu_magic(gp):
    """
    """
    cwd = os.getcwd()
    params = settings.params()

    # gp game parameters
    clock = gp['clock']
    music = gp['music']
    heros = gp['char']
    user_items = gp['items']

    magic_range = 0
    if heros[0]['gem']['name'] is not None:
        gt = ge.get_equipment_for_use(ind=heros[0]['gem']['name'])['class']
        gemexp = [10, 30, 80, 180, 380, 880, 1880, 3880, 8880, 18880, 38880]
        cur_exp = heros[0]['gemlvl'][gt]
        cur_skill = 0
        for g in range(len(gemexp)):
            if gemexp[g] > cur_exp:
                cur_skill = g + 1
                break
        if cur_exp > 38880:
            cur_skill = len(gemexp) + 1

        itx = user_items[heros[0]['gem']['idx']]
        gem_level = settings.get_gem_level(gt, name=itx)

        magic_range = min(gem_level, cur_skill)

    nature_spell_list = settings.gem_spells(1e5, ind='Nature')

    opt = 0
    msel = 0
    h_opt = 0
    reading = True
    display_magic_spells(gp, select=opt, msel=msel, vs=h_opt)
    useable_spells = ['Heal', 'Rise', 'Heal II', 'Heal III', 'Healra', 'Healra II']
    while reading:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                reading = False
                pg.quit()
                break
            elif e.type == pg.KEYDOWN:
                # Exit Menu
                if e.key == pg.K_q:
                    return False, None
                if e.key in [pg.K_RETURN] and h_opt == 1:
                    # This is not correct
                    menu_magic = nature_spell_list[msel]
                    if gt == 'Nature' and menu_magic['name'] in useable_spells:
                        # Does hero have enough magic
                        # Hero must not be knocked out and have enough mana
                        if heros[opt]['HP'] == 0 or heros[opt]['MP'] < menu_magic['cost']:
                            # Play cancel sound
                            #                            display_magic_spells(gp, select=opt, msel=msel, vs=h_opt)
                            music.play_sound(music.sound_list('magicfail'), num=1)
                            continue
                        # opt is casting, msel is/are getting
                        sel_hero = select_cast_spell_from_menu(gp, opt, msel)

                        # q returns False, None
                        if None in sel_hero:
                            display_magic_spells(gp, select=opt, msel=msel, vs=h_opt)
                            continue
                        heros[opt]['MP'] -= menu_magic['cost']
                        for h in range(len(sel_hero)):
                            jb = heros[sel_hero[h]]['class']
                            if '_' in jb:
                                jb = heros[sel_hero[h]]['class'].split('_')[0]
                            base = settings.get_base_stats(jb, heros[sel_hero[h]]['level'])

                            jb2 = heros[opt]['class']
                            if '_' in jb2:
                                jb2 = heros[opt]['class'].split('_')[0]
                            base2 = settings.get_base_stats(jb2, heros[opt]['level'])
                            ps = ['weapon', 'head', 'body', 'legs', 'gem']

                            addl = {'STR': base['STR'], 'END': base['END'], 'DEX': base['DEX'],
                                    'WSD': base['WSD'], 'INT': base['INT'], 'CHR': base['CHR']}
                            for s in range(len(ps)):
                                if heros[sel_hero[h]][ps[s]]['name'] is not None:
                                    armor_stat = ge.get_equipment_for_use(heros[sel_hero[h]][ps[s]]['name'])
                                    if armor_stat['inc'] is not None:
                                        for stat in armor_stat['inc']:
                                            addl[stat] += armor_stat['inc'][stat]
                            addl2 = {'STR': base2['STR'], 'END': base2['END'], 'DEX': base2['DEX'],
                                    'WSD': base2['WSD'], 'INT': base2['INT'], 'CHR': base2['CHR']}
                            for s in range(len(ps)):
                                if heros[opt][ps[s]]['name'] is not None:
                                    armor_stat = ge.get_equipment_for_use(heros[opt][ps[s]]['name'])
                                    if armor_stat['inc'] is not None:
                                        for stat in armor_stat['inc']:
                                            addl2[stat] += armor_stat['inc'][stat]

                            if menu_magic['name'] == 'Rise':
                                if heros[sel_hero[h]]['HP'] == 0:
                                    # Restore 33% oh fallen char hp
                                    max_hp = base['HP']
                                    heros[sel_hero[h]]['HP'] = int(0.33 * max_hp)
                            elif menu_magic['name'] != 'Rise':
                                if heros[sel_hero[h]]['HP'] > 0:
                                    heal_mult = 1.1
                                    if menu_magic['name'] in ['Heal II', 'Healra']:
                                        heal_mult = 2.2 
                                    if menu_magic['name'] in ['Heal III', 'Healra II']:
                                        heal_mult = 3.3 
                                    # heal multiplier * WISDOM / 5 + target CHR / 5
                                    heal_x = int(heal_mult * (addl2['WSD']/5 + addl['CHR']/5))

                                    #    print(heal_x)
                                    heros[sel_hero[h]]['HP'] = heros[sel_hero[h]]['HP'] + heal_x
                                    if heros[sel_hero[h]]['HP'] > base['HP']:
                                        heros[sel_hero[h]]['HP'] = base['HP']
                            music.play_sound(music.sound_list('menu_heal'), num=1)
                if e.key == pg.K_DOWN:
                    music.play_sound(music.sound_list('menu'), num=1)
                    if h_opt == 0:
                        opt += 1
                        if opt == len(heros):
                            opt = 0
                    else:
                        msel += 1
                        if msel == magic_range:
                            msel = 0
                elif e.key == pg.K_UP:
                    music.play_sound(music.sound_list('menu'), num=1)
                    if h_opt == 0:
                        opt -= 1
                        if opt == -1:
                            opt = len(heros) - 1
                    else:
                        msel -= 1
                        if msel == -1:
                            msel = magic_range - 1
                elif e.key == pg.K_LEFT:
                    music.play_sound(music.sound_list('menu'), num=1)
                    h_opt += 1
                    if h_opt == 2:
                        h_opt = 0
                elif e.key == pg.K_RIGHT:
                    music.play_sound(music.sound_list('menu'), num=1)
                    h_opt -= 1
                    if h_opt == -1:
                        h_opt = 1
                if heros[opt]['gem']['name'] is not None:
                    gt = ge.get_equipment_for_use(ind=heros[opt]['gem']['name'])['class']
                    gemexp = [10, 30, 80, 180, 380, 880, 1880, 3880, 8880, 18880, 38880]
                    cur_exp = heros[opt]['gemlvl'][gt]
                    cur_skill = 0
                    for g in range(len(gemexp)):
                        if gemexp[g] > cur_exp:
                            cur_skill = g + 1
                            break
                    if cur_exp > 38880:
                        cur_skill = len(gemexp) + 1

                    itx = user_items[heros[opt]['gem']['idx']]
                    gem_level = settings.get_gem_level(gt, name=itx)

                    magic_range = min(gem_level, cur_skill)

                display_magic_spells(gp, select=opt, msel=msel, vs=h_opt)
        clock.tick(params['frames_per_second'])


def display_magic_spells(gp, select=0, msel=0, vs=0):
    """All a user to select a hero
    """
    MSIZE = 3.5
    cwd = os.getcwd()
    params = settings.params()

    # gp game parameters
    surface = gp['screen']
    font = gp['font']
    clock = gp['clock']
    music = gp['music']
    user_items = gp['items']
    heros = gp['char']

    # Get font height
    FS = font.render('T', 0, (0, 0, 0)).get_size()

    # Display heros
    hn = pg.font.Font('misc/Anonymous_Pro.ttf', params['font_size'] + 4)
    hn.set_underline(True)

    # Black screen
    pg.draw.rect(surface, (0, 0, 0), (0, 0, params['screen_width'], params['screen_height']))

    mx_show_heros = 3
    start = 0
    stop = len(heros)

    if stop > mx_show_heros:
        # if the user cursur is more than the last position
        if select + 1 >= mx_show_heros:
            start = select - mx_show_heros + 1
            stop = select + 1
        else:
            stop = mx_show_heros

    # Item list full width
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [params['screen_width']-400, 240]
    bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))

    # Menu List
    m_bck = [400, params['screen_height']]
    Mbck = pg.transform.scale(bck, (m_bck[0], m_bck[1]))
    surface.blit(Mbck, (bck_size[0], 0), Mbck.get_rect())
    for i in range(start, stop):
        ii = i - start
        surface.blit(bck, (0, ii * bck_size[1]), bck.get_rect())

        # Char Name
        hero_name = hn.render(heros[i]['name'], 0, (0, 0, 0))
        s_y = ii * bck_size[1] + 8
        surface.blit(hero_name, (100, s_y))

        # Display Image
        ci = dialog.get_char_img(heros[i]['class'])
        cj = pg.image.load(cwd + dialog.get_char_sheets(ci['sheet'])).convert()

        char = pg.transform.rotozoom(cj, 0, MSIZE)
        char.set_colorkey((254, 255, 254))
        if i == select:
            surface.blit(char, (50, hero_name.get_size()[1] + ii * bck_size[1] + int((bck_size[1] - 180.)/2.)), (ci['pos'][0]*48*MSIZE, ci['pos'][1]*48*MSIZE, (48-1)*MSIZE, (48)*MSIZE))
        else:
            surface.blit(char, (100, hero_name.get_size()[1] + ii * bck_size[1] + int((bck_size[1] - 180.)/2.)), (ci['pos'][0]*48*MSIZE, ci['pos'][1]*48*MSIZE, (48-1)*MSIZE, (48)*MSIZE))

        s_x = 425

        # Char Job
        jb = heros[i]['class']
        if '_' in jb:
            jb = heros[i]['class'].split('_')[0]
        job = font.render(jb.capitalize(), 0, (0, 0, 0))

        # Char HP / MP
        cur_hp = heros[i]['HP']
        cur_mp = heros[i]['MP']
        base = settings.get_base_stats(jb, heros[i]['level'])
        max_hp = base['HP']
        max_mp = base['MP']

        s_y = ii * bck_size[1] + 60
        pg.draw.rect(surface, (0, 0, 0), (s_x, s_y - 8, 126, 26))
        cr = float(cur_hp)/float(max_hp)
        HEALTH = (int(255.*(1.-cr)), int(255. * cr),  0)
        print(HEALTH)
        for j in range(1, 101):
            if float(j) <= cr * 100.:
                pg.draw.circle(surface,
                               HEALTH,
                               (s_x + j + 12, s_y + 5), 10, 10)

        HEALTH = font.render(str(cur_hp) + '/' + str(max_hp), 0, (0, 0, 0))
        surface.blit(HEALTH, (s_x - 140, s_y - 10))


        s_y += job.get_size()[1] + 18
        pg.draw.rect(surface, (0, 0, 0), (s_x, s_y - 8, 126, 26))
        cr = float(cur_mp)/float(max_mp)

        HEALTH = (int(255.*(1.-cr)), int(255. * cr), 255)
        for j in range(1, 101):
            if float(j) <= cr * 100.:
                pg.draw.circle(surface,
                               HEALTH,
                               (s_x + j + 12, s_y + 5), 10, 10)
        HEALTH = font.render(str(cur_mp) + '/' + str(max_mp), 0, (0, 0, 0))
        surface.blit(HEALTH, (s_x - 140 , s_y - 10))

        eq = font.render('Gem: ', 0, (0, 0, 0))
        s_y = s_y + eq.get_size()[1] + 8
        surface.blit(eq, (s_x - 140, s_y))

        eq = font.render('None', 0, (255, 0, 0))
        if heros[i]['gem']['name'] is not None:
            eq = font.render(heros[i]['gem']['name'], 0, (0, 0, 255))
        surface.blit(eq, (s_x, s_y))

        if heros[i]['gem']['name'] is not None:
            gt = ge.get_equipment_for_use(ind=heros[i]['gem']['name'])['class']
            gemexp = [10, 30, 80, 180, 380, 880, 1880, 3880, 8880, 18880, 38880]
            cur_exp = heros[i]['gemlvl'][gt]
            cur_skill = 0
            for g in range(len(gemexp)):
                if gemexp[g] > cur_exp:
                    cur_skill = g + 1
                    break
            if cur_exp > 38880:
                cur_skill = len(gemexp) + 1
            eq = font.render(gt.capitalize() +  ' Lv: ' + str(cur_skill), 0, (0, 0, 0))
            s_y = s_y + eq.get_size()[1] + 8
            surface.blit(eq, (s_x-140, s_y))

            useable_spells = ['Heal', 'Rise', 'Heal II', 'Heal III', 'Healra', 'Healra II']

            # Render spells
            if i == select:
                spell_list = settings.gem_spells(heros[i]['gemlvl'][gt], ind=gt)
                itx = user_items[heros[i]['gem']['idx']]
                gem_level = settings.get_gem_level(gt, name=itx)
                for g in range(len(spell_list)):
                    if g + 1 > gem_level:
                        continue
                    if spell_list[g]['spell'] is None:
                        font.set_italic(True)

                    a_font = font.render(spell_list[g]['name'], 0, (0, 0, 0))
                    if spell_list[g]['name'] in useable_spells:
                        a_font = font.render(spell_list[g]['name'], 0, (0, 0, 255))

                    a_y = (g + 1) * FS[1] * 1.5
                    a_x = params['screen_width'] - 300
                    surface.blit(a_font, (a_x, a_y))
                    font.set_italic(False)

                # Scrolling
                pointer = pg.image.load(cwd + '/imgs/textbox/woa_items1.png')
                pointer.set_colorkey((255, 255, 255))
                if gt == 'Nature' and vs == 1:
                    # Pointer
                    s_x = params['screen_width'] - 350
                    s_y = (msel + 1) * 1.5 * FS[1]
                else:
                    s_x = 375
                    s_y = ii * bck_size[1] + 86 + eq.get_size()[1] + job.get_size()[1]
                surface.blit(pointer, (s_x, s_y), (4 * 32, 3 * 32, 32, 32))
    pg.display.flip()


def select_cast_spell_from_menu(gp, select, mselect):
    """ Remake menu with arrows pointing at different heros

        On enter cure
    """
    cwd = os.getcwd()
    params = settings.params()

    # gp game parameters
    clock = gp['clock']
    music = gp['music']
    heros = gp['char']

    if mselect in [3, 11]:
        v_opt = []
        for i in range(len(heros)):
            v_opt.append(i)
    else:
        v_opt = [0]
    opt = 0
    reading = True
    display_heros_getting_magic(gp, select=opt, v_opt=v_opt)
    while reading:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                reading = False
                pg.quit()
                break
            elif e.type == pg.KEYDOWN:
                # Exit Menu
                if e.key == pg.K_q:
                    return False, None
                if e.key == pg.K_RETURN:
                    return v_opt
                if e.key == pg.K_DOWN:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt += 1
                    if opt == len(heros):
                        opt = 0
                if e.key == pg.K_UP:
                    music.play_sound(music.sound_list('menu'), num=1)
                    opt -= 1
                    if opt == -1:
                        opt = len(heros) - 1
                if mselect not in [3, 11]:
                    v_opt[0] = opt
                display_heros_getting_magic(gp, select=opt, v_opt=v_opt)
        clock.tick(params['frames_per_second'])


def display_heros_getting_magic(gp, select=0, v_opt=[0]):
    """
    """
    MSIZE = 3.5
    cwd = os.getcwd()
    params = settings.params()

    # gp game parameters
    surface = gp['screen']
    font = gp['font']
    clock = gp['clock']
    music = gp['music']
    user_items = gp['items']
    heros = gp['char']

    # Get font height
    FS = font.render('T', 0, (0, 0, 0)).get_size()

    # Display heros
    hn = pg.font.Font('misc/Anonymous_Pro.ttf', params['font_size'] + 4)
    hn.set_underline(True)

    # Black screen
    pg.draw.rect(surface, (0, 0, 0), (0, 0, params['screen_width'], params['screen_height']))

    mx_show_heros = 3
    start = 0
    stop = len(heros)

    if stop > mx_show_heros:
        # if the user cursur is more than the last position
        if select + 1 >= mx_show_heros:
            start = select - mx_show_heros + 1
            stop = select + 1
        else:
            stop = mx_show_heros

    # Item list full width
    bck = pg.image.load(cwd + '/imgs/textbox/paper-dialog2.png')
    bck_size = [params['screen_width'], 240]
    bck = pg.transform.scale(bck, (bck_size[0], bck_size[1]))

    # Menu List
    m_bck = [400, params['screen_height']]
    Mbck = pg.transform.scale(bck, (m_bck[0], m_bck[1]))
    surface.blit(Mbck, (bck_size[0], 0), Mbck.get_rect())
    for i in range(start, stop):
        ii = i - start
        surface.blit(bck, (0, ii * bck_size[1]), bck.get_rect())

        # Char Name
        hero_name = hn.render(heros[i]['name'], 0, (0, 0, 0))
        s_y = ii * bck_size[1] + 8
        surface.blit(hero_name, (100, s_y))

        # Display Image
        ci = dialog.get_char_img(heros[i]['class'])
        cj = pg.image.load(cwd + dialog.get_char_sheets(ci['sheet'])).convert()

        char = pg.transform.rotozoom(cj, 0, MSIZE)
        char.set_colorkey((254, 255, 254))
        if i not in v_opt:
            surface.blit(char, (50, hero_name.get_size()[1] + ii * bck_size[1] + int((bck_size[1] - 180.)/2.)), (ci['pos'][0]*48*MSIZE, ci['pos'][1]*48*MSIZE, (48-1)*MSIZE, (48)*MSIZE))
        else:
            surface.blit(char, (100, hero_name.get_size()[1] + ii * bck_size[1] + int((bck_size[1] - 180.)/2.)), (ci['pos'][0]*48*MSIZE, ci['pos'][1]*48*MSIZE, (48-1)*MSIZE, (48)*MSIZE))

        s_x = 425

        # Char Job
        jb = heros[i]['class']
        if '_' in jb:
            jb = heros[i]['class'].split('_')[0]
        job = font.render(jb.capitalize(), 0, (0, 0, 0))

        # Char HP / MP
        cur_hp = heros[i]['HP']
        cur_mp = heros[i]['MP']
        base = settings.get_base_stats(jb, heros[i]['level'])
        max_hp = base['HP']
        max_mp = base['MP']

        s_y = ii * bck_size[1] + 60
        pg.draw.rect(surface, (0, 0, 0), (s_x, s_y - 8, 126, 26))
        cr = float(cur_hp)/float(max_hp)
        HEALTH = (int(255.*(1.-cr)), int(255. * cr),  0)
        for j in range(1, 101):
            if float(j) <= cr * 100.:
                pg.draw.circle(surface,
                               HEALTH,
                               (s_x + j + 12, s_y + 5), 10, 10)

        HEALTH = font.render(str(cur_hp) + '/' + str(max_hp), 0, (0, 0, 0))
        surface.blit(HEALTH, (s_x - 140, s_y - 10))


        s_y += job.get_size()[1] + 18
        pg.draw.rect(surface, (0, 0, 0), (s_x, s_y - 8, 126, 26))
        cr = float(cur_mp)/float(max_mp)

        HEALTH = (int(255.*(1.-cr)), int(255. * cr), 255)
        for j in range(1, 101):
            if float(j) <= cr * 100.:
                pg.draw.circle(surface,
                               HEALTH,
                               (s_x + j + 12, s_y + 5), 10, 10)
        HEALTH = font.render(str(cur_mp) + '/' + str(max_mp), 0, (0, 0, 0))
        surface.blit(HEALTH, (s_x - 140 , s_y - 10))

        eq = font.render('Gem: ', 0, (0, 0, 0))
        s_y = s_y + eq.get_size()[1] + 8
        surface.blit(eq, (s_x - 140, s_y))

        eq = font.render('None', 0, (255, 0, 0))
        if heros[i]['gem']['name'] is not None:
            eq = font.render(heros[i]['gem']['name'], 0, (0, 0, 255))
        surface.blit(eq, (s_x, s_y))

        if heros[i]['gem']['name'] is not None:
            gt = ge.get_equipment_for_use(ind=heros[i]['gem']['name'])['class']
            gemexp = [10, 30, 80, 180, 380, 880, 1880, 3880, 8880, 18880, 38880]
            cur_exp = heros[i]['gemlvl'][gt]
            cur_skill = 0
            for g in range(len(gemexp)):
                if gemexp[g] > cur_exp:
                    cur_skill = g + 1
                    break
            if cur_exp > 38880:
                cur_skill = len(gemexp) + 1
            eq = font.render(gt.capitalize() +  ' Lv: ' + str(cur_skill), 0, (0, 0, 0))
            s_y = s_y + eq.get_size()[1] + 8
            surface.blit(eq, (s_x-140, s_y))

        for ii in v_opt:
            pointer = pg.image.load(cwd + '/imgs/textbox/woa_items1.png')
            pointer.set_colorkey((255, 255, 255))
            s_x = 50
            s_y = ii * bck_size[1] + 120 - 14
            if ii > 2:
                s_y = 2 * bck_size[1] + 120 - 14
            surface.blit(pointer, (s_x, s_y), (4 * 32, 3 * 32, 32, 32))
    pg.display.flip()


def menu_options():
    menu = ['Items',
            'Magic',
            'Equipment',
            'Gems',
            'Status',
            'Save']
    return menu
