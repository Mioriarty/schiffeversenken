from components.ui.ImageButton import ImageButton
from scenes.Scene import Scene
from utils.Images import Sprite
from utils.Transform import Transform


class MenuScene(Scene):

    def __init__(self):
        super().__init__((255, 255, 255))
        self.leftButton = ImageButton(Sprite("buttons.left"), transform = Transform((200, 200), scale=(0.2, 0.2)))
        self.leftButton.setOnClickEvent(lambda : print("Left"))

        self.rightButton = ImageButton(Sprite("buttons.right"), transform = Transform((800, 200), scale=(0.2, 0.2)))
        self.rightButton.setOnClickEvent(lambda : print("Right"))