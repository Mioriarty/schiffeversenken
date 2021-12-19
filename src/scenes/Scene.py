class Scene:

    def start(self) -> None:
        pass

    def destroy(self) -> None:
        pass



class SceneManager:

    __currentScene : Scene = None

    @staticmethod
    def loadScene(scene : Scene) -> None:
        if SceneManager.__currentScene != None:
            SceneManager.__currentScene.destroy()
        
        SceneManager.__currentScene = scene
        SceneManager.__currentScene.start()

