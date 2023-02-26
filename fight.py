import settings, random
import visuals.sprites as sprites
import visuals.draw as draw


class Enemy:

    def __init__(self, chances):
        self.boss_type = random.choices(("common", "boss", "main boss"), weights=chances)[0]


class Card:
    def __init__(self, card_id, cost, energy, attack, health, name2, name1="          ", name3="          ", name0="•"):
        self.card_id = card_id
        self.cost = cost
        self.energy = energy
        self.attack = attack
        self.health = health
        self.name1 = name1
        self.name2 = name2
        self.name3 = name3
        self.name0 = name0

    def __repr__(self):
        return self.name1.strip() + " " + self.name2.strip() + " " + self.name3.strip()

    def __str__(self):
        return sprites.card_template.format(self.attack, self.health, self.name1, self.name2, self.name3,
                                            self.name0, self.energy)


class PassiveSpell(Card):
    def __init__(self, card_id, cost, energy, attack, health, name2, attack_boost, health_boost, energy_boost,
                 name1="          ", name3="          ", name0="•"):
        super().__init__(card_id, cost, energy, attack, health, name2, name1, name3, name0)

        self.attack_boost = attack_boost
        self.health_boost = health_boost
        self.energy_boost = energy_boost

    def __str__(self):
        up_width = 10
        down_width = 10

        up_width -= (len(self.attack) + len(self.health))
        down_width -= (len(self.energy) + len(self.name0))

        header = str(self.attack) + ' ' * up_width + str(self.health)

        if down_width % 2 == 0:
            footer = str(self.name0) + '﹏' * (down_width // 2) + str(self.energy)
        else:
            footer = str(self.name0) + '﹏' * ((down_width-1) // 2) + '_' + str(self.energy)

        return sprites.spell_template.format(header, self.name1, self.name2, self.name3, footer)

class Spearman(Card):
    def __init__(self):
        super().__init__(card_id=0, cost=5, energy=1, attack=1, health=2, name2=" копейщик ")


class Archer(Card):
    def __init__(self):
        super().__init__(card_id=1, cost=20, energy=1, attack=2, health=1, name2="  лучник  ")


class Samurai(Card):
    def __init__(self):
        super().__init__(card_id=2, cost=40, energy=3, attack=2, health=3, name2=" самурай  ")


class Rider(Card):
    def __init__(self):
        super().__init__(card_id=3, cost=60, energy=4, attack=3, health=4,
                         name1=" самурай  ", name2="    на    ", name3="   коне   ")


class Shield(Card):
    def __init__(self):
        super().__init__(card_id=4, cost=25, energy=2, attack=0, health=3, name2=" щитоносец")


class Catapult(Card):
    def __init__(self):
        super().__init__(card_id=5, cost=35, energy=3, attack=4, health=0, name2="катапульта")


# TODO новые карты кирилла


# ------------------------


class CardBack(Card):
    def __init__(self):
        super().__init__(card_id=-1, cost=0, energy="•", attack="•", health="•", name0="•", name2="  ~TDM~   ")


# ------------------------


class BattleCry(PassiveSpell):  # +1 атаки всем картам
    def __init__(self):
        super().__init__(card_id=-2, cost=50, energy="•", attack="+1", health="•", name0="•",
                         name1="  Боевой  ", name2="   Клич   ", attack_boost=1, health_boost=0, energy_boost=0)


class AncientCharms(PassiveSpell):  # +2 маны каждый раунд
    def __init__(self):
        super().__init__(card_id=-3, cost=50, energy="+2", attack="•", health="•", name0="•",
                         name1=" Древние  ", name2="   Чары   ", attack_boost=0, health_boost=0, energy_boost=2)


cards = (Spearman, Archer, Samurai, Rider, Shield, Catapult)
passive_spells = (BattleCry, AncientCharms)
# cards_to_buy = (Spearman, Archer, Samurai, Rider, BattleCry, AncientCharms)
DEFAULT_TROOPS = (Spearman, Archer)             # Войска, доступные с начала игры
player_weights = (.35, .3, .2, .15, .20, .35)
common_weights = (.4, .3, .2, .1, .25, .2)
boss_weights = (.3, .3, .2, .2, .2, .35)
main_boss_weights = (.25, .25, .3, .2, .15, .25)


def empty_table():
    return [0 for o in range(settings.CARDS_ON_TABLE)], [0 for o in range(settings.CARDS_ON_TABLE)], [0], [0]


def start_fight():
    player_cards = list(map(lambda x: x(), random.choices(cards, player_weights, k=settings.CARDS_ON_HAND)))
    str_player_cards = list(map(lambda x: str(x), player_cards))

    draw.draw_and_wait_for_any_key([["Your hand is"], [str_player_cards], ["Redeal?"]], [None, 12 * len(player_cards), None])
    
    pass


def print_fight_head():
    print(sprites.color_str(draw.render_scene([[sprites.FIGHT]], is_map=False), fg='red'))


def find_free_position(lst):
    if lst.count(0) == 0:
        return None

    center = len(lst) // 2
    if lst[center] == 0:
        return center

    if len(lst) % 2 == 1:
        for i in range(1, center + 1):
            if lst[center - i] == 0:
                return center - i
            elif lst[center + i] == 0:
                return center + i

    else:
        for i in range(1, center + 1):
            if lst[center - i] == 0:
                return center - i
            elif lst[center + i] == 0:
                return center + i


def bot_makes_move(table, player_hp, enemy_hp, enemy_hand, number_of_pl_cards, enemy_energy):
    # returns "done" or num of card to play
    # TODO придумать алгоритм для бота

    ats = [crd.attack for crd in enemy_hand]
    hps = [crd.health for crd in enemy_hand]
    enrgs = [crd.energy for crd in enemy_hand]

    if len(enemy_hand) == 0 or enemy_energy < min(enrgs) or find_free_position(table[0]) is None:
        return 'done'

    pl_hp = pl_at = en_hp = en_at = 0
    for i in range(len(table[0])):
        if table[0][i] != 0:
            en_hp += table[0][i].health
            en_at += table[0][i].attack

        if table[1][i] != 0:
            pl_hp += table[1][i].health
            pl_at += table[1][i].attack

    if table[0].count(0) == settings.CARDS_ON_TABLE and table[1].count(0) == settings.CARDS_ON_TABLE:
        return enemy_hand.index(list(filter(lambda x: x.attack == min(ats), enemy_hand))[0])

    if random.random() < 0.2:
        return 'done'

    return enemy_hand.index(random.choice(list(filter(lambda x: x.energy <= enemy_energy, enemy_hand))))


if __name__ == "__main__":
    print(draw.render_scene([[str(cards[0]())] * 9], is_map=False, center_size=9*12))

    # print(draw.render_scene([str_player_cards], is_map=False,
    #                         center_size=12*len(player_cards)))
    # print(str(player_cards[0]()).split('\n'))
    # print(draw.convert_codes_map_to_scene(gp.generate_level_3()))
