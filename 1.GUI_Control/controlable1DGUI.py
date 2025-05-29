import pygame

pygame.init()

#define screen size
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

#create "game" window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Controlable 1D GUI")

#define font
font_size = 12
font = pygame.font.SysFont("Futura", font_size)

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#initialise the joystick module
pygame.joystick.init()

#create empty list to store joysticks
joysticks = []

#setting game frame rate
clock = pygame.time.Clock()
FPS = 60

#create player agent
diam = 30
size_x = diam
size_y = diam
pos_x = SCREEN_WIDTH/2
pos_y = SCREEN_HEIGHT/2
player = pygame.Rect(size_x, size_y, pos_x, pos_y)

#define player colour
player_colour = "red"

#game loop
run = True
while run:
    clock.tick(FPS)

    #update blackground
    screen.fill(pygame.Color("black"))

    #draw player agent
    player.center = (pos_x, pos_y)
    pygame.draw.circle(screen, pygame.Color(player_colour), player.center, diam/2)

    #show number of connected joysticks
    draw_text("Controllers: " + str(pygame.joystick.get_count()), font, pygame.Color("azure"), 10, 10)
    for joystick in joysticks:
        draw_text("Battery Level: " + str(joystick.get_power_level()), font, pygame.Color("azure"), 10, 35)
        draw_text("Controller Type: " + str(joystick.get_name()), font, pygame.Color("azure"), 10, 60)
        draw_text("Number of axes: " + str(joystick.get_numaxes()), font, pygame.Color("azure"), 10, 85)

        vert_move = joystick.get_axis(1)
        if abs(vert_move) > 0.05:
            pos_y = SCREEN_HEIGHT/2 + vert_move * 200
        
    #event handling
    for event in pygame.event.get():
        
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks.append(joy)
        
        #quit program
        if event.type == pygame.QUIT:
            run = False
    
    #update display
    pygame.display.flip()

pygame.quit()