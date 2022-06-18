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
    ['NOOP'],            #0
    ['right'],           #1
    ['right', 'A'],      #2
    ['right', 'B'],      #3
    ['right', 'A', 'B'], #4
    ['left'],            #5
    ['left', 'A'],       #6
    ['left', 'B'],       #7
    ['left', 'A', 'B'],  #8
    ['down'],            #9
    ['up'],              #10
    ['A'],               #11
    ['B'],               #12
    ['start'],           #13
    ['select'],          #14
]

screen = {
    "w": 1280,
    "h": 720,
}

kitsune_images = {
    "normal": base_path + "/assets/fox.png",
}
