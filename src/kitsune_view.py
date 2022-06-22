"""
https://github.com/vmorarji/Object-Detection-in-Mario
"""
import os
import random
import cv2 as cv
import numpy as np
import pyglet
import multiprocessing
from functools import partial

from src.config import (
    threshold
)

class KitsuneView():
    def __init__(self, sprites_path):
        self.sprites_path = sprites_path
        sprite_types = list(set([s.split("/")[-2] for s in sprites_path]))
        colors = {
            sprite_type: (
                random.randint(0,255),
                random.randint(0,255),
                random.randint(0,255)
            )
            for sprite_type in sprite_types
        }

        self.sprites = []
        for sprite_path in sprites_path:
            info = sprite_path.split("/")
            name = info[-1].split(".")[0].split("-")[0]
            img = np.array(cv.imread(sprite_path, 0))
            w, h = img.shape[::-1]
            # Add image
            self.sprites.append({
                "name": name,
                "id_type": sprite_types.index(info[-2]),
                "type": info[-2],
                "img": img,
                "color": colors[info[-2]],
                "path": sprite_path,
                "size": (w, h)
            })
            if info[-2] in ['player', 'enemie']:
                # Add mirroed image
                img_flip = cv.flip(img, 1)
                self.sprites.append({
                    "name": name,
                    "id_type": sprite_types.index(info[-2]),
                    "type": info[-2],
                    "img": img_flip,
                    "color": colors[info[-2]],
                    "path": sprite_path,
                    "size": (w, h)
                })
        self.frame_obj = None
        self.pool = multiprocessing.Pool(4)


    def find_objects(self, image):
        img_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        # Using parallelism to speedup the search
        objects = self.pool.map(
            partial(KitsuneView.find_sprite,img_gray=img_gray),
            self.sprites
        )
        # Removing None results
        objects = [obj for obj in objects if obj]

        return objects


    @staticmethod
    def find_sprite(sprite, img_gray):
        sprite_template = sprite["img"]
        result = cv.matchTemplate(np.array(img_gray), np.array(sprite_template), cv.TM_CCOEFF_NORMED)
        locales = np.where( result >= threshold)

        # Merging vertically sprites that is side by side
        locales_simple= {}
        aux = {}
        w = sprite["size"][0]
        h = sprite["size"][1]
        for pt in zip(*locales[::-1]):
            if pt[0] in locales_simple.keys():
                pos = locales_simple[pt[0]]

                #one is inside of other
                if ((pos[1] <= pt[1] <= (pos[1] + pos[3]))
                    or (pt[1] <= pos[1] <= (pt[1] + h))):
                    new_p = pos[1]
                    if pt[1] < pos[1]:
                        new_p = pt[1]
                    new_h = h + abs(pos[1] - pt[1])
                    locales_simple[pt[0]] = [
                        pos[0], int(new_p),
                        pos[2], int(new_h)
                    ]
                #they arent side by side
                else:
                    a = aux.get(pt[0], 0)
                    aux[pt[0]] = a+1
                    locales_simple[f'{pt[0]}_+{a}'] =  [
                        int(pt[0]), int(pt[1]),
                        int(w), int(h)
                    ]
            else:
                locales_simple[pt[0]] = [
                    int(pt[0]), int(pt[1]),
                    int(w), int(h)
                ]

        sprint_pts = list(locales_simple.values())

        if sprint_pts:
            #objects.append(
            return (
                {
                    "name": sprite["name"],
                    "type": sprite["type"],
                    "pts": sprint_pts,
                    "w": w,
                    "h": h,
                    "color": sprite["color"],
                }
            )


    def get_image_with_objects(self, image, objects):
        img_with_objs = image.copy()
        for obj in objects:
            for pt in obj['pts']:
                cv.putText(
                    img_with_objs, obj['name'],
                    (pt[0], pt[1]-5), cv.FONT_HERSHEY_SIMPLEX, 0.3,
                    obj['color'],
                    1, cv.LINE_AA
                )
                cv.rectangle(img_with_objs, pt[:2], (pt[0] + pt[2], pt[1] + pt[3]), obj["color"], 1)

        return img_with_objs 

