import os
import pygame

class Sounds:

    SOUND_EFFECT_FOLDER = "./res/music/sounds/"
    MUSIC_FOLDER = "./res/music/music/"
    EXTENTIONS = [ ".wav" ]

    __soundEffects : dict[str, pygame.mixer.Sound] = {}

    @staticmethod
    def loadAll() -> None:
        for root, _, files in os.walk(Sounds.SOUND_EFFECT_FOLDER):
            for file in files:
                [ filename, extention ] = os.path.splitext(file)
                print(filename, extention)
                if extention in Sounds.EXTENTIONS:
                    key = filename
                    Sounds.__soundEffects[key] = pygame.mixer.Sound(os.path.join(root, file))
                    
    
    @staticmethod
    def playSoundEffect(name : str) -> None:
        Sounds.__soundEffects[name].play()

    
    @staticmethod
    def playMusic(name : str, fileExt : str = ".wav") -> None:
        pygame.mixer.music.unload()
        pygame.mixer.music.load(Sounds.MUSIC_FOLDER + name + fileExt)
        pygame.mixer.music.play(-1)