import pyglet

#define window size
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

# Load background image
#background = pyglet.resource.image("2D_background.png")
#background.width = WINDOW_WIDTH
#background.height = WINDOW_HEIGHT


# get a list of all low-level input devices:
#devices = pyglet.input.get_devices()
# get a list of all controllers:
#controllers = pyglet.input.get_controllers()
# get a list of all joysticks:
#joysticks = pyglet.input.get_joysticks()

window = pyglet.window.Window(width = WINDOW_WIDTH, height = WINDOW_HEIGHT, caption='Controlable GUI')
window.set_caption("Controllable 1D GUI")
#define font
font_size = 12
font_name = "Times New Roman"

# Player setup
diam = 40
pos_x = WINDOW_WIDTH // 2
pos_y = WINDOW_HEIGHT // 2
circle_batch = pyglet.graphics.Batch()
player = pyglet.shapes.Circle(pos_x, pos_y, diam // 2, color=(255, 0, 0), batch=circle_batch)
#score_zone = pyglet.shapes.Circle(pos_x, pos_y, diam // 2, color=(255, 0, 0), batch=circle_batch)


# Label setup
labels = {
    "controllers": pyglet.text.Label("Controllers: 0", font_name=font_name,
                                     font_size=font_size, x=10, y=WINDOW_HEIGHT - 20,
                                     anchor_x='left', anchor_y='top', color=(240, 255, 255, 255)),
    "name": pyglet.text.Label("", font_name=font_name, font_size=font_size,
                              x=10, y=WINDOW_HEIGHT - 40, anchor_x='left', anchor_y='top',
                              color=(240, 255, 255, 255)),
}
    

controller_manager = pyglet.input.ControllerManager()
controllers = controller_manager.get_controllers()

if controllers:
    controller = controllers[0]
    controller.open()
    labels["controllers"].text = "Controllers: 1"
else:
    print("[Error] No controller detected. Please connect a controller")
    labels["controllers"].text = "Controllers: 0"

#Controller Connection
@controller_manager.event
def on_connect(controller):
    labels["controllers"].text = "Controllers: 1"
    labels["name"].text = f"Controller Type: {controller.name}"
    print(f"Connected: {controller}")
@controller_manager.event
def on_disconnect(controller):
    labels["controllers"].text = "Controllers: 0"
    labels["name"].text = f"None"
    print(f"Disconnected: {controller}")

#Axis movement

@controller_manager.event
def on_stick_motion(value):
    x, y = controller.left_joystick
    print(f"Left Stick - X: {x:.2f}, Y: {y:.2f}")



@window.event
def on_draw():
    window.clear()
    #background.blit(0, 0)
    player.draw()
    for label in labels.values():
        label.draw()

pyglet.app.run()