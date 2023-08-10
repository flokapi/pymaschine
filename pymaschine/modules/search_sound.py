


import easymix as mixer
import maschine
import utils
import os



class Module:
    def __init__(self, engine):
        self.engine = engine

        self.active = False
        self.state = None

        self.availSounds = []
        self.selSound = None
        self.padNb = None

    def showSelSound(self):
        msg = f'pad {self.padNb+1}\n{self.selSound}'
        maschine.device.setScreen(msg)

    def playSelSound(self):
        mixer.stop()
        mixer.play(self.sndPath + self.selSound)

    def update(self):
        pass

    def checkEvent(self, event):
        if event[0] == 'btn_pressed':
            if event[1] == 'search':
                self.active = not self.active
                maschine.setBtnLight('search', bright=self.active)
                return True

        if self.active:
            if event[0] == 'pad_pressed':
                self.sndPath = self.engine.project.data['sound_path']
                self.availSounds = sorted(os.listdir(self.sndPath))

                self.padNb = event[1]
                self.state = 'searching'
                self.selSound = self.engine.padLayout.getSound(self.padNb, path=False)
                self.showSelSound()
                return True

            if event[0] == 'encoder_move':
                move = event[1]
                if self.selSound == None:
                    currIndex = -1
                else:
                    currIndex = self.availSounds.index(self.selSound)
                nextIndex = currIndex + move
                if nextIndex >= 0 and nextIndex < len(self.availSounds):
                    self.selSound = self.availSounds[nextIndex]
                    self.showSelSound()
                    self.playSelSound()
                return True

            if event[0] == 'btn_pressed':
                if event[1] == 'enter':
                    self.engine.padLayout.setSound(self.padNb, self.selSound)
                return True

        return None