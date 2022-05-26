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

screen = {
    "w": 1280,
    "h": 720,
}

kitsune_images = {
    "normal": base_path + "/assets/fox.png",
}
