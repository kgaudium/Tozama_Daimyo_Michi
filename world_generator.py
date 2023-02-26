import random, math
import libs.matrix as mtx
import libs.vector as vec
import settings


def generate_level(height, width, prev_roads=None, side='bottom'):
    # sprite codes are in sprites.py
    grass_symbol = 0
    road = 1
    building_symbol = 4

    Map = mtx.zeros((height, width))

    Map[0][int(width / 2)] = road
    # mtx.print_mtx(Map)

    # 1 Центральная дорога

    for i in range(1, len(Map)):
        Map[i][int(width / 2)] = road
        if random.random() < 0.4:
            break

    # print('#1')
    # mtx.print_mtx(Map)

    # 2 Ветвление

    for i in range(1, len(Map) - 1):
        # Один проход по левую сторону от центра, второй по правую
        for j in range(int(width / 2), width):
            if Map[i - 1][j] != road and Map[i][j - 1] == road and random.random() < 0.8:
                Map[i][j] = road

        for j in range(int(width / 2), -1, -1):
            if Map[i - 1][j] != road and Map[i][j + 1] == road and random.random() < 0.8:
                Map[i][j] = road

    # print('#2')
    # mtx.print_mtx(Map)

    # 3 Проверка на возможность выхода

    count = 0
    for i in range(1, height - 1):
        if Map[i][0] == road:
            count += 1
            break
        elif Map[i][width - 1] == road:
            count += 1
            break

    if Map[height - 1][int(width / 2)] != road and count == 0:
        for i in range(height):
            Map[i][int(width / 2)] = road

    # print('#3')
    # mtx.print_mtx(Map)

    # 4 Добавление зданий
    br = True
    for i in range(height):
        for j in range(width):
            neighbors = []
            for k in range(4):
                try:
                    neighbors += [Map[i + int(math.sin(k * math.pi / 2))][j + int(math.cos(k * math.pi / 2))]]
                except Exception as e:
                    neighbors += [grass_symbol]

            if neighbors.count(1) > 2 and random.random() > 0.2 and Map[i][j] == 0:
                Map[i][j] = building_symbol
                br = False

            if br == 0:
                break

        if br == 0:
            break
            # print(i, j, neighbors)

    # mtx.print_mtx(Map)
    return Map


def add_buildings(Map):
    grass_symbol = 0
    road = 1
    building_symbol = 4

    br = True
    for i in range(len(Map)):
        for j in range(len(Map[i])):
            neighbors = []
            for k in range(4):
                try:
                    neighbors += [Map[i + int(math.sin(k * math.pi / 2))][j + int(math.cos(k * math.pi / 2))]]
                except Exception as e:
                    neighbors += [grass_symbol]

            if neighbors.count(1) > 2 and random.random() > 0.2 and Map[i][j] == 0:
                Map[i][j] = building_symbol
                br = False

            if br == 0:
                break

        if br == 0:
            break
            # print(i, j, neighbors)

    return Map


def generate_level_2(start_side='down', start_array=None, ):
    if not start_array:
        start_array = [0] * settings.MAP_SIZE[1]
        start_array[int(settings.MAP_SIZE[1] / 2)] = 1

    Map = mtx.zeros(settings.MAP_SIZE)
    map_size_0 = settings.MAP_SIZE[0]
    map_size_1 = settings.MAP_SIZE[1]
    # map_size_1_minus_1 = map_size_1 - 1

    # --- 1 ---

    match start_side:
        case 'down':
            Map[0] = start_array

        case 'left':
            Map = mtx.set_column_to_mtx(Map, 0, start_array)
            pass

        case 'right':
            Map = mtx.set_column_to_mtx(Map, map_size_1 - 1, start_array)
            pass

    # --- 2 ---

    last_move = 3  # против часовой стрелки начиная с 0 - право (1 - вверх и т.д.)

    def Bot(pos, allowed_ways):  # (2,4), ((1,0), (0,1), (-1,0)) - пример
        # global map_size_1_minus_1, map_size_1
        # map_size_1 = settings.MAP_SIZE[1]
        map_size_1_minus_1 = settings.MAP_SIZE[1] - 1
        generating = True

        def paint_cell(coord, color=1):
            Map[coord[0]][coord[1]] = color

        # def make_step(way):
        #     # global pos
        #     paint_cell(pos)
        #     pos = vec.summ(pos, way)

        while generating:
            match pos:

                # --- Если в самом начале, то делает шаг вперёд, чтобы не топтаться у стенки

                case (0, _) if start_side == 'down':
                    paint_cell(pos)
                    pos = vec.summ(pos, (1, 0))

                case (_, 0) if start_side == 'left':
                    paint_cell(pos)
                    pos = vec.summ(pos, (0, 1))

                case (_, 6) if start_side == 'right':
                    paint_cell(pos)
                    pos = vec.summ(pos, (0, -1))

                # --- Если упёрся в стену, то вырубает, чтобы не было полосы у стены

                case (0, _) if start_side != 'down':
                    paint_cell(pos)
                    break

                case (_, 0) if start_side != 'left':
                    paint_cell(pos)
                    break

                case (_, 6) if start_side != 'right':
                    paint_cell(pos)
                    break

                # ---

            # --- Выбирает куда и в каком количестве идти

            way = random.sample(allowed_ways, random.choices(population=[1, 2, 3], weights=[.7, .2, .1], k=1)[0])

            # --- Делает шаг
            paint_cell(pos)

            if Map[vec.summ(pos, way[0])[0]][vec.summ(pos, way[0])[1]] != 0:
                continue

            pos = vec.summ(pos, way[0])

            # --- Если нужно, создаёт других ботов

            if len(way) > 1:
                for i in range(1, len(way)):
                    Bot(vec.summ(pos, way[i]), allowed_ways)

        pass

    for i in range(len(start_array)):
        if start_array[i] == 1:
            match start_side:
                case 'down':
                    Bot((0, i), ((1, 0), (0, 1), (0, -1)))  # вверх, вправо, влево

                case 'left':
                    Bot((i, 0), ((1, 0), (0, 1)))

                case 'right':
                    Bot((i, 0), ((1, 0), (0, -1)))

    # для всех единичек в старт_аррау запустить бота
    # если с краю на разрешённых направлениях, то конец
    # если с краю на запрещённых направлениях, то выйти из края

    return Map


def generate_level_3(start_side='down', start_array=None, need_buildings=True):
    if not start_array:
        start_array = [0] * settings.MAP_SIZE[1]
        start_array[int(settings.MAP_SIZE[1] / 2)] = 1

    Map = mtx.zeros(settings.MAP_SIZE)

    # --- 1 ---

    match start_side:
        case 'down':
            Map[0] = start_array

        case 'left':
            Map = mtx.set_column_to_mtx(Map, 0, start_array)

        case 'right':
            Map = mtx.set_column_to_mtx(Map, settings.MAP_SIZE[1] - 1, start_array)
            pass

    # --- 2 ---

    def Bot(pos, side):  # ЗДЕСЬ ПРАВИЛА (стр 242 и пр.) РАБОТАЮТ ТОЛЬКО ДЛЯ РЕЖИМА DOWN

        match side:
            case 'down':
                Map[pos[0]][pos[1]] = 1
                allowed_ways = ((1, 0), (0, 1), (0, -1))
                def_pos = pos
                way_count = random.choices(population=[1, 2, 3], weights=[.6, .3, .05], k=1)[0]
                ways = random.sample(allowed_ways, way_count)

                for i in range(way_count):
                    pos = vec.summ(pos, ways[i])
                    Map[pos[0]][pos[1]] = 1
                    last_way = ways[i]
                    if last_way == (1, 0):
                        up_counter = 2
                    else:
                        up_counter = 0

                    generating = True
                    while generating:

                        allows = list(allowed_ways)
                        if last_way == (0, 1):
                            allows.remove((0, -1))
                        elif last_way == (0, -1):
                            allows.remove((0, 1))

                        if last_way == (1, 0) and up_counter < 2:
                            last_way = (1, 0)
                            up_counter += 1
                        else:
                            last_way = random.choice(allows)
                            if last_way == (1, 0):
                                up_counter += 1
                            else:
                                up_counter = 0

                        # if (pos[1] == 0 and last_way == (0, -1)) or \
                        #         (pos[1] == settings.MAP_SIZE[1] - 1 and last_way == (0, 1)):
                        #     continue

                        try:
                            if Map[vec.summ(pos, last_way)[0]][vec.summ(pos, last_way)[1]] != 0:
                                break

                            if pos[1] == 0 and last_way == (0, -1):
                                continue

                            pos = vec.summ(pos, last_way)

                        except IndexError:
                            break

                        if pos[0] == settings.MAP_SIZE[0] - 1 or pos[1] == 0 or pos[1] == settings.MAP_SIZE[1] - 1:
                            # print(pos, settings.MAP_SIZE)
                            generating = False

                        Map[pos[0]][pos[1]] = 1

                        pass

                    pos = def_pos

            case 'left':
                Map[pos[0]][pos[1]] = 1
                allowed_ways = ((1, 0), (0, 1), (-1, 0))
                def_pos = pos
                way_count = random.choices(population=[1, 2, 3], weights=[.6, .3, .05], k=1)[0]
                ways = random.sample(allowed_ways, way_count)

                for i in range(way_count):
                    if pos[0] == 0 and ways[i] == (1, 0):
                        ways[i] = random.choice(((0, 1), (-1, 0)))

                    pos = vec.summ(pos, ways[i])
                    Map[pos[0]][pos[1]] = 1
                    last_way = ways[i]
                    if last_way == (0, 1):
                        up_counter = 2
                    else:
                        up_counter = 0

                    generating = True
                    while generating:

                        allows = list(allowed_ways)
                        if last_way == (1, 0):
                            allows.remove((-1, 0))
                        elif last_way == (-1, 0):
                            allows.remove((1, 0))

                        if last_way == (0, 1) and up_counter < 2:
                            last_way = (0, 1)
                            up_counter += 1
                        else:
                            last_way = random.choice(allows)
                            if last_way == (0, 1):
                                up_counter += 1
                            else:
                                up_counter = 0

                        try:
                            if Map[vec.summ(pos, last_way)[0]][vec.summ(pos, last_way)[1]] != 0:
                                break

                            if pos[0] == 1 and last_way == (-1, 0):
                                continue

                            pos = vec.summ(pos, last_way)

                        except IndexError:
                            break

                        if pos[0] == settings.MAP_SIZE[0] - 1 or pos[1] == 0 or pos[1] == settings.MAP_SIZE[1] - 1:
                            # print(pos, settings.MAP_SIZE)
                            generating = False

                        Map[pos[0]][pos[1]] = 1

                        pass

                    pos = def_pos

            case 'right':
                Map[pos[0]][pos[1]] = 1
                allowed_ways = ((1, 0), (0, -1), (-1, 0))
                def_pos = pos
                way_count = random.choices(population=[1, 2, 3], weights=[.6, .3, .05], k=1)[0]
                ways = random.sample(allowed_ways, way_count)

                for i in range(way_count):
                    if pos[0] == 0 and ways[i] == (1, 0):
                        ways[i] = random.choice(((0, 1), (-1, 0)))

                    pos = vec.summ(pos, ways[i])
                    Map[pos[0]][pos[1]] = 1
                    last_way = ways[i]
                    if last_way == (0, 1):
                        up_counter = 2
                    else:
                        up_counter = 0

                    generating = True
                    while generating:

                        allows = list(allowed_ways)
                        if last_way == (1, 0):
                            allows.remove((-1, 0))
                        elif last_way == (-1, 0):
                            allows.remove((1, 0))

                        if last_way == (0, 1) and up_counter < 2:
                            last_way = (0, 1)
                            up_counter += 1
                        else:
                            last_way = random.choice(allows)
                            if last_way == (0, 1):
                                up_counter += 1
                            else:
                                up_counter = 0

                        try:
                            if Map[vec.summ(pos, last_way)[0]][vec.summ(pos, last_way)[1]] != 0:
                                break

                            if pos[0] == 1 and last_way == (-1, 0):
                                continue

                            pos = vec.summ(pos, last_way)

                        except IndexError:
                            break

                        if pos[0] == settings.MAP_SIZE[0] - 1 or pos[1] == 0 or pos[1] == settings.MAP_SIZE[1] - 1:
                            # print(pos, settings.MAP_SIZE)
                            generating = False

                        Map[pos[0]][pos[1]] = 1

                        pass

                    pos = def_pos

    for i in range(len(start_array)):
        if start_array[i] == 1:
            match start_side:
                case 'down':
                    Bot((1, i), start_side)

                case 'left':
                    Bot((i, 1), start_side)

                case 'right':
                    Bot((i, settings.MAP_SIZE[1] - 2), start_side)

    return add_buildings(Map) if need_buildings else Map


if __name__ == '__main__':
    mtx.print_mtx(mtx.flip_mtx(generate_level_3('right', [0, 0, 0, 1, 0])))
