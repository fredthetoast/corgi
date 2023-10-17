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
        self.dir = 0
        self.cur = 0
        self.speed = 0

    def render(self, screen):
        """Display sprite on screen."""
        # screen.blit(self.textures[self.dir][self.cur])
        anim_line = self.textures[self.dir]
        tex = anim_line[int(self.cur) % len(anim_line)]
        screen.blit(tex, self.pos)

    def animate(self, dt):
        """Moves the sprite according to speed and direction"""
        self.cur = (self.cur + dt * self.speed)
        x, y = self.pos

        dp = self.speed / 5.0
        if self.dir == SPRITE_DOWN:
            y = y + dp
        elif self.dir == SPRITE_UP:
            y = y - dp
        elif self.dir == SPRITE_LEFT:
            x = x - dp
        elif self.dir == SPRITE_RIGHT:
            x = x + dp

        if x > 1200:
            x = -80
        elif x < -80:
            x = 1200

        if y > 800:
            y = -80
        elif y < -80:
            y = 800

        self.pos = (x, y)
        # self.pos[1] ....

    def set_pos(self, pos):
        self.pos = pos

    def set_speed(self, speed):
        self.speed = speed

    def set_direction(self, dir):
        self.dir = dir
    

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

    if is_key_pressed(pygame.K_w):
        dog.set_direction(SPRITE_UP)
        dog.set_speed(dog_speed)
    elif is_key_pressed(pygame.K_s):
        dog.set_direction(SPRITE_DOWN)
        dog.set_speed(dog_speed)
    elif is_key_pressed(pygame.K_a):
        dog.set_direction(SPRITE_LEFT)
        dog.set_speed(dog_speed)
    elif is_key_pressed(pygame.K_d):
        dog.set_direction(SPRITE_RIGHT)
        dog.set_speed(dog_speed)
    else:
        dog.set_speed(0)

    # sprint
    if is_key_pressed(pygame.K_LSHIFT):
        dog.set_speed(dog_sprint_speed)

    dog.animate(dt)
    dog.render(screen)

    if is_key_pressed(pygame.K_ESCAPE):
        return MODE_SPLASH

    return MODE_NORMAL


def render_text(screen, font, text, pos, antialiasing, color):
    thefont = font
    label = thefont.render(text, antialiasing, (color) )
    screen.blit(label, (pos))


def render_splash(screen, dt):
    myfont = pygame.font.Font("assets/fonts/Pokemon_GB.ttf", 32)  
    menu_image = pygame.image.load('assets/backgrounds/menu_image.png')

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
    
