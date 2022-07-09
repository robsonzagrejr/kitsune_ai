import pyglet
import time
import cv2 as cv

from src.kitsune_env import KitsuneEnv 
from src.kitsune_view import KitsuneView
from src.kitsune_agent import KitsuneAgent

from src.config import (
    screen,
    kitsune_images,
)

from src.utils import (
    get_pyglet_image
)


class Kitsune():

    def __init__(self, rom, sprites_paths, env_actions, is_training):
        self._window = pyglet.window.Window(width=screen['w'],height=screen['h'])
        self._is_training = is_training

        self.env   = KitsuneEnv(rom, env_actions, self._window, self._is_training)
        self.view  = KitsuneView(sprites_paths)
        self.agent = KitsuneAgent(self.env, self.view)

        self.images = {
            "normal": get_pyglet_image(
                cv.cvtColor(
                    cv.imread(kitsune_images['normal'], 3),
                    cv.COLOR_BGR2RGB
                )
            )
        }

        self._window.event(self.on_draw)

        #self.play()


    def get_kitsune_image(self):
        return self.images['normal']
 

    def _play_game(self, dt):
        return


    def play(self):
        pyglet.clock.schedule_interval(self._play_game, 0.01)


    def stop_play(self):
        pyglet.clock.unschedule(self._play_game)


    def start(self):
        pyglet.app.run()


    def on_draw(self):
        self._window.clear()

        # Game Image
        if self.agent._frame is not None:
            get_pyglet_image(self.agent._frame).blit(
                x=0, y=0,
                width=self._window.width//2, height=self._window.height//2
            )

        # Kitsune View
        if self.view.frame_obj is not None:
            get_pyglet_image(self.view.frame_obj).blit(
                self._window.width//2,0,
                width=self._window.width//2, height=self._window.height//2
            )

        # FPS
        fps_label = pyglet.text.Label(f'FPS: {pyglet.clock.get_fps()}',
            font_name='Times New Roman',
            font_size=12,
            x=10, y=self._window._height-20,
            anchor_x='left', anchor_y='top'
        )
        fps_label.draw()

        # Mode
        mode = "Keyboard" if self.env.key_mode else "Auto"
        mode_label = pyglet.text.Label(f'Mode: {mode}',
            font_name='Times New Roman',
            font_size=12,
            x=self._window.width-10, y=self._window._height-20,
            anchor_x='right', anchor_y='top'
        )
        mode_label.draw()

        # Reward
        reward = self.env.info.get('reward', [0])[0]
        reward_label = pyglet.text.Label(f'Reward: {reward}',
            font_name='Times New Roman',
            font_size=12,
            x=10, y=self._window._height-60,
            anchor_x='left', anchor_y='top'
        )
        reward_label.draw()

        # Step 
        step= self.env.n_step
        step_label = pyglet.text.Label(f'Step: {step}',
            font_name='Times New Roman',
            font_size=12,
            x=10, y=self._window._height-80,
            anchor_x='left', anchor_y='top'
        )
        step_label.draw()

        # Episode 
        episode= self.env.episode
        episode_label= pyglet.text.Label(f'Episode: {episode}',
            font_name='Times New Roman',
            font_size=12,
            x=10, y=self._window._height-100,
            anchor_x='left', anchor_y='top'
        )
        episode_label.draw()
        
        # Score
        score = self.env.score
        score_label= pyglet.text.Label(f'Score: {score}',
            font_name='Times New Roman',
            font_size=12,
            x=10, y=self._window._height-120,
            anchor_x='left', anchor_y='top'
        )
        score_label.draw()


        # Kitsune
        self.get_kitsune_image().blit(
            self._window.width//4,self._window.height//2,
            width=self._window.width//2, height=self._window.height//2
        )

