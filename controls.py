from pynput.keyboard import Key, KeyCode

control_list = {'ext': Key.esc,
                'move_u': Key.up,
                'move_l': Key.left,
                'move_d': Key.down,
                'move_r': Key.right,
                'move_u_alt': KeyCode.from_char('w'),  # W
                'move_l_alt': KeyCode.from_char('a'),  # A
                'move_d_alt': KeyCode.from_char('s'),  # S
                'move_r_alt': KeyCode.from_char('d'),  # D
                }

ext = Key.esc
move_u = Key.up
move_l = Key.left
move_d = Key.down
move_r = Key.right
move_u_alt = KeyCode.from_char('w')  # W
move_l_alt = KeyCode.from_char('a')  # A
move_d_alt = KeyCode.from_char('s')  # S
move_r_alt = KeyCode.from_char('d')  # D
enter = Key.enter
one = KeyCode.from_char('1')