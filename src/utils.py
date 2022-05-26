import pyglet


def get_pyglet_image(image):
    return pyglet.image.ImageData(
        image.shape[1],
        image.shape[0],
        'RGB',
        image.tobytes(),
        pitch=image.shape[1]*-3
    )

