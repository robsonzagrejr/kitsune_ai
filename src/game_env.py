"""
https://github.com/Kautenja/nes-py
https://github.com/Kautenja/gym-super-mario-bros
"""
from nes_py import NESEnv


class SuperMarioBrosEnv(NESEnv):
    """An environment for playing Super Mario Bros with OpenAI Gym."""

    # the legal range of rewards for each step
    reward_range = (-15, 15)

    def __init__(self, rom):
        """
        Initialize a new Super Mario Bros environment.
        Args:
            rom_mode (str): the ROM mode to use when loading ROMs from disk
            lost_levels (bool): whether to load the ROM with lost levels.
                - False: load original Super Mario Bros.
                - True: load Super Mario Bros. Lost Levels
            target (tuple): a tuple of the (world, stage) to play as a level
        Returns:
            None
        """
        # decode the ROM path based on mode and lost levels flag
        #rom = rom_path(lost_levels, rom_mode)
        # initialize the super object with the ROM path
        super(SuperMarioBrosEnv, self).__init__(rom)
        # set the target world, stage, and area variables
        #target = decode_target(target, lost_levels)
        #self._target_world, self._target_stage, self._target_area = target
        # setup a variable to keep track of the last frames time
        self._time_last = 0
        # setup a variable to keep track of the last frames x position
        self._x_position_last = 0
        # reset the emulator
        self.reset()
        # skip the start screen
        #self._skip_start_screen()
        # create a backup state to restore from on subsequent calls to reset
        self._backup()

