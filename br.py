import os
import numpy as np
import pygame as pg

import src.settings as settings
import src.zone as zones
import src.avatar as avatar
import src.walls as walls
import src.music as music
import src.events as ge
import src.dialog as dialog
import src.menu as menu
import src.story as story


SQ = 32
MSIZE = 3.5


def run():
    """Run game
    """

    pg.init()

    # Get game params
    params = settings.params()

    h2 = params['screen_height'] / 2
    w2 = params['screen_width'] / 2


    # init clock
    clock = settings.get_game_clock()
    screen = settings.get_screen(params)
    screen.set_alpha(0)

    # init font
    font = pg.font.Font('misc/Anonymous_Pro.ttf', params['font_size'])

    # Select from menu (eventually)
    new_game = True
    if new_game:
        game = settings.new_game()

    zone = zones.load_zone(game['zone'])
    r = settings.get_screen_rect(zone)

    shift_x, shift_y = settings.get_screen_shift(zone)
    # =============================================
    tmp_x = game['x'] * SQ
    tmp_y = game['y'] * SQ

    shift_x, shift_y = settings.load_shift_zone(r, shift_x, shift_y, tmp_x, tmp_y)

    # get zone walls
    wall = zones.get_walls(game['zone'], shift_x, shift_y)

    # player starting point and direction
    DIR = 'D'
    player = avatar.Player(tmp_x + shift_x, tmp_y + shift_y)
    # =============================================

    # Music
    song = music.music_list(game['zone'])
    music.play_music(song)

    player.get_image(DIR, False)

    movingSprites = pg.sprite.RenderPlain((player))

    moving = False
    play = True

    fade_out = False
    fade_in = False
    alpha = 255
    event_trigger = False
    while play:
        screen.fill((0, 0, 0))
        screen.blit(zone, (shift_x, shift_y), zone.get_rect())

        for e in pg.event.get():
            if e.type == pg.QUIT:
                play = False
                continue

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_LEFT:
                    moving = True
                    DIR = 'L'
                    player.move(-params['speed'], 0)
                elif e.key == pg.K_RIGHT:
                    moving = True
                    DIR = 'R'
                    player.move(params['speed'], 0)
                elif e.key == pg.K_UP:
                    moving = True
                    DIR = 'U'
                    player.move(0, -params['speed'])
                elif e.key == pg.K_DOWN:
                    moving = True
                    DIR = 'D'
                    player.move(0, params['speed'])
                elif e.key == pg.K_q:
                    play = False
                    continue
                elif e.key == pg.K_m:
                    gp = {'screen': screen, 'music': music, 'clock': clock, 'font': font, 'player': player,
                          'items': game['items'], 'gold': game['gold'], 'char': game['char']}
                    menu.show_menu(gp)
                    del gp

                # check is changing dialog in zone
                action = story.alt_story(game['zone'], game['mission'])
                if action is not None:
                    if e.key == pg.K_RETURN:
                        for i in range(len(action['positions'])):
                            aa = action['positions'][i]
                            aa[0] += shift_x
                            aa[1] += shift_y
                            pg.draw.rect(screen, (0, 255, 255), aa)

                            # if within the box
                            if player.game_prevent(aa):
                                til = action['til'][i]
                                cm = 0
                                for j in range(len(til)):
                                    if til[j] == 'n':
                                        cm = len(til) - 1
                                        break
                                    if game['mission'] < til[j]:
                                        cm = j
                                        break
                                dialog.blit_text(screen, story.make_alt_dialog(action['utext'][i][cm],
                                                                               action['gtext'][i][cm])['text'],
                                                 (params['text_padding'], params['text_padding']),
                                                 font, imgs_to_blit=[movingSprites])


                action = player.game_event(ge.reoccuring_events(game['zone']), shift_x, shift_y)
                if action is not None and not event_trigger and e.key in [pg.K_RETURN, pg.K_SPACE]:
                    # do not repeat event unless action allows it without zoning
                    event_trigger = True
                    for i in range(len(action)):
                        if 'repeat' in action[i]:
                            event_trigger = False
                            continue
                        if 'text' in action[i]:
                            dialog.blit_text(screen, action[i]['text'],
                                             (params['text_padding'], params['text_padding']),
                                             font,
                                             imgs_to_blit=[movingSprites])
                            reading = True
                            while reading:
                                for sub_event in pg.event.get():
                                    if sub_event.type == pg.QUIT:
                                        play = False
                                        reading = False
                                        break
                                    elif sub_event.type == pg.KEYDOWN:
                                        if sub_event.key in [pg.K_RETURN, pg.K_SPACE]:
                                            reading = False
                                            break
                                clock.tick(params['frames_per_second'])
                        if 'rest' in action[i]:
                            # Not the best way but... 
                            zp = {'zone': zone, 'name': game['zone'], 'x': shift_x, 'y': shift_y}
                            gp = {'screen': screen, 'music': music, 'clock': clock, 'font': font, 'player': player, 'DIR': DIR}
                            ge.player_rest(gp, zp, cost=action[i]['rest']['cost'], itb=[movingSprites])
                            del gp
                            del zp
                            game = ge.restore_health(game)
                        if 'shop' in action[i]:
                            zp = {'zone': zone, 'name': game['zone'], 'x': shift_x, 'y': shift_y}
                            gp = {'screen': screen, 'music': music, 'clock': clock, 'font': font,
                                  'player': player, 'DIR': DIR, 'items': game['items'], 'gold': game['gold'],
                                  'char': game['char']}
                            game['gold'] = ge.player_shop(gp, zp, action[i]['shop'], itb=[movingSprites])
                            del gp
                            del zp
                        #    print(game['gold'], game['items'])
            elif e.type == pg.KEYUP:
                moving = False
                if e.key == pg.K_LEFT:
                    DIR = 'L'
                elif e.key == pg.K_RIGHT:
                    DIR = 'R'
                elif e.key == pg.K_UP:
                    DIR = 'U'
                elif e.key == pg.K_DOWN:
                    DIR = 'D'
                player.move(0, 0, stop=True)
            print(player.rect.topleft)
        # Check if the story can proceed
        action = story.story_prevent(game['mission'])
        
        # If the current zone has any preventable actions
        if game['zone'] in action['locs']:
            for h in range(len(action['locs'])):
                if game['zone'] == action['locs'][h]:
                    aa = action['positions'][h]
                    aa[0] += shift_x
                    aa[1] += shift_y
                    pg.draw.rect(screen, (0, 0, 255), aa)
                    # Text is displayed need to move to "get out" of event
                    if player.game_prevent(aa):
                        for a in action['actions'][h]:
                            if a.keys()[0] == 'text':
                                dialog.blit_text(screen, a['text'],
                                                 (params['text_padding'], params['text_padding']),
                                                 font,
                                                 imgs_to_blit=[movingSprites])
                            if a.keys()[0] == 'move':
                                td = a['move']['STEPS'] * 32
                                DIR = a['move']['DIR']
                                sd = 0
                                moving = True
                                while True:
                                    player.move(0, 0, stop=True)
                                    player.get_image(DIR, moving).get_rect()
                                    if sd >= td:
                                        break
                                    screen.fill((0, 0, 0))
                                    screen.blit(zone, (shift_x, shift_y), zone.get_rect())
                                    if DIR == 'L':
                                        player.move(-params['speed'], 0)
                                    elif DIR == 'R':
                                        player.move(params['speed'], 0)
                                    elif DIR == 'U':
                                        player.move(0, -params['speed'])
                                    elif DIR == 'D':
                                        player.move(0, params['speed'])
                                    sd += params['speed']
                                    player.update(wall)

                                    px, py = settings.get_move_background(zone, shift_x, shift_y, 
                                                                          player.rect.top,
                                                                          player.rect.left)
                                    if py != shift_y:
                                        if DIR == 'U':
                                            player.rect.top += params['speed']
                                            shift_y += params['speed']
                                            if shift_y > 0:
                                                shift_y = 0
                                            else:
                                                walls.update_walls(wall, 0, params['speed'])
                                        if DIR == 'D':
                                            player.rect.top -= params['speed']
                                            shift_y -= params['speed']
                                            if shift_y < h2 - r.height:
                                                shift_y = h2 - r.height
                                            else:
                                                walls.update_walls(wall, 0, -params['speed'])
                                    if px != shift_x:
                                        if DIR == 'R':
                                            player.rect.left -= params['speed']
                                            shift_x -= params['speed']
                                            walls.update_walls(wall, -params['speed'], 0)
                                        if DIR == 'L':
                                            player.rect.left += params['speed']
                                            shift_x += params['speed']
                        #                    if shift_x > 0:
                        #                        shift_x = 0
                        #                    else:
                                            walls.update_walls(wall, params['speed'], 0)
                                    movingSprites.draw(screen)
                                    pg.display.flip()
                                    clock.tick(params['frames_per_second'])

                                continue


        # Check if story
        CZ = False
        action = story.story_event(game['mission'])
        # If the current zone has any story lines
        if game['zone'] in action['locs']:
            for h in range(len(action['locs'])):
                if game['zone'] == action['locs'][h]:
                    aa = action['positions'][h]

                    aa[0] += shift_x
                    aa[1] += shift_y
                    pg.draw.rect(screen, (0, 0, 255), aa)

                    # Show images that are part of storyline
                    if 'show' in action:
                        tmp_img = pg.image.load(os.getcwd() + '/imgs/story/' + action['show'][h]['IMG'] + '.png').convert()
                        tmp_img.set_colorkey((255, 174, 201))
                        screen.blit(tmp_img,
                                    (action['show'][h]['POS'][0] + shift_x,
                                        action['show'][h]['POS'][1] + shift_y),
                                    tmp_img.get_rect())

                    # See if player reached story_event
                    IN_CS = False
                    if player.game_prevent(aa):
                        tmp_ch = {}
                        for a in action['actions'][h]:
                            if a.keys()[0] == 'text':
                                dialog.blit_text(screen, a['text'],
                                                 (params['text_padding'], params['text_padding']),
                                                 font,
                                                 imgs_to_blit=[movingSprites],
                                                 char_pos=player.rect.topleft)
                                reading = True
                                while reading:
                                    for sub_event in pg.event.get():
                                        if sub_event.type == pg.QUIT:
                                            play = False
                                            reading = False
                                            break
                                        elif sub_event.type == pg.KEYDOWN:
                                            if sub_event.key in [pg.K_RETURN, pg.K_SPACE]:
                                                reading = False
                                                break
                                    clock.tick(params['frames_per_second'])
                            if a.keys()[0] == 'inc':
                                game['mission'] += a['inc']
                            if a.keys()[0] == 'music':
                                if a['music'] is not song:
                                    song = music.music_list(a['music'])
                                    music.play_music(song)
                            if a.keys()[0] == 'fade':
                                alpha = 255
                                while alpha > -1:
                                    screen.fill((0, 0, 0))
                                    if not IN_CS:
                                        screen.blit(zone, (shift_x, shift_y), zone.get_rect())
                                        zone.set_alpha(alpha)
                                    else:
                                        screen.blit(tmp_img, (tmp_pos), tmp_img.get_rect())
                                        tmp_img.set_alpha(alpha)
                                    for tt in tmp_ch:
                                        tmp_av = pg.sprite.RenderPlain((tmp_ch[tt]))
                                        tmp_av.draw(screen)
                                    movingSprites.draw(screen)
                                    alpha -= 15
                                    clock.tick(params['frames_per_second'])
                                    pg.display.flip()

                                screen.fill((0, 0, 0))
                                screen.blit(zone, (shift_x, shift_y), zone.get_rect())
                                zone.set_alpha(255)
                                # Display only Hero after
                                movingSprites.draw(screen)
                                clock.tick(params['frames_per_second'])
                                pg.display.flip()
                            if a.keys()[0] == 'flash':
                                alpha = 255
                                flash_img = pg.image.load(os.getcwd() + '/zones/FLASH.png').convert()
                                while alpha > -1:
                                    screen.fill((0, 0, 0))
                                    screen.blit(zone, (shift_x, shift_y), zone.get_rect())
                                    flash_img.set_alpha(alpha)
                                    screen.blit(flash_img, (0, 0), flash_img.get_rect())
                                    alpha -= 5
                                    clock.tick(params['frames_per_second'])
                                    pg.display.flip()
                            if a.keys()[0] == 'add_char':
                                for c in range(len(game['not_char'])):
                                    if game['not_char'][c]['name'] == a['add_char']:
                                        # Add to playable characters
                                        game['char'].append(game['not_char'][c])
                                        # Remove from hidden char list
                                        game['not_char'].pop(c)
                                        break
                            if a.keys()[0] == 'add_equipment':
                                game['items'].append(a['add_equipment'])
                                print(game['items'])
                            if a.keys()[0] == 'make':
                                nc_x, nc_y = a['make']['POS']
                                nc_c = a['make']['CHAR']

                                # Make image
                                tmp_ch[nc_c] = avatar.tmp_npc(nc_x + shift_x, nc_y + shift_y, nc_c)

                                # Make direction
                                tmp_ch[nc_c].get_image(a['make']['DIR'], False)

                                # show image
                                screen.blit(tmp_ch[nc_c].image, (tmp_ch[nc_c].rect.topleft), tmp_ch[nc_c].rect)

                                tmp_av = pg.sprite.RenderPlain((tmp_ch[nc_c]))
                                tmp_av.draw(screen)

                                pg.display.flip()
                            if a.keys()[0] == 'sound':
                                music.play_sound(music.sound_list(a['sound']), num=1)
                            if a.keys()[0] == 'move':
                                td = a['move']['STEPS'] * 32
                                DIR = a['move']['DIR']
                                sd = 0
                                moving = True
                                while True:
                                    player.move(0, 0, stop=True)
                                    player.get_image(a['move']['DIR'], moving).get_rect()
                                    if sd >= td:
                                        break
                                    screen.fill((0, 0, 0))
                                    screen.blit(zone, (shift_x, shift_y), zone.get_rect())
                                    if DIR == 'L':
                                        player.move(-params['speed'], 0)
                                    elif DIR == 'R':
                                        player.move(params['speed'], 0)
                                    elif DIR == 'U':
                                        player.move(0, -params['speed'])
                                    elif DIR == 'D':
                                        player.move(0, params['speed'])
                                    sd += params['speed']
                                    player.update(wall)

                                    px, py = settings.get_move_background(zone, shift_x, shift_y, 
                                                                          player.rect.top,
                                                                          player.rect.left)
                                    if py != shift_y:
                                        if DIR == 'U':
                                            player.rect.top += params['speed']
                                            shift_y += params['speed']
                                            if shift_y > 0:
                                                shift_y = 0
                                            else:
                                                walls.update_walls(wall, 0, params['speed'])
                                        if DIR == 'D':
                                            player.rect.top -= params['speed']
                                            shift_y -= params['speed']
                                            if shift_y < h2 - r.height:
                                                shift_y = h2 - r.height
                                            else:
                                                walls.update_walls(wall, 0, -params['speed'])
                                    if px != shift_x:
                                        if DIR == 'R':
                                            player.rect.left -= params['speed']
                                            shift_x -= params['speed']
                                            walls.update_walls(wall, -params['speed'], 0)
                                        if DIR == 'L':
                                            player.rect.left += params['speed']
                                            shift_x += params['speed']
                        #                    if shift_x > 0:
                        #                        shift_x = 0
                        #                    else:
                                            walls.update_walls(wall, params['speed'], 0)
                                    screen.fill((0, 0, 0))
                                    screen.blit(zone, (shift_x, shift_y), zone.get_rect())
                                    movingSprites.draw(screen)
                                    pg.display.flip()
                                    clock.tick(params['frames_per_second'])
                                continue
                            if a.keys()[0] == 'cs':
                                IN_CS = True
                                screen.fill((0, 0, 0))
                                tmp_img = pg.image.load(os.getcwd() + '/zones/' + a['cs']['IMG'] + '.png').convert()
                                tmp_pos = [a['cs']['POS'][0], a['cs']['POS'][1]]
                                screen.blit(tmp_img, (tmp_pos), tmp_img.get_rect())
                                pg.display.flip()
                                clock.tick(params['frames_per_second'])
                                player.rect.topleft = [-32, -32]
                                shift_x = 0
                                shift_y = 0
                            if a.keys()[0] == 'zone':
                                cs_zone = a['zone']['loc']
                                zone = zones.load_zone(cs_zone)
                                game['zone'] = cs_zone
                                new_pos = a['zone']['POS']
                                CZ = True


        player.get_image(DIR, moving).get_rect()
        player.update(wall)
        if CZ and game['zone'] == 'BLANK':
            player.rect.topleft = [-32, -32]
            shift_x = 0
            shift_y = 0
            #            print(player.rect.topleft, shift_x, shift_y, zone)
        elif CZ:
            # Get shift correct shift_x and shift_y that will load player at correct position
            player.rect.topleft = new_pos
            #            print(player.rect.topleft, shift_x, shift_y, zone)
        new_zone = player.change_zone(zones.zoner(game['zone']), shift_x, shift_y)
        if new_zone is not None:
            # Fade
            alpha = 255
            while alpha > 0:
                screen.fill((0, 0, 0))
                screen.blit(zone, (shift_x, shift_y), zone.get_rect())
                moving = False
                player.get_image(DIR, moving).get_rect()
                player.move(0, 0, stop=True)
                zone.set_alpha(alpha)
                alpha -= 10

                for e in pg.event.get():
                    if e.type == pg.QUIT:
                        play = False
                        continue

                    if e.type == pg.KEYDOWN:
                        if e.key == pg.K_q:
                            play = False
                            continue
                clock.tick(params['frames_per_second'])
                pg.display.flip()

            # Get name of new zone
            game['zone'] = new_zone['zone']

            # load new zone
            zone = zones.load_zone(game['zone'])

            tmp_x, tmp_y = new_zone['load_point']

            # get zone shift
            shift_x, shift_y = settings.get_screen_shift(zone)

            # ==================================================
            #                start load screen mess
            # ==================================================
            r = settings.get_screen_rect(zone)

            tmp_x *= SQ
            tmp_y *= SQ

            shift_x, shift_y = settings.load_shift_zone(r, shift_x, shift_y, tmp_x, tmp_y)

            # get zone walls
            wall = zones.get_walls(game['zone'], shift_x, shift_y)

            # get player starting point
            player.rect.top = tmp_y + shift_y
            player.rect.left = tmp_x + shift_x

            # ==================================================
            #                End load screen mess
            # ==================================================

            # Music
            if music.music_list(game['zone']) is not song:
                song = music.music_list(game['zone'])
                music.play_music(song)

            event_trigger = False

        if moving:
            px, py = settings.get_move_background(zone, shift_x, shift_y, 
                                                  player.rect.top,
                                                  player.rect.left)
            if py != shift_y:
                if DIR == 'U':
                    player.rect.top += params['speed']
                    shift_y += params['speed']
                    if shift_y > 0:
                        shift_y = 0
                    else:
                        walls.update_walls(wall, 0, params['speed'])
                if DIR == 'D':
                    player.rect.top -= params['speed']
                    shift_y -= params['speed']
                    if shift_y < h2 - r.height:
                        shift_y = h2 - r.height
                    else:
                        walls.update_walls(wall, 0, -params['speed'])
            if px != shift_x:
                if DIR == 'R':
                    player.rect.left -= params['speed']
                    shift_x -= params['speed']
                    if shift_x < w2 - r.width:
                        shift_x = w2 - r.width
                    else:
                        walls.update_walls(wall, -params['speed'], 0)
                if DIR == 'L':
                    player.rect.left += params['speed']
                    shift_x += params['speed']
                    if shift_x > 0:
                        shift_x = 0
                    else:
                        walls.update_walls(wall, params['speed'], 0)

        for zz in zones.zoner(game['zone'])['OUT']:
            aa = zz['area']
            aa[0] += shift_x
            aa[1] += shift_y
            pg.draw.rect(screen, (0, 0, 0), aa)
        for ww in wall:
            pg.draw.rect(screen, (255, 0, 0), ww)

        for ee in ge.reoccuring_events(game['zone']):
            aa = ee['area']
            aa[0] *= 32
            aa[0] += shift_x
            aa[1] *= 32
            aa[1] += shift_y

            pg.draw.rect(screen, (0, 255, 0), aa)

        movingSprites.draw(screen)
        pg.display.flip()

        if music.music_list(game['zone']) is not song:
            song = music.music_list(game['zone'])
            music.play_music(song)

        # 30 frames per second
        clock.tick(params['frames_per_second'])

    pg.quit()
    return


if __name__ == '__main__':
    run()
