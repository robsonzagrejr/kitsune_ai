"""
https://github.com/vmorarji/Object-Detection-in-Mario
"""
import os
import random
import cv2 as cv
import numpy as np
import pyglet

from src.config import (
    threshold
)

class KitsuneView():
    def __init__(self, sprites_path):
        self.sprites_path = sprites_path
        sprite_types = set([s.split("/")[-2] for s in sprites_path])
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
            img_flip = cv.flip(img, 1)
            w, h = img.shape[::-1]
            # Add image
            self.sprites.append({
                "name": name,
                "type": info[-2],
                "img": img,
                "color": colors[info[-2]],
                "path": sprite_path,
                "size": (w, h)
            })
            # Add mirroed image
            self.sprites.append({
                "name": name,
                "type": info[-2],
                "img": img_flip,
                "color": colors[info[-2]],
                "path": sprite_path,
                "size": (w, h)
            })
        self.frame_obj = None


    def find_objects(self, image):
        img_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        objects = {}
        for sprite in self.sprites:
            sprite_template = sprite["img"]
            result = cv.matchTemplate(np.array(img_gray), np.array(sprite_template), cv.TM_CCOEFF_NORMED)
            locales = np.where( result >= threshold)

            sprint_pts = [ pt for pt in zip(*locales[::-1])]
            if sprint_pts:
                if not objects.get(type):
                    objects[type] = []
                objects[type].append(
                    {
                        "name": sprite["name"],
                        "type": sprite["type"],
                        "pts": [[int(x[0]), int(x[1])] for x in sprint_pts],
                        "w": sprite["size"][0],
                        "h": sprite["size"][1],
                        "color": sprite["color"],
                    }
                )

        return objects


    def get_image_with_objects(self, image, objects):
        img_with_objs = image.copy()
        for objs_types in objects.values():
            for obj in objs_types:
                for pt in obj['pts']:
                    cv.putText(
                        img_with_objs, obj['name'],
                        (pt[0], pt[1]-5), cv.FONT_HERSHEY_SIMPLEX, 0.3,
                        obj['color'],
                        1, cv.LINE_AA
                    )
                    cv.rectangle(img_with_objs, pt, (pt[0] +obj['w'], pt[1] + obj['h']), obj["color"], 1)

        return img_with_objs 

