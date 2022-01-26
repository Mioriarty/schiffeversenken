from components.ui.ImageButton import ImageButton
from scenes.Scene import Scene
from scenes.menu.DifficultySelect import DifficultySelect
from utils.Images import Sprite
from utils.Transform import Transform


class MenuScene(Scene):

    def __init__(self):
        super().__init__((255, 255, 255))
        

        self.difficultySelect = DifficultySelect(Transform((512, 200)))
    