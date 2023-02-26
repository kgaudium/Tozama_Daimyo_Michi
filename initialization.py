import os, colored

print(colored.fg('white')+colored.bg('black'))
is_cmd = True

try:
    os.get_terminal_size()
except:
    is_cmd = False

# TODO TUTORIAL