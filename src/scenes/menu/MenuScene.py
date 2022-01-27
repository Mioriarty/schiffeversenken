from components.ambient.Diashow import Diashow
from components.ui.ImageButton import ImageButton
from scenes.Scene import Scene, SceneManager
from scenes.menu.DifficultySelect import DifficultySelect
from utils.Images import Sprite
from utils.Transform import Transform


class MenuScene(Scene):

    def __init__(self):
        super().__init__((255, 255, 255))
    
        self.difficultySelect = DifficultySelect(Transform((512, 200)))

        self.island = Diashow([ "ambient.island1", "ambient.island2" ], 0.5, SceneManager.UI_MAIN_LAYER, Transform((200, 200), scale=(0.5, 0.5)))
    