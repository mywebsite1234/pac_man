from pygame import*
from random import*
from math import*
from ghosts_exept_red import*
import variables
def text(message,x,y,font_color,font_size, font_type='font.otf'):
        font_type=font.Font(font_type,font_size)
        text=font_type.render(message,True,font_color)
        window.blit (text, (x,y))

init()

        
        # if self.index < 1 or self.index > 3:
        #     self.index=-self.index
                        







    
draw_map(True)
size_window = (variables.width, variables.height)
window = display.set_mode(size_window)
display.set_caption('Pac Man')
run=True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key==K_s:
                print(score)
            if e.key==K_l:
                variables.life+=1
            if e.key==K_c:
                variables.cheat_level=True
            if e.key==K_LSHIFT:
                variables.cheat_speed=True
            if e.key==K_LCTRL:
                variables.ghost_freeze=True
            if e.key==K_LALT:
                variables.power = 1
                variables.frightened_timer_start = time.get_ticks()
        if e.type == KEYUP:
            if e.key==K_LSHIFT:
                variables.cheat_speed=False
            if e.key==K_LCTRL:
                variables.ghost_freeze=False


    
    

        
        
        

#   update
    if variables.begin == 1:
        # pac_man_group.update()
        variables.dot_group.update()
        variables.ghost_group.update()
        variables.red_group.update()
        variables.pink_group.update()
        variables.power_group.update()
    if variables.begin == 1 or variables.pac_update == 1:
        variables.pac_man_group.update()
#   time thing
    if variables.power == 1:
        current_time = time.get_ticks()
        if current_time - variables.frightened_timer_start > variables.FRIGHTENED_DURATION:
            # variables.power = 0  # Time's up! End frightened mode.
            # print('test')
            turn_back_red()

#   draw
    window.fill(variables.black)
    # print(variables.power)
    variables.brick_group.draw(window)
    variables.dot_group.draw(window)
    variables.pac_man_group.draw(window)
    variables.ghost_group.draw(window)
    variables.red_group.draw(window)
    variables.pink_group.draw(window)
    variables.power_group.draw(window)
#   text
    text(f'lives left:{variables.life}', 0, 0, 'white', 30)
    text(f'level:{variables.level}', 250, 0, 'white', 30)

    if variables.begin == 0:
        text(f'lives left:{variables.life}', 0, 0, 'white', 30)
        text(f'level:{variables.level}', 250, 0, 'white', 30)
        mixer.Sound.play(variables.start)
        text('Ready?', variables.width//2-70, variables.height//2-60, 'red', 50)
        display.update()
        time.delay(2000)
        window.fill(variables.black)
        variables.brick_group.draw(window)
        variables.dot_group.draw(window)
        variables.pac_man_group.draw(window)
        variables.ghost_group.draw(window)
        variables.red_group.draw(window)
        variables.pink_group.draw(window)
        variables.power_group.draw(window)
        text('Go!', variables.width//2-20, variables.height//2-60, 'green', 50)
        text(f'lives left:{variables.life}', 0, 0, 'white', 30)
        text(f'level:{variables.level}', 250, 0, 'white', 30)
        display.update()
        time.delay(2000)
        variables.begin=1
    elif variables.begin == -3:
        # mixer.Sound.play(start)
        # text('Ready?', width//2-90, height//2-20, 'red', 50)
        display.update()
        # time.delay(2000)
        window.fill(variables.black)
        variables.brick_group.draw(window)
        variables.dot_group.draw(window)
        variables.pac_man_group.draw(window)
        variables.ghost_group.draw(window)
        variables.red_group.draw(window)
        variables.pink_group.draw(window)
        variables.power_group.draw(window)
        text('Go!', variables.width//2-40, variables.height//2-50, 'green', 50)
        display.update()
        time.delay(1000)
        variables.begin=1
    
    display.update()
    time.delay(50)
    

quit()