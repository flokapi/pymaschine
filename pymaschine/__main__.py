


import maschine
import engine
import ui




def launch():
    maschine.init()

    while True:
        event = maschine.getEvent()
        if event:
            engine.processEvent(event)

        engine.update()
        maschine.update()
        ui.update()



if __name__ == '__main__':
    launch()