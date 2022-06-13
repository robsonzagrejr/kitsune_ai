from src.config import (
    sprites_paths,
    threshold,
    rom,
    actions
)

from src.kitsune import Kitsune

def main():
    kitsune = Kitsune(
        rom = rom,
        sprites_paths = sprites_paths,
        env_actions = actions,
    )

    kitsune.start()


if __name__ == "__main__":
    main()
