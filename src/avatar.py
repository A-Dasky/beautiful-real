import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, c='warrior_m'):
        pg.sprite.Sprite.__init__(self)

        #self.fname = 'Images/24x32-characters-big-pack-by-Svetlana-Kushnariova/Heroes/Fighter-M-01.png'
        self.fname = 'chars/' + c + '.png'
        self.sheet = pg.image.load(self.fname).convert()
        self.W = 32
        self.H = 36
        self.image = pg.Surface([self.W, self.H])
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

        self.tmp_dict = {'U1': {'x': 0, 'y': 0},
                         'U2': {'x': self.W, 'y': 0},
                         'U3': {'x': self.W  * 2, 'y': 0},
                         'R1': {'x': 0, 'y': self.H},
                         'R2': {'x': self.W, 'y': self.H},
                         'R3': {'x': self.W  * 2, 'y': self.H},
                         'D1': {'x': 0, 'y': self.H * 2},
                         'D2': {'x': self.W, 'y': self.H * 2},
                         'D3': {'x': self.W  * 2, 'y': self.H * 2},
                         'L1': {'x': 0, 'y': self.H * 3},
                         'L2': {'x': self.W, 'y': self.H * 3},
                         'L3': {'x': self.W  * 2, 'y': self.H * 3}}
        self.change_x = 0
        self.change_y = 0

        self.tick = 10
        self.moving = False

        self.image.set_colorkey((254, 255, 254))


    def get_image(self, dir, moving):
        self.moving = moving
        if self.moving:
            var = 10
            if dir == 'L' or dir == 'R':
                if self.tick < var - 4:
                    self.image.blit(self.sheet, (0,0),
                                    (self.tmp_dict[dir + '1']['x'],
                                    self.tmp_dict[dir + '1']['y'],
                                    self.W, self.H))
                elif (var - 4 <= self.tick  and self.tick < var):
                    self.image.blit(self.sheet, (0,0),
                                    (self.tmp_dict[dir + '2']['x'],
                                    self.tmp_dict[dir + '2']['y'],
                                    self.W, self.H))
                elif (var <= self.tick and self.tick < var + 6):
                    self.image.blit(self.sheet, (0,0),
                                    (self.tmp_dict[dir + '3']['x'],
                                    self.tmp_dict[dir + '3']['y'],
                                    self.W, self.H))
                else:
                    self.image.blit(self.sheet, (0,0),
                                    (self.tmp_dict[dir + '2']['x'],
                                    self.tmp_dict[dir + '2']['y'],
                                    self.W, self.H))
                self.tick += 1
                if self.tick == var * 2:
                    self.tick = 0
            else:
                if self.tick < var:
                    self.image.blit(self.sheet, (0,0),
                                    (self.tmp_dict[dir + '1']['x'],
                                    self.tmp_dict[dir + '1']['y'],
                                    self.W, self.H))
                elif (var <= self.tick  and self.tick < var  * 2):
                    self.image.blit(self.sheet, (0,0),
                                    (self.tmp_dict[dir + '3']['x'],
                                    self.tmp_dict[dir + '3']['y'],
                                    self.W, self.H))
                self.tick += 1
                if self.tick == var * 2:
                    self.tick = 0
        else:
            self.tick = 10
            self.image.blit(self.sheet, (0,0),
                            (self.tmp_dict[dir + '2']['x'],
                            self.tmp_dict[dir + '2']['y'],
                            self.W, self.H))
        # Transparent color
        self.image.set_colorkey((254, 255, 254))
        # Return Image
        return self.image
    
    def move(self, x, y, stop=False):
        if stop:
            self.change_x = x
            self.change_y = y
            return
        self.change_x += x
        self.change_y += y
        return

    def update(self, walls):
        old_x = self.rect.topleft[0]
        old_y = self.rect.topleft[1]

        new_x = old_x + self.change_x
        new_y = old_y + self.change_y

        self.rect.topleft = [new_x, new_y]

        collide = pg.sprite.spritecollide(self, walls, False)
        if (new_x != old_x or new_y != old_y) and not self.moving:
            self.tick += 1
            if self.tick > 20:
                self.tick = 0
        if collide:
            self.rect.topleft = [old_x, old_y]

    def change_zone(self, zones, shift_x, shift_y):
        # Check OUT
        o = zones['OUT']
        for i in range(len(o)):
            area = o[i]['area']
            area[0] += shift_x
            area[1] += shift_y
            # If within area
            bot = self.rect.bottom >= area[1] and self.rect.bottom <= area[1] + area[3]
            top = self.rect.top <= area[1] + area[3] and self.rect.top >= area[1]

            left = self.rect.left >= area[0] and self.rect.left <= area[0] + area[2]
            right = self.rect.right <= area[0] + area[2] and self.rect.right >= area[0]

            cz = [bot and right, # bottom right
                  top and right, # top right
                  bot and left,  # bottom left
                  top and left]  # top left
            if True in cz:
                # change zone
                return o[i]
        return None

    def game_event(self, zone, shift_x, shift_y):
        for i in range(len(zone)):
            area = zone[i]['area']
            area[0] *= 32
            area[0] += shift_x
            area[1] *= 32
            area[1] += shift_y
            # If within area
            bot = self.rect.bottom >= area[1] and self.rect.bottom <= area[1] + area[3]
            top = self.rect.top <= area[1] + area[3] and self.rect.top >= area[1]

            left = self.rect.left >= area[0] and self.rect.left <= area[0] + area[2]
            right = self.rect.right <= area[0] + area[2] and self.rect.right >= area[0]

            cz = [bot and right, # bottom right
                  top and right, # top right
                  bot and left,  # bottom left
                  top and left]  # top left

            if True in cz:
                return zone[i]['action']
        return None


    def game_prevent(self, area):
        """check to see if hero enters game prevent area
        """
        bot = self.rect.bottom >= area[1] and self.rect.bottom <= area[1] + area[3]
        top = self.rect.top <= area[1] + area[3] and self.rect.top >= area[1]

        left = self.rect.left >= area[0] and self.rect.left <= area[0] + area[2]
        right = self.rect.right <= area[0] + area[2] and self.rect.right >= area[0]

        cz = [bot and right, # bottom right
              top and right, # top right
              bot and left,  # bottom left
              top and left]  # top left

        if True in cz:
            return True
        return False



class tmp_npc(pg.sprite.Sprite):
    def __init__(self, x, y, c):
        pg.sprite.Sprite.__init__(self)

        self.fname = 'chars/' + c + '.png'
        self.sheet = pg.image.load(self.fname).convert()
        self.W = 32
        self.H = 36
        self.image = pg.Surface([self.W, self.H])
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

        self.tmp_dict = {'U1': {'x': 0, 'y': 0},
                         'U2': {'x': self.W, 'y': 0},
                         'U3': {'x': self.W  * 2, 'y': 0},
                         'R1': {'x': 0, 'y': self.H},
                         'R2': {'x': self.W, 'y': self.H},
                         'R3': {'x': self.W  * 2, 'y': self.H},
                         'D1': {'x': 0, 'y': self.H * 2},
                         'D2': {'x': self.W, 'y': self.H * 2},
                         'D3': {'x': self.W  * 2, 'y': self.H * 2},
                         'L1': {'x': 0, 'y': self.H * 3},
                         'L2': {'x': self.W, 'y': self.H * 3},
                         'L3': {'x': self.W  * 2, 'y': self.H * 3}}
        self.change_x = 0
        self.change_y = 0

        self.tick = 10
        self.moving = False

        self.image.set_colorkey((254, 255, 254))


    def get_image(self, dir, moving):
        self.moving = moving
        if self.moving:
            var = 10
            if dir == 'L' or dir == 'R':
                if self.tick < var - 4:
                    self.image.blit(self.sheet, (0,0),
                                    (self.tmp_dict[dir + '1']['x'],
                                    self.tmp_dict[dir + '1']['y'],
                                    self.W, self.H))
                elif (var - 4 <= self.tick  and self.tick < var):
                    self.image.blit(self.sheet, (0,0),
                                    (self.tmp_dict[dir + '2']['x'],
                                    self.tmp_dict[dir + '2']['y'],
                                    self.W, self.H))
                elif (var <= self.tick and self.tick < var + 6):
                    self.image.blit(self.sheet, (0,0),
                                    (self.tmp_dict[dir + '3']['x'],
                                    self.tmp_dict[dir + '3']['y'],
                                    self.W, self.H))
                else:
                    self.image.blit(self.sheet, (0,0),
                                    (self.tmp_dict[dir + '2']['x'],
                                    self.tmp_dict[dir + '2']['y'],
                                    self.W, self.H))
                self.tick += 1
                if self.tick == var * 2:
                    self.tick = 0
            else:
                if self.tick < var:
                    self.image.blit(self.sheet, (0,0),
                                    (self.tmp_dict[dir + '1']['x'],
                                    self.tmp_dict[dir + '1']['y'],
                                    self.W, self.H))
                elif (var <= self.tick  and self.tick < var  * 2):
                    self.image.blit(self.sheet, (0,0),
                                    (self.tmp_dict[dir + '3']['x'],
                                    self.tmp_dict[dir + '3']['y'],
                                    self.W, self.H))
                self.tick += 1
                if self.tick == var * 2:
                    self.tick = 0
        else:
            self.tick = 10
            self.image.blit(self.sheet, (0,0),
                            (self.tmp_dict[dir + '2']['x'],
                            self.tmp_dict[dir + '2']['y'],
                            self.W, self.H))
        # Transparent color
        self.image.set_colorkey((254, 255, 254))
        # Return Image
        return self.image