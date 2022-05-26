#from nes_py.wrappers import JoypadSpace

from src.config import (
    sprites_paths,
    threshold,
    rom,
    actions
)

from kitsune import Kitsune

"""
#while True:
    # Close visualization
    #if (cv2.waitKey(1) & 0xFF) == ord('q'):
        #cv2.destroyAllWindows()
        #break

    #look_to_game(show=True)

    #((1 sec / FPS) - exec_time) = wait time
    #wait_time = (1/FPS) - (time.time() - start_time)
    #time.sleep(wait_time)
"""

def main():
    kitsune = Kitsune(
        rom = rom,
        sprites_paths = sprites_paths,
        env_actions = actions,
    )

    kitsune.start()


if __name__ == "__main__":
    main()
