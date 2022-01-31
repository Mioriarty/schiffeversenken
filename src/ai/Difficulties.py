# Name              Fehlerwkt.     Beschreibung  
# Käpt'n Blaubär    0.8            Erzählt nur Seemannsgarn und hat folglich auch hier wohl Blaubeeren auf den Augen.
# Caipten Hook      0.5            Sein Haken behindert ihm beim Zielen. Trotzdem ist er stets bemüht.
# Die Wilde 13      0.2            Alleine alaphabet. Als Team könnnen sie locker eine ganze Flotte besiegen.
# Jack Sparrow      0.0            Unberechenbar und heimtückisch. Lässt jeden über die Planke gehen. Vorsicht!


class Difficulties:

    __nameImages = [ 'texts.kaptnBlaubar', 'texts.captainHook', 'texts.dieWilde13', 'texts.jackSparrow' ]
    __descriptionImages = [ 'texts.kb_des', 'texts.ch_des', 'texts.w13_des', 'texts.js_des' ]
    __chancesOfMistake = [ 0.8, 0.5, 0.2, 0.0 ]
    __selectedIndex = 0


    @staticmethod
    def allNameImages() -> list[str]:
        return Difficulties.__nameImages
    
    @staticmethod
    def allDescriptionIamges() -> list[str]:
        return Difficulties.__descriptionImages
    


    @staticmethod
    def setSelectedIndex(index : int) -> None:
        Difficulties.__selectedIndex = index

    
    @staticmethod
    def getSelectedNameImage() -> str:
        return Difficulties.__nameImages[Difficulties.__selectedIndex]
    

    @staticmethod
    def getSelectedChanceOfMistake() -> float:
        return Difficulties.__chancesOfMistake[Difficulties.__selectedIndex]