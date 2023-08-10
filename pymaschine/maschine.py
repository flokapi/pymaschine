


import pymikro


import threading
import random
import time



class ButtonsModel:
    def __init__(self):
        self.pressedBtns = []

    def getEvent(self, cmd):
        if cmd['cmd'] == 'btn':
            btnOld = self.pressedBtns
            btnNew = cmd['btn_pressed']
            self.pressedBtns = btnNew

            diff = set(btnOld) ^ set(btnNew)
            for diffBtn in diff:
                if diffBtn in btnNew:
                    return ['btn_pressed', diffBtn]
                else:
                    return ['btn_relased', diffBtn]

        return None



class EncoderModel:
    def __init__(self):
        pass

    def getEvent(self, cmd):
        if cmd['cmd'] == 'btn':
            encMove = cmd['encoder_move'] 
            if encMove != 0:
                return ['encoder_move', encMove]

        return None



class PadsModel:
    def __init__(self):
        self.nbPads = 16
        self.treshold = 5
        self.pads = {}
        for i in range(self.nbPads):
            self.pads[i] = {'pressed': False, 'buf': []}

    def padReleased(self, padNb):
        self.pads[padNb]['buf'] = []
        self.pads[padNb]['pressed'] = False

    def padPressed(self, padNb):
        self.pads[padNb]['buf'] = []
        self.pads[padNb]['pressed'] = True

    def getEvent(self, cmd):
        if cmd['cmd'] == 'pad':
            padNb = cmd['pad_nb']
            padVal = cmd['pad_val']
            buf = self.pads[padNb]['buf']

            if cmd['pressed'] == True:
                self.padPressed(padNb)
                return ['pad_pressed', padNb, padVal]

            if cmd['released'] == True:
                self.padReleased(padNb)
                return ['pad_released', padNb]

            if cmd['touched'] == True:
                if padVal == 0:
                    self.padReleased(padNb)
                if self.pads[padNb]['pressed'] == False:
                    if padVal > self.treshold:
                        buf.append(padVal)
                if len(buf) == 5:
                    self.padPressed(padNb)
                    return ['pad_pressed', padNb, max(buf)]

        return None




# --------------------- leds and screen init

def launch(fname):
    threading.Thread(target=fname).start()


def padLedAnimation():
    while True:
        for padNb in range(16):
            colorNb = int(random.random()*16)+1
            color = device.settings['color'][colorNb]
            brightness = 1 #int(random.random()*3)+1
            device.setLight('pad', padNb, brightness, color)
        device.updLights()
        time.sleep(60)


def initButtonLeds():
    activeButtons = [
        'play',
        'stop',
        'erase',
        'rec',
        'star',
        'project',
        'search'
    ]
    for btnName in activeButtons:
        device.setLight('button', btnName, 1)
    device.updLights()


def init():
    device.setScreen('PyMaschine', size=20)
    launch(padLedAnimation)
    initButtonLeds()


# --------------------- pad light reaction

def blinkPad(padNb):
    def blink(padNb):
        padLights = device.getLights()['pad']
        if padNb in padLights.keys():
            color = padLights[padNb]['color']
            val = padLights[padNb]['val']

        device.setLight('pad', padNb, 2, color)
        time.sleep(0.05)
        device.setLight('pad', padNb, 1, color)

    threading.Thread(target=blink, args=[padNb]).start()


# --------------------- button light control

def setBtnLight(btnName, bright=True):
    brightness = 3 if bright else 1
    device.setLight('button', btnName, brightness)


# --------------------- event processing


def update():
    device.updLights()


def getEvent():
    cmd = device.readCmd()

    if cmd:
        for iface in [btnMdl, encMdl, padMdl]:
            event = iface.getEvent(cmd)
            if event:
                return event

    return None


device = pymikro.MaschineMikroMk3()
device.showConnInfo()

btnMdl = ButtonsModel()
encMdl = EncoderModel()
padMdl = PadsModel()

