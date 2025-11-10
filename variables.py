from pygame import*
from math import*
# from Pac_Man_Full_Release_1 import pac_man
init()
FRIGHTENED_DURATION = 20000  # 7 seconds in milliseconds
frightened_timer_start = 0
is_eyes=0
ghost_freeze=False
cheat_level=False
cheat_speed=False
life=3
level=1
pac_update=0
power=0
begin = 0
start=mixer.Sound('assets/pacman_beginning.wav')
death_sound=mixer.Sound('assets/pacman_death.wav')
eat=mixer.Sound('assets/nom_nom.wav')
power_snd=mixer.Sound('assets/power-up.wav')
mixer.Sound.set_volume(eat, 0.1)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
white = (255,255,255)
map2=[
    '--------------------',
    '-   - -       -    -',
    '-  -- - --         -',
    '-   - - -x-  --    -',
    '- --- - -xx-    ----',
    '-       -x-   -    -',
    '---- -  --    - ----',
    'xxx- -        - -xxx',
    '---- - -xeex- - ----',
    '-    - -gggg- -    -',
    '---- - ------ - ----',
    'xxx-  *  p      -xxx',
    '---- - -- --- ------',
    '-          --      -',
    '- --- ---- --- --- -',
    '-                  -',
    '--------------------',
]

game_map=[
    '-----------------------',
    '-#         -         #-',
    '- --- ---- - ---- --- -',
    '- -             - - - -',
    '- - --- ----- --- - - -',
    '-                     -',
    '- -- ---        --- - -',
    '-        -rxxi-       -',
    '- -- --- ------ --- - -',
    '-#         p         #-',
    '- --- ---- - ---- --- -',
    '-   -             -   -',
    '- - - ---   --- - - - -',
    '-#    -     -     -  #-',
    '-----------------------',
]
# Near the top with width, height, etc.
TILE_SIZE = 30
width=690
height=450
score=0
red_ghost=0
pac_man=0
up=['assets/pac man 1-up.png', 'assets/pac man 2-up.png', 'assets/pac man 3.png', 'assets/pac man 2-up.png']
down=['assets/pac man 1-down.png', 'assets/pac man 2-down.png', 'assets/pac man 3.png', 'assets/pac man 2-down.png']
left=['assets/pac man 1-left.png', 'assets/pac man 2-left.png', 'assets/pac man 3.png', 'assets/pac man 2-left.png']
right=['assets/pac man 1.png', 'assets/pac man 2.png', 'assets/pac man 3.png', 'assets/pac man 2.png']
white_ghost=['assets/pac man white1.png', 'assets/pac man white2.png']
red_up=['assets/red up 1.png', 'assets/red up 2.png']
red_down=['assets/red down 1.png', 'assets/red down 2.png']
red_left=['assets/red left 1.png', 'assets/red left 2.png']
red_right=['assets/red right 1.png', 'assets/red right 2.png']
red_still=['assets/red still 1.png', 'assets/red still 2.png']
eyes={'left':'assets/eyes_left.png', 'right':'assets/eyes_right.png', 'up':'assets/eyes_up.png', 'down':'assets/eyes_down.png'}
ghost_ani={'red':{'up':['assets/red up 1.png', 'assets/red up 2.png'],
                'down':['assets/red down 1.png', 'assets/red down 2.png'],
                'left':['assets/red left 1.png', 'assets/red left 2.png'],
                'right':['assets/red right 1.png', 'assets/red right 2.png'],
                'still':['assets/red still 1.png', 'assets/red still 2.png']},
           'pink':{'up':['assets/pink up 1.png', 'assets/pink up 2.png'],
                   'down':['assets/pink down 1.png', 'assets/pink down 2.png'],
                   'left':['assets/pink left 1.png', 'assets/pink left 2.png'],
                   'right':['assets/pink right 1.png', 'assets/pink right 2.png'],
                   'still':['assets/pink still 1.png', 'assets/pink still 2.png']}
}
brick_group = sprite.Group()
dot_group = sprite.Group()
pac_man_group = sprite.Group()
ghost_group = sprite.Group()
red_group = sprite.Group()
pink_group = sprite.Group()
ghosts = sprite.Group()
power_group = sprite.Group()