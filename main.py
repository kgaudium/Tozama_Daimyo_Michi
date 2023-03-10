import msvcrt
import os
import random

import fight
import settings
import visuals.draw as draw, visuals.sprites as sprites, initialization, world_generator as gen
import libs.matrix as mtx

from pynput.keyboard import Key, Listener
import keyboard as kb
import gaudium as g
import colored

import controls

Map = gen.generate_level_3()
# Table = fight.empty_table()

# Player attrs
player_position = (settings.MAP_SIZE[0] - 1, int(settings.MAP_SIZE[1] / 2))
player_money = random.randint(25, 45)
# player_money = 1000
available_troops = list(fight.DEFAULT_TROOPS)
passive_spells = []

current_enemy = fight.Enemy((.3, .3, .3))
steps_from_fight = 0
levels_from_fight = 0
collected_money = player_money
victories = [0, 0, 0]  # common, boss, main boss
loses = 0
draws = 0

in_shop = False
is_player_turn = False
is_fight = False
do_cycle = True
on_level = True
game_over = False
game_win = False


def ext(code=0):
    global on_level, do_cycle
    print('Bye bye!')
    on_level = False
    do_cycle = False
    listener.stop()
    # g.cls()
    exit(code)

def print_stats():
    print(draw.center_text('Your Statistics'))
    draw.print_spaces(1)
    print(draw.render_scene([[f'Current Balance: {player_money}'],
                             [f'Collected Money: {collected_money}'],
                             [''],
                             [
                                 f"Available Troops: {', '.join(map(lambda x: x().__repr__().strip(), available_troops))}"],
                             [f"Available Spells: {', '.join(map(lambda x: x().__repr__().strip(), passive_spells))}"],
                             [''],
                             ['Victories'],
                             [f'    Common Enemy: {victories[0]}'],
                             [f'    Boss: {victories[1]}'],
                             [f'    Main Boss: {victories[2]}'],
                             [''],
                             [f'Loses: {loses}'],
                             [f'Draws: {draws}']
                             ], center_size=35))

def on_press(key):
    # print(key)
    pass


def on_release(key):
    global player_position, on_level, do_cycle, Map, steps_from_fight, is_fight, current_enemy, in_shop, levels_from_fight

    # if not is_fight:
    if on_level:
        match key:

            case controls.ext:
                ext()

            case controls.move_u | controls.move_u_alt:  # go up -------------------------------------------
                # ???????? ?????????? ???????????? ?????????? - ?????????????? ???? ?????????????? ??????????
                if player_position[0] == 0:
                    start_array = Map[settings.MAP_SIZE[0] - 1]  # ?????????? ???????? ?????????????????????? ????????????
                    Map = gen.generate_level_3('down', start_array)  # ?????????????? ?????????? ?????????????? ???? ??????????
                    player_position = (settings.MAP_SIZE[0] - 1, player_position[1])  # ???????????? ???????????? ?? ???????????? ??????????????
                    levels_from_fight += 1
                    g.cls()

                # ????????????????????????
                else:
                    if player_position[0] != 0:
                        y = player_position[0] - 1
                        x = player_position[1]

                    try:
                        # ?????????? ???? ????????????????
                        if mtx.flip_mtx(Map)[y][x] == 1:
                            steps_from_fight += 1
                            player_position = (y, x)

                        # ?????????? ?? ??????????????
                        elif mtx.flip_mtx(Map)[y][x] == 4:
                            in_shop = True
                            on_level = False

                    except UnboundLocalError:
                        pass

            case controls.move_l | controls.move_l_alt:  # go left -----------------------------------------
                if player_position[1] == 0:
                    start_array = mtx.get_mtx_column(Map, 0)
                    Map = gen.generate_level_3('right', start_array)
                    player_position = (player_position[0], settings.MAP_SIZE[1] - 1)
                    levels_from_fight += 1
                    g.cls()

                else:
                    if player_position[1] != 0:
                        y = player_position[0]
                        x = player_position[1] - 1

                    try:
                        if mtx.flip_mtx(Map)[y][x] == 1:
                            steps_from_fight += 1
                            player_position = (y, x)

                        # ?????????? ?? ??????????????
                        elif mtx.flip_mtx(Map)[y][x] == 4:
                            in_shop = True
                            on_level = False

                    except UnboundLocalError:
                        pass

            case controls.move_d | controls.move_d_alt:  # go down -----------------------------------------
                y = player_position[0] + 1
                x = player_position[1]

                try:
                    if mtx.flip_mtx(Map)[y][x] == 1:
                        steps_from_fight += 1
                        player_position = (y, x)

                    # ?????????? ?? ??????????????
                    elif mtx.flip_mtx(Map)[y][x] == 4:
                        in_shop = True
                        on_level = False

                except IndexError:
                    pass

            case controls.move_r | controls.move_r_alt:  # go right ----------------------------------------
                if player_position[1] == settings.MAP_SIZE[1] - 1:
                    start_array = mtx.get_mtx_column(Map, settings.MAP_SIZE[1] - 1)
                    Map = gen.generate_level_3('left', start_array)
                    player_position = (player_position[0], 0)
                    levels_from_fight += 1
                    g.cls()

                else:
                    y = player_position[0]
                    x = player_position[1] + 1

                    try:
                        if mtx.flip_mtx(Map)[y][x] == 1:
                            steps_from_fight += 1
                            player_position = (y, x)

                        # ?????????? ?? ??????????????
                        elif mtx.flip_mtx(Map)[y][x] == 4:
                            in_shop = True
                            on_level = False

                    except IndexError:
                        pass

            case Key.shift:
                # on_level = False
                pass

    elif is_player_turn:
        match key:
            case controls.one:
                # print('ONE')
                pass
        pass

    if steps_from_fight > 15 and levels_from_fight > 1:
        if random.random() < .35:
            is_fight = True
            on_level = False

            if victories[1] > 10:  # ???????? ?????????????? ???????????? ?????????????? ????????????, ???? ???????????? ???????? ?????????????? ???? ????????????????
                current_enemy = fight.Enemy((.5, .2, .3))
            else:
                current_enemy = fight.Enemy((.8, .8, 0))  # .8 .2 0

            steps_from_fight = 0
            levels_from_fight = 0


# Intro
# TODO change time in intro to 0.6 and 0.4
import scripts.intro
print(f'\033]2;TDM - Main Menu\007')

draw.pause(0)  # ??????????

g.cls()

listener = Listener(  # ?????????????????? ???????????????????????????? ??????????????
    on_press=on_press,
    on_release=on_release)
listener.start()

# ???????????????? ????????
while do_cycle:
    g.cls()

    try: rows_full = os.get_terminal_size()[1] - 1  # ???????????? ????????????
    except OSError: rows_full = 58


    while on_level:  # ???????? ???? ???????????? ------------------------------------------------------------------------------
        print(f'\033]2;{settings.WINDOW_NAME}\007')  # ???????????? ?????? ????????
        print("\033[F" * rows_full)  # ?????????????????? ?????????? (?????????????? ???????????? ?? ????????????)

        draw.load_main_menu(logo=sprites.MINI_LOGO, slp=0, cls=False)  # ???????????? ????????

        print(draw.render_scene([*draw.convert_codes_map_to_scene(mtx.flip_mtx(Map), player_pos=player_position)],
                                is_map=True))  # ???????????? ??????????????

        draw.print_spaces(1)
        print(draw.center_text(f'Money: {player_money} yen'))  # ????????????
        print(draw.center_text(', '.join(map(lambda x: x().__repr__().strip(), available_troops))))  # ?????????????????? ????????????
        print(draw.center_text(', '.join(map(lambda x: x().__repr__().strip(), passive_spells))))  # ?????????????????? ????????????????

        if player_money < 0:  # ???????? ?????????? ???????? - ????????????????
            on_level = False
            game_over = True

        if victories[2] == 1 and game_win == False:
            on_level = False
            game_win = True

        # print(player_position)
        # mtx.print_mtx(mtx.flip_mtx(Map))

        # key = kb.read_key()

        g.slp(1 / settings.FPS)  # ?????????????????????? ??????

    if in_shop:  # ???????? ?? ???????????????? ---------------------------------------------------------------------------------
        print('\033]2;TDM - In The Shop\007')  # ???????????? ???????????????? ????????

        while in_shop:  # ???????? ????????????????
            g.cls()
            # print("\033[F" * rows_full)

            # ???????????? ???????? ????????????????
            print(sprites.color_str(draw.render_scene([[sprites.SHOP], [''], ['???']]), fg=sprites.table_color))

            # ???????????? ????????, ?????????????? ?????????? ???????????? (???????????? ???????? ?? ???????????? ???????? ?? ???? ???? ???????????? ???????? ?? ????????????)
            product = list(map(lambda x: x(),
                               filter(lambda x: x not in available_troops, fight.cards)))

            product += list(map(lambda x: x(),
                                filter(lambda x: x not in passive_spells, fight.passive_spells)))

            # ?????????????? ???????????? ??????????????
            if len(product) != 0:
                print(draw.render_scene([list(map(lambda x: str(x), product))], center_size=settings.CARD_WIDTH * len(product)))
            else:
                draw.print_spaces(8)

            # ?????????????? ???????????? ??????
            costs = ''
            for i in range(len(product)):
                cst = str(product[i].cost) + ' yen'
                costs += ' ' * ((settings.CARD_WIDTH - len(cst)) // 2 ) + cst + ' ' * (((settings.CARD_WIDTH - len(cst)) // 2 ))

            print(draw.center_text(costs))  # ?????????????? ????????
            draw.print_spaces(1)

            # ?????????????????? ????????
            print(draw.center_text(''.join([' ' * (settings.CARD_WIDTH // 2) + str(i) + ' ' * (settings.CARD_WIDTH // 2 - 1) \
                                            for i in range(1, len(product) + 1)])))
            draw.print_spaces(3)

            print(draw.center_text(f'Money: {player_money} yen'))
            print(draw.center_text(
                ', '.join(map(lambda x: x().__repr__().strip(), available_troops))))  # ?????????????????? ????????????
            print(draw.center_text(
                ', '.join(map(lambda x: x().__repr__().strip(), passive_spells))))  # ?????????????????? ????????????????
            draw.print_spaces(2)
            print(draw.center_text("Enter Card number to buy it or 'exit' to leave"))
            print(draw.center_text("Enter 'stats' to view statistics"))

            while True:
                while msvcrt.kbhit():
                    msvcrt.getwch()

                inp = input()

                if inp.isdigit() and int(inp) - 1 in range(len(product)):
                    id = int(inp) - 1

                    if player_money >= product[id].cost:
                        if type(product[id]).__base__ == fight.Card:
                            available_troops += [type(product[id])]
                        elif type(product[id]).__base__ == fight.PassiveSpell:
                            passive_spells += [type(product[id])]

                        player_money -= product[id].cost
                        break
                    else:
                        print("You haven't enough money")

                elif inp.lower() == 'exit':
                    in_shop = False
                    on_level = True
                    break

                elif inp.lower() == 'stats':
                    g.cls()
                    print_stats()
                    draw.load_main_menu(logo=sprites.PRESS_ANY_BUTTON, cls=0, color='#410000', slp=0.0)
                    draw.pause()
                    break

                else:
                    print('No such number!')

    # ???????? ???????????????? ??????????
    if is_fight:  # -------------------------------------------------------------------------------------------
        Table = fight.empty_table()  # ?????????????? ???????????? ????????
        fight_status = 'going'       # ???????????? ???????????? ?????????? ???? "????????" (?????????? ???????? "????????????????", "????????????", "??????????")
        round_count = 0              # ?????????????? ???????????????????? ?????????????? (?????????? ?????????????????? ?????????? - ?????????? ??????????) ???? ????????????????????????

        player_passive_spells = list(map(lambda x: x(), passive_spells))

        player_energy_boost = 0      # ???????????????????? ?????????????? ????????????
        player_attack_boost = 0      # ???????????????????? ?????????? ???????????? ????????????
        player_health_boost = 0      # ???????????????????? ???????????? ???????????? ????????????

        for spell in player_passive_spells:         # ???????????????????? ?????????????????? ????????????????
            player_energy_boost += spell.energy_boost
            player_attack_boost += spell.attack_boost
            player_health_boost += spell.health_boost

        g.cls()
        print(sprites.color_str(draw.render_scene([[sprites.FIGHT]]), fg='red'))  # ?????????????????? ???????? ??????????

        # ?????????????? ????????
        current_player_weights = []
        for i in range(len(available_troops)):  # ???????????????????? ?????????? ?????? ????????????, ???? ???????????? ?????????????????? ????????
            current_player_weights += [fight.player_weights[available_troops[i]().card_id]]

        # ???????????? ????????
        player_cards = list(map(lambda x: x(), random.choices(available_troops, current_player_weights,
                                                              k=settings.CARDS_ON_HAND)))
        str_player_cards = list(map(lambda x: str(x), player_cards))  # ???????????? ???? ?????????????????? ???????? ???????????? (?????? ????????)

        # ------ ???????????????? ?????? ?????????? ------
        draw.print_spaces(2)
        print(draw.center_text('Your enemy is'))

        print(colored.fg('red'))
        if current_enemy.boss_type == 'common':
            print(draw.center_text('Common Enemy'))
            print(f'\033]2;TDM - Fight (Common Enemy)\007')

        elif current_enemy.boss_type == 'boss':
            print(draw.center_text('Boss'))
            print(f'\033]2;TDM - Fight (Boss)\007')

        else:
            print(draw.center_text('Main Boss'))
            print(f'\033]2;TDM - Fight (Main Boss)\007')
        print(sprites.def_fg)
        # ------ ???????????????? ?????? ?????????? ------

        # ???????? ??????????????????
        draw.print_spaces(2)
        draw.draw_and_wait_for_any_key([["Your hand is"], [str_player_cards], ["Redeal?"]],
                                       [None, settings.CARD_WIDTH * len(player_cards), None], wait=False)
        draw.print_spaces(3)
        print(draw.center_text('Type something and press Enter to Redeal'))
        print(draw.center_text('Or just press Enter to Continue'))

        # ???????? ????????, ???? ???? 10 ??????, ???????? ?????????????? ????????, ???? ??????????????????
        if current_enemy.boss_type == 'boss':
            print(draw.center_text('Print "run" to run (costs 10 yen)'))
        elif current_enemy.boss_type == 'main boss':
            print(draw.center_text('Print "run" to run (free)'))

        while True:
            while msvcrt.kbhit():
                msvcrt.getwch()

            inp = input()

            if inp.lower() == 'run':
                match current_enemy.boss_type:
                    case 'common':
                        print("You can't run away from common enemy")

                    case 'boss':
                        if player_money < 10:
                            print("You haven't 10 yen!")
                            continue

                        player_money -= 10
                        is_fight = False
                        on_level = True
                        break

                    case 'main boss':
                        is_fight = False
                        on_level = True
                        break

            elif len(inp) != 0:
                player_cards = list(map(lambda x: x(), random.choices(available_troops, current_player_weights,
                                                                      k=settings.CARDS_ON_HAND)))
                str_player_cards = list(map(lambda x: str(x), player_cards))
                break
            else:
                break

        del inp

        # Deal Enemy Cards
        match current_enemy.boss_type:
            case 'common':
                enemy_available_troops = available_troops
                current_enemy_weights = []
                for i in range(len(available_troops)):
                    current_enemy_weights += [fight.common_weights[available_troops[i]().card_id]]

            case 'boss':
                current_enemy_weights = fight.boss_weights
                enemy_available_troops = fight.cards
            case 'main boss':
                enemy_available_troops = fight.cards
                current_enemy_weights = fight.main_boss_weights

        enemy_cards = list(map(lambda x: x(), random.choices(enemy_available_troops, current_enemy_weights,
                                                             k=settings.CARDS_ON_HAND)))

        # Choose first player
        dice = list(range(1, 7))
        player_dice = random.choice(dice)
        dice.remove(player_dice)
        enemy_dice = random.choice(dice)

        is_player_turn = True if player_dice > enemy_dice else False

        if is_fight:
            g.cls()
            print(current_enemy_weights)
            print(draw.render_scene([["Enemy"], [sprites.DICES[enemy_dice - 1]],
                                     [sprites.DICES[player_dice - 1]], ["Player"], [""],
                                     ["Press any key to continue..."]]))
            draw.pause()

        del dice, player_dice, enemy_dice

        # Create vars
        player_hp = enemy_hp = settings.START_HP
        player_energy = settings.START_ENERGY + player_energy_boost
        enemy_energy = settings.START_ENERGY
        is_player_done = False
        is_enemy_done = False

        # Main Battle Loop
        while is_fight: # -------------------------------------------------------------------------------------------
            g.cls()
            if not settings.PLAY_WITH_BOT:
                if is_player_turn:
                    print(draw.center_text('??????????????????????????????'))
                    print(draw.center_text("Bottom Player's Turn!"))

                    print(draw.center_text('Press any key to start...'))
                    draw.pause()

                elif not is_player_turn:
                    print(draw.center_text('??????????????????????????????'))
                    print(draw.center_text("Top Player's Turn!"))

                    print(draw.center_text('Press any key to start...'))
                    draw.pause()

            g.cls()
            str_player_cards = list(map(lambda x: str(x), player_cards))
            str_enemy_cards = list(map(lambda x: str(x), enemy_cards))

            # ?????????????????????????? ?????????????????? ??????????????
            for card in Table[1]:
                if type(card).__base__ == fight.Card:
                    card.attack = type(card)().attack + player_attack_boost
                    card.health = type(card)().health + player_health_boost

            # Draw FIGHT logo, print whose turn, print hp's
            fight.print_fight_head()
            draw.print_spaces(0)

            if is_player_done:
                is_player_turn = False
            elif is_enemy_done:
                is_player_turn = True

            print(sprites.color_str(draw.center_text("Your Turn"), fg='green') if is_player_turn else
                  sprites.color_str(draw.center_text("Enemy's Turn"), fg='red'))

            if len(passive_spells) == 0:
                print(draw.center_text("You haven't any Passive Spells"))
            else:
                print(draw.center_text(
                    f'????????????????: {", ".join(map(lambda x: x().__repr__().strip(), passive_spells))}'))  # ?????????????????? ????????????????

            if is_player_done and is_enemy_done:
                print(draw.center_text('All finished'))
            elif is_player_done:
                print(draw.center_text('You finished your moves'))
            elif is_enemy_done:
                print(draw.center_text('Enemy finished moves'))

            print(draw.center_text(f"Your HP: {player_hp}      Enemy's HP: {enemy_hp}"))

            print(draw.center_text(f'Your Energy: {player_energy}       Enemy Energy: {enemy_energy}'))

            # Draw Table, Player Hand and Numbers of Cards
            # Draw enemy hand
            if len(enemy_cards) != 0:
                # ???????? ?????? ?? ?????????? ????????
                if not settings.PLAY_WITH_BOT and not is_player_turn:
                    print(
                        draw.render_scene(scene=[str_enemy_cards], center_size=settings.CARD_WIDTH * len(enemy_cards)))
                else:
                    print(draw.render_scene(scene=[[str(fight.CardBack())] * len(enemy_cards)],
                                            center_size=settings.CARD_WIDTH * len(enemy_cards)))
            else:
                draw.print_spaces(settings.CARD_HEIGHT)

            # Draw Table
            print(draw.render_scene(scene=[[draw.generate_sprite_from_table(table=Table)]],
                                    center_size=settings.CARD_WIDTH * len(Table[0]) + 2))

            # Draw Player Hand
            if len(player_cards) != 0:
                # ???????? ?????? ?? ???????????? ????
                if not settings.PLAY_WITH_BOT and is_player_turn:
                    print(draw.render_scene(scene=[str_player_cards],
                                            center_size=settings.CARD_WIDTH * len(player_cards)))
                # ???????? ?????? ?? ???????????? ???? ????
                elif not settings.PLAY_WITH_BOT and not is_player_turn:
                    print(draw.render_scene(scene=[[str(fight.CardBack())] * len(player_cards)],
                                            center_size=settings.CARD_WIDTH * len(player_cards)))
                # ???????? ???????????? ?? ??????????
                elif settings.PLAY_WITH_BOT:
                    print(draw.render_scene(scene=[str_player_cards],
                                            center_size=settings.CARD_WIDTH * len(player_cards)))
            else:
                draw.print_spaces(settings.CARD_HEIGHT)

            print(draw.center_text(
                ''.join([' ' * (settings.CARD_WIDTH // 2) + str(i) + ' ' * (settings.CARD_WIDTH // 2 - 1) \
                         for i in range(1, len(player_cards) + 1)])))

            # Print Tips
            if fight_status == 'going':
                print('\n', draw.center_text('Enter the number of the card you want to put'))
                print(draw.center_text('Enter "done" to finish your moves'))

            # ?????? ????????????
            if is_player_turn and not is_player_done:
                while True:
                    # ?????????????? ?????????? ?????????? (????????????????)
                    while msvcrt.kbhit():
                        msvcrt.getch()

                    inp = input()  # ?????? ???????????? ????????????

                    # ?????????? ????????????????
                    if inp.lower() == 'done':
                        is_player_done = True
                        is_player_turn = False
                        break

                    # ???????????????? ??????????
                    if inp.isdigit() and int(inp) - 1 in range(len(player_cards)):  # ???????? ???????? ?????????? ?? ?????? ?? ???????????????? ???????????????????? ????????
                        if Table[1].count(0) == 0:  # ???????? ???????? ????????????????, ???? ???????????? ????????????
                            print('Table is full')
                        elif player_cards[int(inp) - 1].energy > player_energy:  # ???????? ???? ?????????????? ??????????????
                            print("You haven't enough energy")
                        else:
                            player_energy -= player_cards[int(inp) - 1].energy  # ???????????????? ??????????????
                            # ?????????????? ???? ???????? ?? ???????????? ???? ????????
                            Table[1][fight.find_free_position(Table[1])] = player_cards.pop(int(inp) - 1)
                            is_player_turn = False
                            break
                    else:
                        print('No such number!')

            # ?????? ??????????
            elif not is_player_turn and not is_enemy_done:
                if settings.PLAY_WITH_BOT:  # ???????? ???????????? ?? ??????????
                    g.slp(settings.BOT_THINKING_TIME)
                    # ?????? ???????????? ??????
                    inp = fight.bot_makes_move(Table, player_hp, enemy_hp, enemy_cards, len(player_cards), enemy_energy)

                    # ?????? ????????????????
                    if inp == 'done':
                        is_enemy_done = True
                        is_player_turn = True
                    # ???????????????? ??????????
                    else:
                        enemy_energy -= enemy_cards[inp].energy
                        Table[0][fight.find_free_position(Table[0])] = enemy_cards.pop(inp)
                        is_player_turn = True
                else:  # ???????? ?????? ??????????
                    while True:
                        # ?????????????? ?????????? ?????????? (????????????????)
                        while msvcrt.kbhit():
                            msvcrt.getch()

                        inp = input()  # ?????? ???????????? ?????????????

                        # ???????? ????????????????
                        if inp.lower() == 'done':
                            is_enemy_done = True
                            is_player_turn = True
                            break

                        # ???????????????? ??????????
                        if inp.isdigit() and int(inp) - 1 in range(len(enemy_cards)):
                            if Table[0].count(0) == 0:
                                print('Table is full')
                            elif enemy_cards[int(inp) - 1].energy > enemy_energy:
                                print("You haven't enough energy")
                            else:
                                enemy_energy -= enemy_cards[int(inp) - 1].energy
                                Table[0][fight.find_free_position(Table[0])] = enemy_cards.pop(int(inp) - 1)
                                is_player_turn = True
                                break
                        else:
                            print('No such number!')

            # ?????? ??????????????????
            elif is_player_done and is_enemy_done:
                # print(fight_status)

                # ?????????????? ?????????? ?????????? ?? ???????????? ????????
                pl_hp = pl_at = en_hp = en_at = 0
                for i in range(len(Table[0])):
                    if Table[0][i] != 0:
                        en_hp += Table[0][i].health
                        en_at += Table[0][i].attack

                    if Table[1][i] != 0:
                        pl_hp += Table[1][i].health
                        pl_at += Table[1][i].attack

                # ?????????????? ?????????? ???? ??????????????
                player_hp -= (en_at - pl_hp) if en_at - pl_hp >= 0 else 0
                enemy_hp -= (pl_at - en_hp) if pl_at - en_hp >= 0 else 0

                # matching winner
                if fight_status != 'going':
                    print(
                        sprites.color_str(draw.center_text('The Fight is over! Press any key to continue...'), 'green'))

                    # clear input buffer
                    while msvcrt.kbhit():
                        msvcrt.getch()
                    g.slp(1)
                    kb.read_key()
                    g.cls()
                    # TODO ???????????????????? ??????????????????????
                    match fight_status:
                        case 'win':
                            print(sprites.color_str(draw.render_scene([[sprites.WIN]]), fg='#af0000'))
                            draw.print_spaces(2)
                            print(draw.center_text('You defeated the'))

                            match current_enemy.boss_type:
                                case 'common':
                                    # 32 average
                                    print(sprites.color_str(draw.center_text("Common Enemy"), "red"))
                                    earn = random.choices([random.randint(20, 40), random.randint(40, 50)], [.7, .1])[0]
                                    victories[0] += 1

                                case 'boss':
                                    # 50 average
                                    print(sprites.color_str(draw.center_text("Boss"), "red"))
                                    earn = random.choices([random.randint(40, 50), random.randint(50, 70)], [.6, .3])[0]
                                    victories[1] += 1

                                case 'main boss':
                                    # 90 average
                                    print(sprites.color_str(draw.center_text("Main Boss"), "red"))
                                    earn = random.randint(60, 120)
                                    victories[2] += 1

                            draw.print_spaces(1)
                            print(draw.center_text('You have earned'))
                            print(sprites.color_str(draw.center_text(str(earn)), 'green'))
                            print(draw.center_text('yen'))
                            collected_money += earn

                        case 'lose':
                            print(sprites.color_str(draw.render_scene([[sprites.LOSE]]), fg='#5f0000'))
                            draw.print_spaces(2)
                            print(draw.center_text('You were defeated by the'))
                            loses += 1

                            match current_enemy.boss_type:
                                case 'common':
                                    # 32 average
                                    print(sprites.color_str(draw.center_text("Common Enemy"), "red"))
                                    earn = - random.choices([random.randint(10, 15), random.randint(15, 25)], [.7, .1])[
                                        0]

                                case 'boss':
                                    # 50 average
                                    print(sprites.color_str(draw.center_text("Boss"), "red"))
                                    earn = - random.choices([random.randint(20, 30), random.randint(30, 40)], [.6, .3])[
                                        0]

                                case 'main boss':
                                    # 90 average
                                    print(sprites.color_str(draw.center_text("Main Boss"), "red"))
                                    earn = - random.randint(50, 100)

                            # ???????? ???? ?????? ???? ?????????? ?????????? ???????????? ?? ???? ?????????????? 4 ??????????
                            if available_troops == list(fight.DEFAULT_TROOPS) and sum(victories) < 4:
                                earn = - random.randint(5, 10)

                            draw.print_spaces(1)
                            print(draw.center_text('You have lost'))
                            print(sprites.color_str(draw.center_text(str(earn)), 'red'))
                            print(draw.center_text('yen'))

                        case 'draw':
                            print(sprites.color_str(draw.render_scene([[sprites.DRAW]]), fg='#870000'))
                            draw.print_spaces(2)
                            print(draw.center_text('Then you quietly dispersed...'))
                            draws += 1

                    draw.print_spaces(1)
                    print(sprites.color_str(draw.center_text('Press any key to continue...'), 'green'))

                    player_money += earn

                    # clear input buffer
                    while msvcrt.kbhit():
                        msvcrt.getch()
                    g.slp(1)
                    kb.read_key()

                    is_fight = False
                    on_level = True

                # ???????? ??????-???? ????????
                if player_hp <= 0 and player_hp == enemy_hp:
                    fight_status = 'draw'
                elif player_hp <= 0 and enemy_hp <= 0:
                    if player_hp < enemy_hp:
                        fight_status = 'lose'
                    elif player_hp > enemy_hp:
                        fight_status = 'win'
                elif player_hp <= 0:
                    fight_status = 'lose'
                elif enemy_hp <= 0:
                    fight_status = 'win'

                if fight_status == 'going':
                    # ?????????????? ???????? ?? ?????????????? ?????? ??????????
                    Table = fight.empty_table()
                    player_cards += list(map(lambda x: x(), random.choices(available_troops, current_player_weights,
                                                                           k=settings.CARDS_TO_DEAL)))

                    enemy_cards += list(map(lambda x: x(), random.choices(available_troops if
                                                                          current_enemy.boss_type == 'common' else
                                                                          fight.cards,
                                                                          current_enemy_weights,
                                                                          k=settings.CARDS_TO_DEAL)))

                    is_enemy_done = is_player_done = False  # Clear done flags
                    player_energy += settings.START_ENERGY + player_energy_boost
                    enemy_energy += settings.START_ENERGY

                    # Loser goes first
                    is_player_turn = True if player_hp <= enemy_hp else False

            g.slp(1 / settings.FPS)

    if game_over:
        g.cls()

        print(sprites.color_str(draw.render_scene([[sprites.GAME_OVER]]), fg='#410000'))
        draw.print_spaces(2)
        print_stats()
        draw.print_spaces(5)
        draw.load_main_menu(logo=sprites.PRESS_ANY_BUTTON, cls=0, color='#410000', slp=0.0)
        draw.pause()

        do_cycle = False

    if game_win:
        g.cls()

        print(sprites.color_str(draw.render_scene([[sprites.GAME_WIN]]), fg='#410000'))
        draw.print_spaces(2)
        print(draw.center_text(''))
        print(draw.render_scene([['You defeated the Main Boss!'],
                                 ['You have reached the main goal of the game'],
                                 ['Now you can continue playing in this world.'],
                                 [''], ['Thanks For Playing!'], ['                                 - Gaudium']
                                 ]))
        draw.print_spaces(2)
        print_stats()
        draw.print_spaces(5)
        print(draw.center_text('You can see your stats at the Shop. Just write "stats" there.'))
        draw.load_main_menu(logo=sprites.PRESS_ANY_BUTTON, cls=0, color='#410000', slp=0.0)
        draw.pause()

        game_win = None
        on_level = True