

import utils


class Module:
    def __init__(self, engine):
        self.engine = engine

        self.data = {}

    def open(self, fileName):
        import os
        modPath = os.path.dirname(os.path.realpath(__file__))
        self.data = utils.loadJson(os.path.join(modPath, fileName))
        self.engine.pattern.load(self.data['pattern'])

    def save(self, fileName):
        self.data['pattern'] = self.engine.pattern.getData()
        utils.saveJson(self.data, fileName)

    def update(self):
        pass

    def checkEvent(self, event):
        if event[0] == 'btn_pressed':
            btnName = event[1]
            if btnName == 'project':
                self.save('project.json')