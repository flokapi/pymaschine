

from modules import search_sound
from modules import pad_layout
from modules import pattern
from modules import project





class Engine:
    def __init__(self):
        self.project = project.Module(self)
        self.searchSound = search_sound.Module(self)
        self.pattern = pattern.Module(self)
        self.padLayout = pad_layout.Module(self)

        self.modules = [
            self.project,
            self.searchSound,
            self.pattern,
            self.padLayout
        ]

    def update(self):
        for module in self.modules:
            module.update()

    def processEvent(self, event):
        for module in self.modules:
            if module.checkEvent(event):
                return



def processEvent(event):
    engine.processEvent(event)

def update():
    engine.update()


engine = Engine()
engine.project.open('project.json')