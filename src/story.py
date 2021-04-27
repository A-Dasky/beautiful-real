import os
import pygame as pg
import src.dialog as dialog
import src.settings as settings

def story_prevent(ind):
    """Things that prevent the story from progressing, (i.e., turn around
    with text like `we shouldn't go there`)

    Each index lists all the things that `block` the game from progressing

    This is needed for each step in the game...
    Probably a smarter way to do it, like the alt_story (see functions below)
    """
    ev = [# 0  Talk to Friends
          {'locs': ['home_village'],
           'positions': [[496, 832, 128, 32]],
           'actions': [
                       [{'text': {'char': dialog.get_char_img('warrior_M'),
                                  'content': get_prevent_story_dialog(0),
                                 }},
                        {'move': {'DIR': 'U',
                                  'STEPS': 2
                                 }}
                       ],
                      ]
          }, #1 Talk To Elders
          {'locs': ['home_village'],
           'positions': [[496, 832, 128, 32]],
           'actions': [
                       [{'text': {'char': dialog.get_char_img('warrior_M'),
                                  'content': get_prevent_story_dialog(1),
                                 }},
                        {'move': {'DIR': 'U',
                                  'STEPS': 2
                                 }}
                       ],
                      ]
          }, #2 Talk to Rival
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          }, #3 Get Pickaxe
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          }, #4 Get Gem 1
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          }, #5 Get Gem 2
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          }, #6 Get Memory Gem
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          }, #7 Get Memory Gem 2
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          }, #8 Battle Rival (Bezerker) at enterance
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          }, #9 Return to Village Elders
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
          {'locs': [''],
           'positions': [[-1, -1, 1, 1]],
          },
         ]
    return ev[ind]



def get_prevent_story_dialog(ind):
    dia = ['(Hmmm. I should probably find the others first...)',
           '(I cannot leave until I talk to the elders...)',
          ]
    return dia[ind]


def make_text_dialog(av, d):
    if av == '':
        return {'text': {'char': '',
                     'content': get_event_story_dialog(d)}}
    return {'text': {'char': dialog.get_char_img(av),
                     'content': get_event_story_dialog(d)}}


def story_event(ind):
    """Story to progress things
    """
    ev = {}
    f = os.getcwd() + '/story/cs' + str(ind) + '.txt'
    with open(f, 'r') as r:
        fin = r.read()
    fin = fin.split('\n')
    ac = 0
    for line in fin:
        if r'locs:' in line:
            ev['locs'] = []
            line = line.strip(r'locs:')
            line = line.strip()
            if '-' in line:
                line = line.split('-')
            else:
                line = [line]
            for i in range(len(line)):
                line[i] = line[i].rstrip().lstrip()
                ev['locs'].append(line[i])
        if r'positions:' in line:
            ev['positions'] = []
            line = line.strip(r'positions:')
            if '|' in line:
                line = line.split('|')
            else:
                line = [line]
            for i in range(len(line)):
                ev['positions'].append([])
                line[i] = line[i].lstrip().rstrip()
                line[i] = line[i].split(' ')
                for j in range(len(line[i])):
                    line[i][j] = int(float(line[i][j]))
                    ev['positions'][-1].append(line[i][j])
            print(ev['positions'])
        if r'show:' in line:
            ev['show'] = []
            line = line.strip(r'show:')
            if '-' in line:
                line = line.split('-')
            else:
                line = [line]
            for i in range(len(line)):
                line[i] = line[i].lstrip().rstrip().split(' ')
                ev['show'].append({'IMG': line[i][0], 'POS': [int(float(line[i][1])), int(float(line[i][2]))]})
        if r'actions' in line:
            if 'actions' not in ev:
                ev['actions'] = [[]]
            else:
                ac += 1
                ev['actions'].append([])
            continue
        if r'inc:' in line:
            ev['actions'][ac].append({'inc': 1})
        if r'fade:' in line:
            ev['actions'][ac].append({'fade': True})
        if r'flash:' in line:
            ev['actions'][ac].append({'flash': True})
        if r'sound:' in line:
            line = line.rstrip().split()
            ev['actions'][ac].append({'sound': line[-1]})
        if r'music:' in line:
            line = line.split()
            ev['actions'][ac].append({'music': line[-1]})
        if r'add_char:' in line:
            line = line.strip(r'add_char:')
            line = line.strip()
            ev['actions'][ac].append({'add_char': line})
        if r'add_equipment:' in line:
            line = line.strip(r'add_equipment:')
            line = line.strip()
            ev['actions'][ac].append({'add_equipment': line})
        if r'make:' in line:
            line = line.strip(r'make:')
            line = line.split('-')
            POS = line[1].split(',')
            ev['actions'][ac].append({'make': {'CHAR': line[0].strip(), 'POS': [int(float(POS[0])), int(float(POS[1]))], 'DIR': line[2].strip()}})
        if r'move:' in line:
            line = line.strip(r'move:')
            line = line.split('-')
            ev['actions'][ac].append({'move': {'STEPS': int(float(line[1])),
                                               'DIR': line[0].strip()
                                              }
                                     }
                                    )
        if r'text:' in line:
            line = line.strip(r'text:')
            line = line.split('-')
            AV = get_char_attr(line[0].strip())
            if AV['name'] is '':
                ev['actions'][ac].append({'text': {'char': '', 'content': line[1]}})
            else:
                ev['actions'][ac].append({'text': {'char': dialog.get_char_img(line[0].strip()), 'content': AV['name'] + ': ' + line[1].lstrip()}})
        if r'cs:' in line:
            line = line.strip(r'cs:')
            line = line.lstrip().rstrip().split(' ')
            ev['actions'][ac].append({'cs': {'IMG': line[0].strip(), 'POS': [int(float(line[1])), int(float(line[2]))]}})
        if r'zone:' in line:
            line = line.strip(r'zone:')
            line = line.lstrip().rstrip().split(' ')
            ev['actions'][ac].append({'zone': {'loc': line[0].strip(), 'POS': [int(float(line[1])), int(float(line[2]))]}})
    return ev


def get_char_attr(c):
    """
    """
    a = {'monk_F': {'name': 'Melhay',
                    'text_img': '',
                    'av_img': '',},
         'ranger_M': {'name': 'Myhal',
                      'text_img': '',
                      'av_img': '',},
         'warrior_M': {'name': 'Kralean',
                       'text_img': '',
                       'av_img': '',},
         'bezerk_M': {'name': 'Heiral',
                      'text_img': '',
                      'av_img': '',},
         'soldier_M': {'name': '',
                      'text_img': '',
                      'av_img': '',},
         'king_M': {'name': 'Tolen',
                      'text_img': '',
                      'av_img': '',},
         'bard_M': {'name': 'Rasamus',
                      'text_img': '',
                      'av_img': '',},
         'princess_F': {'name': 'Evlee',
                      'text_img': '',
                      'av_img': '',},
         'old_M': {'name': 'Village Patriarch',
                      'text_img': '',
                      'av_img': '',},
         'old_F': {'name': 'Village Matriarch',
                      'text_img': '',
                      'av_img': '',},
         'princess_O': {'name': 'Princess Selell',
                        'text_img': '',
                        'av_img': '',},
         'soldier_M': {'name': 'Knight',
                       'text_img': '',
                       'av_img': '',},
         }
    if c in a:
        return a[c]
    return {'name': c, 'text_img': None, 'av_img': None}


def alt_story(ind, step):
    """Things that change while the story progresses

    positions: Position of event
    til: do text until mission
    gtext: get the alt text from get_alt_story_dialog
    utext: which character is speaking, leave blank for non chars
    itext: images to show

    """
    ev = {'elders_house': {'positions': [[0, 176, 160, 64]],
                           'til': [[1, 'n']],
                           'gtext': [[0, 1]],
                           'utext': [['', '']]
                          },
         }
    if ind in ev:
        return ev[ind]
    return None



def get_alt_story_dialog(ind):
    dia = ['Village Matriarch: I know you are excited about your big day but we should wait for everyone to arrive before we begin.',
           'Village Matriarch: Run along now. Your trial has begun.  This is an exciting time for youth, but go prepared.'
          ]
    return dia[ind]


def make_alt_dialog(av, d):
    if av == '':
        return {'text': {'char': '',
                         'content': get_alt_story_dialog(d)}}
    return {'text': {'char': dialog.get_char_img(av),
                     'content': get_alt_story_dialog(d)}}