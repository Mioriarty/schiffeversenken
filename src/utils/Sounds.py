import os
import pygame

class Sounds:
    """
    Static class that handles all the sound resources.
    """

    SOUND_EFFECT_FOLDER = "../../res/music/sounds/"
    MUSIC_FOLDER = "../../res/music/music/"
    EXTENTIONS = [ ".wav" ]

    __soundEffects : dict[str, pygame.mixer.Sound] = {}

    __musicOn  = True
    __soundsOn = True

    @staticmethod
    def loadAll() -> None:
        """
        Loads all sound effect resources.
        
        They sould all be in the same folder: SOUND_EFFECT_FOLDER.

        No folder hierarchy is allowed.
        """
        path = os.path.join(os.path.dirname(__file__), Sounds.SOUND_EFFECT_FOLDER)
        for root, _, files in os.walk(path):
            for file in files:
                [ filename, extention ] = os.path.splitext(file)
                if extention in Sounds.EXTENTIONS:
                    key = filename
                    Sounds.__soundEffects[key] = pygame.mixer.Sound(os.path.join(root, file))
                    
    
    @staticmethod
    def playSoundEffect(name : str) -> None:
        """
        Plays a sound affect given its name.

        The name is the file's name without its file extention.

        Args:
            name (str): The name of the sound to be played.
        """
        if Sounds.__soundsOn:
            Sounds.__soundEffects[name].play()

    
    @staticmethod
    def playMusic(name : str, fileExt : str = ".wav") -> None:
        """
        Plays a music inside the MUSIC_FOLDER.

        The name is the file's name without its file extention.

        Args:
            name (str): The name of the file.
            fileExt (str, optional): The file extention. Defaults to ".wav".
        """
        path = os.path.join(os.path.dirname(__file__), Sounds.MUSIC_FOLDER)
        
        pygame.mixer.music.unload()
        pygame.mixer.music.load(path + name + fileExt)
        pygame.mixer.music.play(-1)
    
    @staticmethod
    def stopMusic() -> None:
        """
        Stops any music playing.

        Sound effects will continue.
        """
        pygame.mixer.music.stop()
    
    @staticmethod
    def stopAllSoundEffects() -> None:
        """
        Stops all sound effects.

        Music will continue.
        """
        pygame.mixer.stop()
    
    # MUTE CONTROL

    @staticmethod
    def isMusicOn() -> bool:
        """
        Returns whether the music is currently turned on.

        Returns:
            bool: If the music is currently turned on.
        """
        return Sounds.__musicOn
    
    @staticmethod
    def areSoundsOn() -> bool:
        """
        Returnw whether sound effects are currently turned on.

        Returns:
            bool: If sound effects are currently turned on.
        """
        return Sounds.__soundsOn
    
    @staticmethod
    def setMusicOn(value : bool) -> None:
        """
        Sets whether the music is turned on.

        Args:
            value (bool): If the music should be turned on.
        """
        Sounds.__musicOn = value
        pygame.mixer.music.set_volume(1 if value else 0)
    
    @staticmethod
    def setSoundsOn(value : bool) -> None:
        """
        Sets whether the sound effects are turned on.

        Args:
            value (bool): If the sound effects should be turned on.
        """
        Sounds.__soundsOn = value

        if not value:
            Sounds.stopAllSoundEffects()
