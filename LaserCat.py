import pygame
from pygame.locals import *
import osc
import sys

CLOCKWISE         = True
COUNTER_CLOCKWISE = False

board_address     = '192.168.1.8'
board_port        = 10000
laser_address     = 4
servos = ({
    'axis':   'y',
    'address': 0,
    'start':   -500,
    'end':     1300,
    'speed':   500,
    'direction': CLOCKWISE,
    },{
    'axis':   'x',
    'address': 1,
    'start':   -500,
    'end':     1300,
    'speed':   500,
    'direction': COUNTER_CLOCKWISE,
})

class App():

    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((500, 500))
        pygame.time.set_timer(pygame.USEREVENT, 20)

        osc.init()
        bundle = osc.createBundle()
        osc.appendToBundle(bundle, "/digitalout/%i/value" % laser_address,[1])
        for servo in servos:
            servo['range'] = self._range(servo)
            osc.appendToBundle(
                bundle,
                "/digitalout/%i/speed" % servo['address'],
                [servo['speed']]
            )
        osc.sendBundle(bundle, board_address, board_port)

    @staticmethod
    def _range(servo):
        return lambda percent: int(servo['start'] - (servo['start'] - servo['end']) * percent)

    def run(self):
        try:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT:
                        self.update_servos()

        except(KeyboardInterrupt, SystemExit):
            print "\nShutting down, sending close signals"
            osc.sendMsg("/digitalout/%i/value" % laser_address, [0], board_address, board_port)
            sys.exit()

    def update_servos(self):
        x, y = pygame.mouse.get_pos()
        px, py  = float(x) / self._screen.get_width(), float(y) / self._screen.get_height()
        bundle = osc.createBundle()
        for servo in servos:
            p = px if servo['axis'] == 'x' else py
            osc.appendToBundle(
                bundle,
                "/servo/%i/position" % servo['address'],
                [servo['range'](1 - p if servo['direction'] else p)]
            )
        osc.sendBundle(bundle, board_address, board_port)


if __name__ == '__main__':
    app = App()
    app.run()
