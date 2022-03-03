import os
import pygame

class Sounds:

    SOUND_EFFECT_FOLDER = "../../res/music/sounds/"
    MUSIC_FOLDER = "../../res/music/music/"
    EXTENTIONS = [ ".wav" ]

    __soundEffects : dict[str, pygame.mixer.Sound] = {}

    __musicOn  = True
    __soundsOn = True

    @staticmethod
    def loadAll() -> None:
        path = os.path.join(os.path.dirname(__file__), Sounds.SOUND_EFFECT_FOLDER)
        for root, _, files in os.walk(path):
            for file in files:
                [ filename, extention ] = os.path.splitext(file)
                if extention in Sounds.EXTENTIONS:
                    key = filename
                    Sounds.__soundEffects[key] = pygame.mixer.Sound(os.path.join(root, file))
                    
    
    @staticmethod
    def playSoundEffect(name : str) -> None:
        if Sounds.__soundsOn:
            Sounds.__soundEffects[name].play()

    
    @staticmethod
    def playMusic(name : str, fileExt : str = ".wav") -> None:
        path = os.path.join(os.path.dirname(__file__), Sounds.MUSIC_FOLDER)
        
        pygame.mixer.music.unload()
        pygame.mixer.music.load(path + name + fileExt)
        pygame.mixer.music.play(-1)
    
    @staticmethod
    def stopMusic() -> None:
        pygame.mixer.music.stop()
    
    @staticmethod
    def stopAllSoundEffects() -> None:
        pygame.mixer.stop()
    
    # MUTE CONTROL

    @staticmethod
    def isMusicOn() -> bool:
        return Sounds.__musicOn
    
    @staticmethod
    def areSoundsOn() -> bool:
        return Sounds.__soundsOn
    
    @staticmethod
    def setMusicOn(value : bool) -> None:
        Sounds.__musicOn = value
        if value:
            pygame.mixer.music.set_volume(1)
        else:
            pygame.mixer.music.set_volume(0)
    
    @staticmethod
    def setSoundsOn(value : bool) -> None:
        Sounds.__soundsOn = value

        if not value:
            Sounds.stopAllSoundEffects()
