import pygame
import sys

MODE_NORMAL = 0
MODE_SPLASH = 1
MODE_INVENTORY = 2
MODE_SHOP = 3

SPRITE_DOWN = 0
SPRITE_LEFT = 1
SPRITE_RIGHT = 2
SPRITE_UP = 3

DOG_SHEET= {
    "filename": "assets/sprites/dog.png",
    "animations": {
        SPRITE_DOWN: [
            (0, 0, 80, 80), (80, 0, 80, 80), (160, 0, 80, 80), (240, 0, 80, 80)
        ],
        SPRITE_LEFT: [
            (0, 80, 80, 80), (80, 80, 80, 80), (160, 80, 80, 80), (240, 80, 80, 80)
        ],
        SPRITE_RIGHT: [
            (0, 160, 80, 80), (80, 160, 80, 80), (160, 160, 80, 80), (240, 160, 80, 80)
        ],
        SPRITE_UP: [
            (0, 240, 80, 80), (80, 240, 80, 80), (160, 240, 80, 80), (240, 240, 80, 80)
        ],
    }
}


def sheet_textures(sheet):
    tex = load_texture(sheet["filename"])
    anim = sheet["animations"]

    res = {}
    for dir, line in anim.items():
        anim_line = []
        for i in line:
            anim_line.append(tex.subsurface(i))
        res[dir] = anim_line

    return res

def init():
    pygame.init()
    width, height = 1200, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("l'aventure du corgi")
    clock = pygame.time.Clock()
 
    return (screen, clock)

class SpriteAnim():
    def __init__(self, pos, tex_array):
        self.pos = pos
        self.textures = tex_array
        self.cur = 0
        self.speed = (0, 0)


    def render(self, screen, dt):
        """Display sprite on screen."""

        # move is more horizontal or vertical?
        dir = 0
        speed = 0

        if abs(self.speed[0]) > abs(self.speed[1]):
            
            # left or right?
            if self.speed[0] > 0:
                dir = SPRITE_RIGHT
            else:
                dir = SPRITE_LEFT
            
            speed = abs(self.speed[0])
        
        else:
            # up or down?
            if self.speed[1] > 0:
                dir = SPRITE_DOWN
            else:
                dir = SPRITE_UP

            speed = abs(self.speed[1])

        self.cur += dt * speed * 2.0

        anim_line = self.textures[dir]
        tex = anim_line[int(self.cur) % len(anim_line)]
        
        screen.blit(tex, self.pos)


    def animate(self, dt, accel):
        """Moves the sprite according to speed and direction"""

        ax, ay = accel
        if ax == 0:
            ax = -self.speed[0]

        if ay == 0:
            ay = -self.speed[1]

        self.speed = (self.speed[0] + ax * dt,
                      self.speed[1] + ay * dt)

        if self.speed[0] > 8:
            self.speed = (8, self.speed[1])

        if self.speed[0] < -8:
            self.speed = (-8, self.speed[1])

        if self.speed[1] > 8:
            self.speed = (self.speed[0], 8)

        if self.speed[1] < -8:
            self.speed = (self.speed[0], -8)

        x, y = self.pos
        dp = (self.speed[0], self.speed[1])

        x = x + dp[0]
        y = y + dp[1]
        
        if x > 1200:
            x = -80
        elif x < -80:
            x = 1200

        if y > 800:
            y = -80
        elif y < -80:
            y = 800

        self.pos = (x, y)


    def decay(self, dt):
        pass
        # if self.speed > 0.0:
        #     before = self.speed
        #     decay = dt * 25.0
        #     if self.speed > decay:
        #         self.speed = self.speed - decay
        #     else:
        #         self.speed = 0
        #     print(f'Speed: before={before} after={self.speed}')

    def set_pos(self, pos):
        self.pos = pos

    def set_speed(self, speed):
        self.speed = speed
    

def load_texture(filename):
    tex = pygame.image.load(filename)
    tex.set_colorkey(tex.get_at((0, 0)))
    return tex


# drawing everything on the screen
def place_texture(texture_name, step, width, height):
    for x in range(0, width, step):
        for y in range(0, height, step):
            screen.blit(texture_name, (x, y))


def is_key_pressed(key):
    return pygame.key.get_pressed()[key]


def render_normal(screen, dt):

    place_texture(grass, 225, 1200, 800)            

    dir = (0, 0)
    if is_key_pressed(pygame.K_w):
        dir = (0, -1)
    elif is_key_pressed(pygame.K_s):
        dir = (0, 1)
    elif is_key_pressed(pygame.K_a):
        dir = (-1, 0)
    elif is_key_pressed(pygame.K_d):
        dir = (1, 0)
    
    # sprint
    speed = dog_speed
    if is_key_pressed(pygame.K_LSHIFT):
        speed = dog_sprint_speed

    accel = (dir[0] * speed, dir[1] * speed)        

    dog.animate(dt, accel)
    dog.render(screen, dt)

    dog.decay(dt)

    render_text(screen, myfont,
        f'Speed: {int(dog.speed[0])} {int(dog.speed[1])}',
        (5, 5), 0, ('black'))

    if is_key_pressed(pygame.K_ESCAPE):
        return MODE_SPLASH

    return MODE_NORMAL


def render_text(screen, font, text, pos, antialiasing, color):
    label = font.render(text, antialiasing, (color) )
    screen.blit(label, (pos))


def render_splash(screen, dt):

    menu = pygame.transform.scale(menu_image, (1200, 800))
    screen.blit(menu, (0, 0))

    # blitting text on to menu
    render_text(screen, myfont, "Go Corgi", (450, 500), 0, ('black') )
    render_text(screen, myfont, "[SPACE]", (470,537 ), 0, ('black'))

    if is_key_pressed(pygame.K_SPACE):
        return MODE_NORMAL

    return MODE_SPLASH


# main program
screen, clock = init()
game_running = True
    
grass_img = pygame.image.load("assets/backgrounds/grass.png")
grass = pygame.transform.scale(grass_img,(225, 225))

myfont = pygame.font.Font("assets/fonts/Pokemon_GB.ttf", 32)  
menu_image = pygame.image.load('assets/backgrounds/menu_image.png')

dog_speed = 12
dog_sprint_speed = 20
dog = SpriteAnim((0, 0), sheet_textures(DOG_SHEET))

game_mode = MODE_NORMAL

mode_routines = {
    MODE_NORMAL: render_normal,
    MODE_SPLASH: render_splash
}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    dt = clock.tick(60) / 1000.0

    mode_fct = mode_routines[game_mode]
    game_mode = mode_fct(screen, dt)

    pygame.display.update()
    
