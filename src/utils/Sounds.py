import os
import pygame

class Sounds:

    SOUND_EFFECT_FOLDER = "./res/music/sounds/"
    MUSIC_FOLDER = "./res/music/music/"
    EXTENTIONS = [ ".wav" ]

    __soundEffects : dict[str, pygame.mixer.Sound] = {}

    __musicOn  = True
    __soundsOn = True

    @staticmethod
    def loadAll() -> None:
        for root, _, files in os.walk(Sounds.SOUND_EFFECT_FOLDER):
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
        pygame.mixer.music.unload()
        pygame.mixer.music.load(Sounds.MUSIC_FOLDER + name + fileExt)
        pygame.mixer.music.play(-1)
    
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
            pygame.mixer.stop()
