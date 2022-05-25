import os
import glob

base_path = os.path.dirname(__file__)

#Sprites to detect
sprites_paths = glob.glob(base_path + "/assets/sprites/**/*.png", recursive=True)

#Game Room
rom = base_path + "/assets/rom/super-mario-bros.nes"

threshold = 0.75


#The standard display resolution of the NES is 256 horizontal pixels by 240 vertical pixels. 
resolution = {"w":256, "h":240}
screen_size = (1920, 1080) # 16/9
screen_ratio = (16,9)
game_ratio = (4,3)
prop = screen_ratio[1] / game_ratio[1]

bounding_box = {
    'top': 25,
    'left':int(1920 + (screen_size[0] / screen_ratio[0]
        * ((screen_ratio[0]/game_ratio[0]) / 3)) + 7),
    'width':int((screen_size[0] / screen_ratio[0]) * game_ratio[0] * prop
        + (47*prop)),
    'height': screen_size[1] - 25,
}

actions = [
    ['NOOP'],
    ['right'],
    ['right', 'A'],
    ['right', 'B'],
    ['right', 'A', 'B'],
    ['left'],
    ['left', 'A'],
    ['left', 'B'],
    ['left', 'A', 'B'],
    ['down'],
    ['up'],
    ['A'],
    ['B'],
    ['start'],
    ['select'],
]
