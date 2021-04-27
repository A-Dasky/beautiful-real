import pygame as pg
import src.walls as walls


def zoner(zone):
    """dict of zones and their connections
    """
    d = {'hero_house': {'OUT': [{'zone': 'home_village',    # Next zone
                                 'area': [64, 272, 64, 16], # Left, Top, Width, Height
                                 'load_point': [5, 6],
                                }],
                       }, 
         'home_village': {'OUT': [{'zone': 'hero_house',      # hero house
                                   'area': [160, 128, 64, 16], # Left, Top, Width, Height
                                   'load_point': [3, 5],
                                  },
                                  {'zone': 'world',            # world map
                                   'area': [512, 848, 96, 16],
                                   'load_point': [18, 150],
                                  },
                                  {'zone': 'friends_house',
                                   'area': [416, 164, 64, 16],
                                   'load_point': [4, 8],
                                  },
                                  {'zone': 'home_vill_shops',
                                   'area': [676, 418, 64, 16],
                                   'load_point': [12, 8],
                                  },
                                  {'zone': 'home_vill_shops',
                                   'area': [512, 418, 64, 16],
                                   'load_point': [3, 8],
                                  },
                                  {'zone': 'elders_house',
                                   'area': [32, 512, 64, 16],
                                   'load_point': [6, 8],
                                  },
                                 ],
                         },
         'home_vill_shops': {'OUT':[{'zone': 'home_village',    # Next zone
                                     'area': [64, 304, 96, 16], # Left, Top, Width, Height
                                     'load_point': [17, 15],
                                    },
                                    {'zone': 'home_village',    # Next zone
                                     'area': [352, 304, 96, 16], # Left, Top, Width, Height
                                     'load_point': [22, 15],
                                    },
                                   ],

                             },
         'friends_house':{'OUT': [{'zone': 'home_village',    # Next zone
                                   'area': [96, 336, 64, 16], # Left, Top, Width, Height
                                   'load_point': [13, 7],
                                 }],
                         }, 
         'elders_house':{'OUT': [{'zone': 'home_village',    # Next zone
                                   'area': [128, 304, 96, 16], # Left, Top, Width, Height
                                   'load_point': [2, 19],
                                 }],
                         }, 
         'world': {'OUT': [{'zone': 'home_village',
                            'area': [550, 4666, 64, 64], # Left, Top, Width, Height
                            'load_point': [17, 24],
                           },
                           {'zone': 'cave_no_gem',
                            'area': [1168, 4948, 64, 16], # Left, Top, Width, Height
                            'load_point': [4, 18],
                           },
                           {'zone': 'quiet_forest',
                            'area': [1028, 4564, 16, 64], # Left, Top, Width, Height
                            'load_point': [3, 28],
                           },
                           {'zone': 'quiet_forest',
                            'area': [1440, 4324, 16, 96], # Left, Top, Width, Height
                            'load_point': [72, 15],
                           },
                          ],
                  },
         'cave_no_gem':{'OUT': [{'zone': 'world',
                                       'area': [112, 656, 64, 32], # Left, Top, Width, Height
                                       'load_point': [37, 157],
                                      },
                                     ],
                             },
         'quiet_forest':{'OUT': [{'zone': 'world',
                                  'area': [0, 832, 32, 160], # Left, Top, Width, Height
                                  'load_point': [30, 143],
                                 },
                                 {'zone': 'world',
                                  'area': [2432, 386, 32, 288], # Left, Top, Width, Height
                                  'load_point': [47, 136],
                                 },
                                ],
                             
                             },
          'BLANK': {'OUT': [{'zone': 'BLANK',
                             'area': [100, 100, 100, 100],
                             'load_point': [-32, -32],
                            }
                           ],
                   },
        }
    return d[zone]


def load_zone(zone):
    """load an image of the zone
    """
    z = pg.image.load('zones/' + zone + '.png').convert()
    return z


def get_walls(zone, x, y):
    """load walls in .w file
    """
    wall_list = walls.set_walls('zones/' + zone + '.w', x, y)
    wall = pg.sprite.RenderPlain(wall_list)
    return wall

def get_zones(zone, x, y):
    """
    """
    zone_list = walls.set_zones('zones/' + zone + '.z', x, y)
    z = pg.sprite.RenderPlain(zone_list)
    return z