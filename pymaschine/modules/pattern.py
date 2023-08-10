


import easymix as mixer
import maschine

import time


class Pattern:
    def __init__(self, engine):
        self.engine = engine

        self.data = {}
        self.state = 'stop'

    def load(self, data):
        self.data = {}
        for timeStamp in sorted(data.keys()):
            self.data[int(timeStamp)] = data[timeStamp]

    def playSound(self, padNb):
        sound = self.engine.padLayout.getSound(padNb)
        if sound:
            maschine.blinkPad(padNb)
            mixer.play(sound)

    def insert(self, padNb):
        self.playSound(padNb)
        if self.state == 'rec':
            timeDiff = time.time() - self.timeStart
            timeStamp = int(timeDiff*10**6)
            self.data[timeStamp] = padNb

    def clrPlayer(self):
        self.timeStart = time.time()
        self.timeStamps = sorted(self.data.keys())

    def stop(self):
        mixer.stop()
        self.state = 'stop'

    def record(self):
        mixer.stop()
        self.state = 'rec'
        self.clrPlayer()

    def play(self):
        mixer.stop()
        self.state = 'play'
        self.clrPlayer()

    def update(self):
        if self.state not in ['play', 'rec']:
            return

        if len(self.timeStamps) == 0:
            if self.state in ['play']:
                self.clrPlayer()
            return

        timeDiff = time.time() - self.timeStart

        if timeDiff * 10**6 > int(self.timeStamps[0]):
            padNb = self.data[self.timeStamps[0]]
            self.playSound(padNb)
            self.timeStamps.pop(0)

    def clear(self):
        self.data = {}
        self.timeStamps = []
        self.stop()

    def get(self):
        return self.data

    def toSec(self, timeStamp):
        return timeStamp / 10**6

    def export(self, fileName):
        track = mixer.Track()
        for timeStamp in sorted(self.data.keys()):
            padNb = self.data[timeStamp]
            sound = self.engine.padLayout.getSound(padNb)
            if sound:
                track.addSound(sound, self.toSec(timeStamp))

        track.save(fileName)


class Module:
    def __init__(self, engine):
        self.pattern = Pattern(engine)

    def load(self, data):
        self.pattern.load(data)

    def getData(self):
        return self.pattern.data

    def update(self):
        self.pattern.update()

        state = self.pattern.state
        for btn in ['rec', 'stop', 'play']:
            maschine.setBtnLight(btn, state == btn)

    def checkEvent(self, event):
        if event[0] == 'pad_pressed':
            padNb = event[1]
            self.pattern.insert(padNb)

        if event[0] == 'btn_pressed':
            btnName = event[1]
            if btnName == 'stop':
                self.pattern.stop()
            if btnName == 'play':
                self.pattern.play()
            if btnName == 'erase':
                self.pattern.clear()
            if btnName == 'rec':
                self.pattern.record()
            if btnName == 'star':
                self.pattern.export('export.mp3')