



class Module:
    def __init__(self, engine):
        self.engine = engine

    def getSound(self, padNb, path=True):
        pads = self.engine.project.data['pads']
        soundsLoc = self.engine.project.data['sound_path']
        if str(padNb) in pads.keys():
            sound = pads[str(padNb)]
            if path:
                return soundsLoc + sound
            else:
                return sound
        else:
            return None

    def setSound(self, padNb, soundName):
        self.engine.project.data['pads'][str(padNb)] = soundName

    def update(self):
        pass

    def checkEvent(self, event):
        return None