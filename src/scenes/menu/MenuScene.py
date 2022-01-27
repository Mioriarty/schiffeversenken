from components.ambient.Diashow import Diashow
from components.ui.ImageButton import ImageButton
from scenes.Scene import Scene, SceneManager
from scenes.menu.DifficultySelect import DifficultySelect
from utils.Images import Sprite
from utils.Transform import Transform


class MenuScene(Scene):

    def __init__(self):
        super().__init__((255, 255, 255))
        self.headingSprite = Sprite("texts.seeschlacht", Transform.screenCenter(y = 100., scale=(0.5, 0.5)), bakeNow=True)
        SceneManager.putInDrawLayer(self.headingSprite, SceneManager.UI_MAIN_LAYER)
    
        self.difficultySelect = DifficultySelect(Transform.screenCenter(y = 250.))

        self.island = Diashow([ "ambient.island1", "ambient.island2" ], 0.5, Transform((100, 200), scale=(0.4, 0.4)))
        SceneManager.putInDrawLayer(self.island, SceneManager.UI_MAIN_LAYER)
    