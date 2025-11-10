from pygame import*
import variables
from random import*
from math import*
# from Pac_Man_Full_Release_1 import pink_target




init()
def draw_map(do_dots):
    global pac_man, red_ghost, pink_ghost
    size=30
    x=0
    y=0
    for ro in variables.game_map:
        for s in ro:
            if s == '-':
                brick = Brick(x,y)
                variables.brick_group.add(brick)
            if do_dots == True:
                if s == ' ':
                    dot = Dot(x+12,y+12)
                    variables.dot_group.add(dot)
                if s == '#':
                    power_dot = Power_Dot(x+10, y+10)
                    variables.power_group.add(power_dot)
            if s == 'p':
                pac_man = Pac_Man(x+1,y+1)
                variables.pac_man_group.add(pac_man)
            if s == 'g':
                ghost = Ghost(x+1,y+1)
                variables.ghost_group.add(ghost)
                variables.ghosts.add(ghost)
            if s == 'r':
                red_ghost = Red_Ghost(x, y)
                variables.red_group.add(red_ghost)
                variables.ghosts.add(red_ghost)
            if s == 'i':
                pink_ghost = Pink_Ghost(x, y)
                variables.pink_group.add(pink_ghost)
                variables.ghosts.add(pink_ghost)
            x+=size
        x=0
        y+=size
def clear_groups():
    variables.brick_group.empty()
    # dot_group.empty()
    variables.ghosts.empty()
    variables.ghost_group.empty()
    variables.red_group.empty()
    variables.pac_man_group.empty()
    variables.pink_group.empty()
    # variables.power_group.empty()
def check_ghost_power(ghost):
    var = 0
    if ghost == 'red':
        if red_ghost.power == 1: var = 1
    elif ghost == 'pink':
        if pink_ghost.power == 1: var = 1
    return var


def update_power():
    red_ghost.update_power()
    pink_ghost.update_power()
def turn_back_red():
    red_ghost.turn_back()
    pink_ghost.turn_back()
def pink_target():
    target_x=0
    target_y=0
    if pac_man.direction == 'up':
        target_y=pac_man.rect.centery-3
    if pac_man.direction == 'down':
        target_y=pac_man.rect.centery+3
    if pac_man.direction == 'right':
        target_x=pac_man.rect.centerx+3
    if pac_man.direction == 'left':
        target_x=pac_man.rect.centerx-3
    return (target_x // variables.TILE_SIZE, target_y // variables.TILE_SIZE)
def pink_scared():
    pass
    # implement scared logic here

def get_distance(pos1, pos2):
    """Calculates the Euclidean distance between two (x, y) tuples."""
    return sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)
class  Pink_Ghost (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load(variables.ghost_ani['pink']['still'][0])
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        self.is_eyes = 0
        # New attributes for pathfinding
        self.direction = 'up' # Start by moving left out of the ghost house
        self.speed = 5 # Use a speed that is a divisor of TILE_SIZE for smooth movement
        self.target_tile = (0, 0)
        self.last_direction = ''
        self.power = 0
        # Animation attributes
        self.index = 1
        self.normal_speed = 5 # Slower, more authentic speed
        self.cheat_speed = 0

    def update(self):
        # Handle ghost freeze cheat
        if variables.ghost_freeze:
            self.speed = self.cheat_speed
        else:
            self.speed = self.normal_speed

        if sprite.spritecollide(self, variables.pac_man_group, False) and self.power == 1:
            self.turn_into_eyes()
        
        if (((self.rect.x//variables.TILE_SIZE) == 10 and (self.rect.y//variables.TILE_SIZE) == 7) or ((self.rect.x//variables.TILE_SIZE) == 11 and (self.rect.y//variables.TILE_SIZE) == 7) or ((self.rect.x//variables.TILE_SIZE) == 12 and (self.rect.y//variables.TILE_SIZE) == 7) or ((self.rect.x//variables.TILE_SIZE) == 13 and (self.rect.y//variables.TILE_SIZE) == 7)) and self.is_eyes == 1:
            self.turn_back()

        

        # Only make a decision when the ghost is aligned with the grid
        if self.rect.x % variables.TILE_SIZE == 0 and self.rect.y % variables.TILE_SIZE == 0:
            self.make_pathfinding_decision()

        # Update image based on direction
        if self.direction in variables.ghost_ani['pink']:
            if self.power == 0:
                self.image = image.load(variables.ghost_ani['pink'][self.direction][int(self.index)%2])
            elif self.is_eyes == 1:
                self.image = image.load(variables.eyes[self.direction])
            else:
                self.image = image.load(variables.white_ghost[int(self.index)%2])
        self.index += 0.2

        # Move the ghost based on its current direction
        if self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed

        # Wall collision detection to prevent going through walls
        bricks = sprite.spritecollide(self, variables.brick_group, False)
        if bricks:
            for w in bricks:
                if self.direction == 'right':
                    self.rect.right = w.rect.left
                elif self.direction == 'left':
                    self.rect.left = w.rect.right
                elif self.direction == 'up':
                    self.rect.top = w.rect.bottom
                elif self.direction == 'down':
                    self.rect.bottom = w.rect.top
            
            # Align to grid to ensure we can make pathfinding decisions
            self.rect.x = (self.rect.x // variables.TILE_SIZE) * variables.TILE_SIZE
            self.rect.y = (self.rect.y // variables.TILE_SIZE) * variables.TILE_SIZE
            
            # Immediately recalculate direction since we hit a wall
            self.make_pathfinding_decision()

    def update_power(self):
        if variables.power == 1: self.power = 1
        if variables.power == 0: self.power = 0
    def get_tile_coords(self):
        """Returns the ghost's current tile coordinates (col, row)."""
        return (self.rect.centerx // variables.TILE_SIZE, self.rect.centery // variables.TILE_SIZE)

    def make_pathfinding_decision(self):

        if self.power == 1 and self.is_eyes == 0:
            # Frightened Mode: Pick a random, valid tile as the target
            while True:
                rand_col = randint(0, len(variables.game_map[0]) - 1)
                rand_row = randint(0, len(variables.game_map) - 1)
                # Make sure the random tile is not a wall
                if variables.game_map[rand_row][rand_col] != '-':
                    self.target_tile = (rand_col, rand_row)
                    break # Exit the loop once a valid tile is found

        # 1. Set the target tile to Pac-Man's current tile
        else:
            if self.is_eyes == 0:
                self.target_tile = pink_target()
            elif self.is_eyes == 1:
                self.target_tile = (11, 7)

        # 2. Get possible directions
        possible_directions = self.get_possible_directions()

        # 3. Find the best direction
        best_direction = ''
        min_distance = float('inf')

        for direction in possible_directions:
            # Get the tile that this direction would lead to
            next_tile = self.get_next_tile(direction)
            
            # Calculate distance from that future tile to the target
            distance = get_distance(next_tile, self.target_tile)

            # If this path is shorter, it's our new best choice
            if distance < min_distance:
                min_distance = distance
                best_direction = direction
        
        # 4. Commit to the best direction
        if best_direction:
            self.last_direction = self.direction
            self.direction = best_direction

    def get_possible_directions(self):
        """Checks surroundings for valid paths, excluding walls and reversing."""
        current_tile_col, current_tile_row = self.get_tile_coords()
        directions = []

        # Get map dimensions for bounds checking
        map_height = len(variables.game_map)
        map_width = len(variables.game_map[0])

        # Define opposites to prevent reversing
        opposites = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}

        # Check UP (with bounds check)
        if current_tile_row > 0 and \
           variables.game_map[current_tile_row - 1][current_tile_col] != '-' and \
           self.direction != 'down':
            directions.append('up')
        # Check DOWN (with bounds check)
        if current_tile_row < map_height - 1 and \
           variables.game_map[current_tile_row + 1][current_tile_col] != '-' and \
           self.direction != 'up':
            directions.append('down')
        # Check LEFT (with bounds check)
        if current_tile_col > 0 and \
           variables.game_map[current_tile_row][current_tile_col - 1] != '-' and \
           self.direction != 'right':
            directions.append('left')
        # Check RIGHT (with bounds check)
        if current_tile_col < map_width - 1 and \
           variables.game_map[current_tile_row][current_tile_col + 1] != '-' and \
           self.direction != 'left':
            directions.append('right')
        
        # This handles dead ends where the only option is to reverse
        if not directions and opposites.get(self.direction):
            return [opposites[self.direction]]

        return directions

    def get_next_tile(self, direction):
        """Gets the coordinates of the tile in a given direction."""
        col, row = self.get_tile_coords()
        if direction == 'up':
            return (col, row - 1)
        if direction == 'down':
            return (col, row + 1)
        if direction == 'left':
            return (col - 1, row)
        if direction == 'right':
            return (col + 1, row)
        return (col, row)

    def turn_into_eyes(self):
        self.is_eyes = 1
        self.speed = 10
        self.normal_speed = 10
        # If already grid-aligned, immediately recalculate path to ghost house
        if self.rect.x % variables.TILE_SIZE == 0 and self.rect.y % variables.TILE_SIZE == 0:
            self.make_pathfinding_decision()

    def turn_back(self):
        self.power = 0
        self.speed = 5
        self.normal_speed = 5
        self.is_eyes = 0

class  Brick (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/pac man brick.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]



class  Dot (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/dot.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
    def update(self):
        global score, run, begin, life, level, cheat_level
        if sprite.spritecollide(self, variables.pac_man_group, False):
            self.kill()
            mixer.Sound.play(variables.eat)
            # print(eat)
            variables.score+=1
        if len(variables.dot_group) == 0 or variables.cheat_level == True:
            clear_groups()
            draw_map(True)
            variables.life=3
            variables.level+=1
            variables.cheat_level=False
            variables.begin=0
            # print(variables.begin)

class  Power_Dot (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/power_dot.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
    def update(self):
        global score, run, begin, life, level, cheat_level
        if sprite.spritecollide(self, variables.pac_man_group, False):
            self.kill()
            mixer.Sound.play(variables.power_snd)
            variables.power=1
            update_power()
            variables.frightened_timer_start = time.get_ticks() 
        
class  Red_Ghost (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load(variables.ghost_ani['red']['still'][0])
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        self.is_eyes = 0
        # New attributes for pathfinding
        self.direction = 'up' # Start by moving left out of the ghost house
        self.speed = 5 # Use a speed that is a divisor of TILE_SIZE for smooth movement
        self.target_tile = (0, 0)
        self.last_direction = ''
        self.power = 0
        # Animation attributes
        self.index = 1
        self.normal_speed = 5 # Slower, more authentic speed
        self.cheat_speed = 0

    def update(self):
        # Handle ghost freeze cheat
        keys= key.get_pressed()
        if variables.ghost_freeze:
            self.speed = self.cheat_speed
        else:
            self.speed = self.normal_speed

        

        if keys[K_p]:
            print(pac_man.rect.centerx // variables.TILE_SIZE, pac_man.rect.centery // variables.TILE_SIZE)

        if sprite.spritecollide(self, variables.pac_man_group, False) and self.power == 1:
            self.turn_into_eyes()
        
        if (((self.rect.x//variables.TILE_SIZE) == 10 and (self.rect.y//variables.TILE_SIZE) == 7) or ((self.rect.x//variables.TILE_SIZE) == 11 and (self.rect.y//variables.TILE_SIZE) == 7) or ((self.rect.x//variables.TILE_SIZE) == 12 and (self.rect.y//variables.TILE_SIZE) == 7) or ((self.rect.x//variables.TILE_SIZE) == 13 and (self.rect.y//variables.TILE_SIZE) == 7)) and self.is_eyes == 1:
            self.turn_back()

        # Only make a decision when the ghost is aligned with the grid
        if self.rect.x % variables.TILE_SIZE == 0 and self.rect.y % variables.TILE_SIZE == 0:
            self.make_pathfinding_decision()

        # Update image based on direction
        if self.direction in variables.ghost_ani['red']:
            if self.power == 0:
                self.image = image.load(variables.ghost_ani['red'][self.direction][int(self.index)%2])
            elif self.is_eyes == 1:
                self.image = image.load(variables.eyes[self.direction])
            else:
                self.image = image.load(variables.white_ghost[int(self.index)%2])
        self.index += 0.2

        # Move the ghost based on its current direction
        if self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed

        # Wall collision detection to prevent going through walls (especially important in eyes mode)
        bricks = sprite.spritecollide(self, variables.brick_group, False)
        if bricks:
            for w in bricks:
                if self.direction == 'right':
                    self.rect.right = w.rect.left
                elif self.direction == 'left':
                    self.rect.left = w.rect.right
                elif self.direction == 'up':
                    self.rect.top = w.rect.bottom
                elif self.direction == 'down':
                    self.rect.bottom = w.rect.top
            
            # Align to grid to ensure we can make pathfinding decisions
            self.rect.x = (self.rect.x // variables.TILE_SIZE) * variables.TILE_SIZE
            self.rect.y = (self.rect.y // variables.TILE_SIZE) * variables.TILE_SIZE
            
            # Immediately recalculate direction since we hit a wall
            self.make_pathfinding_decision()

    def update_power(self):
        if variables.power == 1: self.power = 1
        if variables.power == 0: self.power = 0
    def get_tile_coords(self):
        """Returns the ghost's current tile coordinates (col, row)."""
        return (self.rect.centerx // variables.TILE_SIZE, self.rect.centery // variables.TILE_SIZE)

    def turn_into_eyes(self):
        self.is_eyes = 1
        self.speed = 10
        self.normal_speed = 10
        # If already grid-aligned, immediately recalculate path to ghost house
        if self.rect.x % variables.TILE_SIZE == 0 and self.rect.y % variables.TILE_SIZE == 0:
            self.make_pathfinding_decision()
    def turn_back(self):
        # print('test')
        self.power = 0
        self.speed = 5
        self.normal_speed = 5
        self.is_eyes = 0
    def make_pathfinding_decision(self):

        if self.power == 1 and self.is_eyes == 0:
            # Frightened Mode: Pick a random, valid tile as the target
            while True:
                rand_col = randint(0, len(variables.game_map[0]) - 1)
                rand_row = randint(0, len(variables.game_map) - 1)
                # Make sure the random tile is not a wall
                if variables.game_map[rand_row][rand_col] != '-':
                    self.target_tile = (rand_col, rand_row)
                    break # Exit the loop once a valid tile is found

        # 1. Set the target tile to Pac-Man's current tile
        else:
            if self.is_eyes == 0:
                self.target_tile = (pac_man.rect.centerx // variables.TILE_SIZE, pac_man.rect.centery // variables.TILE_SIZE)
            elif self.is_eyes == 1:
                self.target_tile = (10, 7)
        # 2. Get possible directions
        possible_directions = self.get_possible_directions()

        # 3. Find the best direction
        best_direction = ''
        min_distance = float('inf')

        for direction in possible_directions:
            # Get the tile that this direction would lead to
            next_tile = self.get_next_tile(direction)
            
            # Calculate distance from that future tile to the target
            distance = get_distance(next_tile, self.target_tile)

            # If this path is shorter, it's our new best choice
            if distance < min_distance:
                min_distance = distance
                best_direction = direction
        
        # 4. Commit to the best direction
        if best_direction:
            self.last_direction = self.direction
            self.direction = best_direction

    def get_possible_directions(self):
        """Checks surroundings for valid paths, excluding walls and reversing."""
        current_tile_col, current_tile_row = self.get_tile_coords()
        directions = []

        # Get map dimensions
        map_height = len(variables.game_map)
        map_width = len(variables.game_map[0])

        # Define opposites to prevent reversing
        opposites = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}

        # Check UP
        if current_tile_row > 0 and \
           variables.game_map[current_tile_row - 1][current_tile_col] != '-' and \
           self.direction != 'down':
            directions.append('up')
            
        # Check DOWN
        if current_tile_row < map_height - 1 and \
           variables.game_map[current_tile_row + 1][current_tile_col] != '-' and \
           self.direction != 'up':
            directions.append('down')
            
        # Check LEFT
        if current_tile_col > 0 and \
           variables.game_map[current_tile_row][current_tile_col - 1] != '-' and \
           self.direction != 'right':
            directions.append('left')
            
        # Check RIGHT
        if current_tile_col < map_width - 1 and \
           variables.game_map[current_tile_row][current_tile_col + 1] != '-' and \
           self.direction != 'left':
            directions.append('right')
        
        # This handles dead ends where the only option is to reverse
        if not directions and opposites.get(self.direction):
            return [opposites[self.direction]]

        return directions

    def get_next_tile(self, direction):
        """Gets the coordinates of the tile in a given direction."""
        col, row = self.get_tile_coords()
        if direction == 'up':
            return (col, row - 1)
        if direction == 'down':
            return (col, row + 1)
        if direction == 'left':
            return (col - 1, row)
        if direction == 'right':
            return (col + 1, row)
        return (col, row)       



class  Ghost (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load(variables.white_ghost[0])
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        self.direction = choice(['left', 'right', 'up', 'down'])
        self.speed = 7
        self.cheat_speed=0
        self.normal_speed=7 
        self.index = 1
    def update(self):
        # cheat
        if variables.ghost_freeze == True:
            self.speed=self.cheat_speed
        else:
            self.speed=self.normal_speed
        self.image = image.load(variables.white_ghost[int(self.index)%2])
        self.index+=1
        if self.direction == 'left':
            self.rect.x-=self.speed
        elif self.direction == 'right':
            self.rect.x+=self.speed
        bricks=sprite.spritecollide(self, variables.brick_group, False)
        for w in bricks:
            if self.direction == 'right':
                self.rect.right=w.rect.left
                # self.speed=0
                if self.rect.y<pac_man.rect.y:
                    self.direction='down'
                else:
                    self.direction='up' 
                # self.direction = choice(['up', 'down'])
            elif self.direction == 'left':
                self.rect.left=w.rect.right
                # self.speed=0
                # if self.rect.y<pac_man.rect.y:
                #     self.direction='down'
                # else:
                #     self.direction='up'
                self.direction = choice(['up', 'down'])
        if self.direction == 'up':
            self.rect.y-=self.speed
        elif self.direction == 'down':
            self.rect.y+=self.speed
        bricks=sprite.spritecollide(self, variables.brick_group, False)
        for w in bricks:
            if self.direction == 'up':
                self.rect.top=w.rect.bottom
                # self.speed=0
                if self.rect.x<pac_man.rect.x:
                    self.direction='right'
                else:
                    self.direction='left'
                # self.direction = choice(['left', 'right'])
            elif self.direction == 'down':
                self.rect.bottom=w.rect.top
                # self.speed=0
                # if self.rect.x<pac_man.rect.x:
                #     self.direction='right'
                # else:
                #     self.direction='left'
                self.direction = choice(['left', 'right'])
        
        


class  Pac_Man (sprite.Sprite):
    def __init__(self, x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load('assets/pac man 2.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        # Store spawn position for reliable respawn
        self.spawn_x = x
        self.spawn_y = y
        self.direction = 'right'
        self.desired_direction = 'right'  # Added for classic movement
        self.speed = 0
        self.y_speed = 0
        self.index = 1
        self.speed_change=10
        self.cheat_speed_change=15
        self.normal_speed_change=10
        # Death animation state
        self.is_dying = False
        self.death_frame = 1
        self.last_death_frame_time = 0
        self.pink_ghost_power = 0
        self.red_ghost_power = 0
    def death(self):
        global pac_update, begin, life
        # Start death animation (non-blocking)
        variables.life-=1
        self.rect.y+=10
        if not self.is_dying:
            mixer.Sound.play(variables.death_sound)
            variables.pac_update=1
            variables.begin=-1
            self.is_dying = True
            self.death_frame = 1
            self.last_death_frame_time = time.get_ticks()
    def update(self):
        global run, begin, pac_update, cheat_speed
        # cheat speed
        if variables.cheat_speed == True:
            self.speed_change=self.cheat_speed_change
        else:
            self.speed_change=self.normal_speed_change
        # Avoid retriggering death while already dying
        
        self.pink_ghost_power = check_ghost_power('pink')
        self.red_ghost_power = check_ghost_power('red')

        if (not self.is_dying) and sprite.spritecollide(self, variables.ghosts, False):
            if (sprite.spritecollide(self, variables.pink_group, False) and self.pink_ghost_power == 0) or (sprite.spritecollide(self, variables.red_group, False) and self.red_ghost_power == 0):
                self.death()
        # if (not self.is_dying) and self.rect.colliderect(pink_ghost.rect) and pink_ghost.power:
        #     self.death()
        # If in death animation, advance frames over time and stop normal updates
        if self.is_dying:
            now = time.get_ticks()
            self.image = image.load('assets/pac man 3.png')
            # time.delay(100)
            if self.death_frame <= 10 and now - self.last_death_frame_time >= 100:
                self.image = image.load(f'death {self.death_frame}.png')
                time.delay(100)
                self.death_frame += 1
                self.last_death_frame_time = now
            elif self.death_frame > 10 and variables.life == 0:
                self.kill()
                run=False
            elif self.death_frame > 10 and variables.life > 0:
                # Respawn: reset state and hand control back to main loop for Ready/
                global begin
                self.is_dying = False
                self.death_frame = 1
                self.rect.topleft = [self.spawn_x, self.spawn_y]
                self.direction = 'right'
                self.desired_direction = 'right'
                self.speed = 0
                self.y_speed = 0
                variables.pac_update = 0
                
                self.image=image.load('assets/pac man 2.png')
                clear_groups()
                draw_map(False)
                variables.begin = -3
                # print('test')
                # text('Go!', width//2-40, height//2-20, 'green', 50)
                # display.update()
                # time.delay(1000)
                # display.update()
                # begin=1
            return
        # Animation logic
        if self.direction == 'right' and self.speed != 0:
            self.image = image.load(variables.right[int(self.index)%4])
        if self.direction == 'left' and self.speed != 0:
            self.image = image.load(variables.left[int(self.index)%4])
        if self.direction == 'up' and self.y_speed != 0:
            self.image = image.load(variables.up[int(self.index)%4])
        if self.direction == 'down' and self.y_speed != 0:
            self.image = image.load(variables.down[int(self.index)%4])
        self.index+=0.5
        keys = key.get_pressed()
        # Set desired direction on key press
        if keys[K_RIGHT]:
            self.desired_direction = 'right'
        elif keys[K_LEFT]:
            self.desired_direction = 'left'
        elif keys[K_UP]:
            self.desired_direction = 'up'
        elif keys[K_DOWN]:
            self.desired_direction = 'down'
        # Try to turn if possible (simulate the turn)
        dx, dy = 0, 0
        if self.desired_direction == 'right':
            dx = 10
        elif self.desired_direction == 'left':
            dx = -10
        elif self.desired_direction == 'up':
            dy = -10
        elif self.desired_direction == 'down':
            dy = 10
        self.rect.x += dx
        self.rect.y += dy
        bricks = sprite.spritecollide(self, variables.brick_group, False)
        if not bricks:
            self.direction = self.desired_direction
        self.rect.x -= dx
        self.rect.y -= dy
        # Always set speed/y_speed based on current direction
        if self.direction == 'right':
            self.speed = self.speed_change
            self.y_speed = 0
        elif self.direction == 'left':
            self.speed = -self.speed_change
            self.y_speed = 0
        elif self.direction == 'up':
            self.speed = 0
            self.y_speed = -self.speed_change
        elif self.direction == 'down':
            self.speed = 0
            self.y_speed = self.speed_change
        # Move Pac-Man in the current direction
        self.rect.x += self.speed
        self.rect.y += self.y_speed
        # Wall collision (horizontal)
        bricks=sprite.spritecollide(self, variables.brick_group, False)
        for w in bricks:
            if self.direction == 'right':
                self.rect.right=w.rect.left
                self.speed=0
                self.image = image.load('assets/pac man 2.png')
                display.update()
            elif self.direction == 'left':
                self.rect.left=w.rect.right
                self.speed=0
                self.image = image.load('assets/pac man 2-left.png')
                display.update()
        # Wall collision (vertical)
        bricks=sprite.spritecollide(self, variables.brick_group, False)
        for w in bricks:
            if self.direction == 'up':
                self.rect.top=w.rect.bottom
                self.y_speed=0
            if self.direction == 'down':
                self.rect.bottom=w.rect.top
                self.y_speed=0