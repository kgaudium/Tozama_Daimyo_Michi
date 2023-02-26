import msvcrt
import os, time

import settings
import visuals.sprites as sprts
import libs.matrix as mtx
import initialization
import keyboard as kb
import gaudium as g
import copy

import colored


def center_text(text, length=None):
    try:
        return ' ' * int((os.get_terminal_size()[0] - len(text)) / 2) + text if not length else ' ' * int(
        (os.get_terminal_size()[0] - length) / 2) + text

    except OSError:
        return ' ' * int((157 - len(text)) / 2) + text if not length else ' ' * int(
            (157 - length) / 2) + text

def print_spaces(count):
    print('\n' * count)


def render_scene(scene, center=True, is_map=False, center_size=None):
    # scene is 3d matrix (list of 2d sprites)

    # for i in scene:
    #     length = len(i[0])
    #     for j in i:
    #         if len(j) != length:
    #             print(length, '!=', len(j))
    #             # return False

    res = ''

    for line in scene:
        length = len(line[0].split('\n'))
        for i in range(length):
            for sprite in line:
                sprite = sprite.split('\n')

                try:
                    res += sprite[i]
                except IndexError:
                    raise IndexError('Высота спрайтов не совпадает')

            res += '\n'

    if center:
        lst = res.split('\n')
        if is_map:
            lst = list(map(lambda x: center_text(x, settings.MAP_SIZE[1] * settings.MAP_TILE_SIZE[1]), lst))
        elif center_size:
            lst = list(map(lambda x: center_text(x, center_size), lst))
        else:
            lst = list(map(lambda x: center_text(x), lst))

        res = ''
        for i in lst:
            res += i + '\n'

    return res[:-1]


def get_central_logo(logo, color=None, gradient=(220, 50)):
    start_clr, end_clr = gradient
    central_logo = []
    splited_logo = logo.split('\n')

    if color:
        if initialization.is_cmd:
            w = os.get_terminal_size()[0]
            for i in range(len(splited_logo)):
                central_logo += [
                    colored.fg(color) + ' ' * int((w - len(splited_logo[i])) / 2) + splited_logo[i] + colored.fg(
                        'white')]
        else:
            for i in range(len(splited_logo)):
                central_logo += [colored.fg(color) + splited_logo[i] + colored.fg('white')]
    else:
        if initialization.is_cmd:
            w = os.get_terminal_size()[0]
            for i in range(len(splited_logo)):
                central_logo += [colored.fg(
                    f'#{hex(int(start_clr - (i * (start_clr - end_clr) / (len(splited_logo) - 1))))[2:]}0000') + ' ' * int(
                    (w - len(splited_logo[i])) / 2) + splited_logo[i] + colored.fg('white')]
        else:
            for i in range(len(splited_logo)):
                central_logo += [colored.fg(
                    f'#{hex(int(start_clr - (i * (start_clr - end_clr) / (len(splited_logo) - 1))))[2:]}0000') +
                                 splited_logo[i] + colored.fg('white')]

            # print(f'#{hex(int(start_clr - (i * (start_clr - end_clr)/(len(splited_logo)-1))))[2:]}0000')

    return central_logo


def load_main_menu(color=None, logo=sprts.LOGO, slp=0.08, cls=True, gradient=(220, 50)):
    if cls: os.system('cls')

    for i in get_central_logo(logo, color, gradient):
        print(i)
        time.sleep(slp)


def main_menu(pos):
    load_main_menu(logo=sprts.MINI_LOGO, gradient=(220, 130), slp=0)
    pass


def convert_codes_map_to_scene(Map, player_pos=None):
    new_map = copy.deepcopy(Map)
    if player_pos:
        # print(player_pos)
        new_map[player_pos[0]][player_pos[1]] = 5

    res = mtx.zeros((len(new_map), len(new_map[0])))
    for i in range(len(new_map)):
        for j in range(len(new_map[i])):
            res[i][j] = sprts.sprite_codes[new_map[i][j]]

    # print(mtx.print_mtx(new_map))
    return res


def draw_and_wait_for_any_key(scenes, center_sizes, wait=True):
    for i in range(len(scenes)):
        print(render_scene(scenes[i], is_map=False, center_size=center_sizes[i]))

    if wait:
        kb.read_key()


def generate_sprite_from_table(table, print_stats=True):
    scene = ([], [])

    for i in range(len(table[0])):
        if table[0][i] == 0:
            scene[0].append(sprts.empty_table_slot)
        else:
            scene[0].append(str(table[0][i]))

        if table[1][i] == 0:
            scene[1].append(sprts.empty_table_slot)
        else:
            scene[1].append(str(table[1][i]))

    sprite = render_scene(scene, center=False, is_map=False)

    sprite = sprite.split('\n')
    sprite.insert(0, sprts.color_str('┏' + '━' * settings.CARD_WIDTH * settings.CARDS_ON_TABLE + '┓', sprts.table_color))
    sprite.insert(settings.CARD_HEIGHT + 1, sprts.color_str('╍' * settings.CARD_WIDTH * settings.CARDS_ON_TABLE, sprts.table_color))
    sprite.insert(settings.CARD_HEIGHT * 2 + 2, sprts.color_str('┗' + '━' * settings.CARD_WIDTH * settings.CARDS_ON_TABLE + '┛', sprts.table_color))

    for i in range(1, len(sprite)-1):
        if i == 9:
            sprite[i] = sprts.color_str('┣', sprts.table_color) + sprite[i] + sprts.color_str('┫', sprts.table_color)
            continue
        sprite[i] = sprts.color_str('┃', sprts.table_color) + sprite[i] + sprts.color_str('┃', sprts.table_color)

    if print_stats:
        pl_hp = pl_at = en_hp = en_at = 0
        for i in range(len(table[0])):
            if table[0][i] != 0:
                en_hp += table[0][i].health
                en_at += table[0][i].attack

            if table[1][i] != 0:
                pl_hp += table[1][i].health
                pl_at += table[1][i].attack

        # sprite[settings.CARD_HEIGHT // 2 - 1] += '  Total'
        sprite[settings.CARD_HEIGHT // 2] += f'  Attack: {en_at}'
        sprite[settings.CARD_HEIGHT // 2 + 1] += f'  Health: {en_hp}'
        # sprite[settings.CARD_HEIGHT + settings.CARD_HEIGHT // 2 - 1] += '  Total'
        sprite[settings.CARD_HEIGHT + settings.CARD_HEIGHT // 2 + 1] += f'  Attack: {pl_at}'
        sprite[settings.CARD_HEIGHT + settings.CARD_HEIGHT // 2 + 2] += f'  Health: {pl_hp}'

    return '\n'.join(sprite)


def pause(slp=.5):
    while msvcrt.kbhit():
        msvcrt.getch()

    g.slp(slp)
    kb.read_key()
