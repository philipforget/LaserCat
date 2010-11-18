import pygame
from pygame.locals import *
import osc
import sys

class App():
    servos = (
        {
            'axis':   'y',
            'address': 0,
            'start':   -500,
            'end':     1300,
            'speed':   500,
            'direction': True,
        },{
            'address': 1,
            'start':   -500,
            'end':     1300,
            'speed':   500,
            'direction': False,
            },
        )
    board_address = '192.168.1.8'
    board_port    = 10000

    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((500, 500))
        pygame.time.set_timer(pygame.USEREVENT, 20)

        osc.init()
        bundle = osc.createBundle()
        osc.appendToBundle(bundle, "/digitalout/4/value",[1])
        for servo in self.servos:
            servo['range'] = self._range(servo)
            osc.appendToBundle(bundle, "/digitalout/%i/speed" % servo['address'], [servo['speed']])
        osc.sendBundle(bundle, self.board_address, self.board_port)

    @staticmethod
    def _range(servo):
        return lambda percent: int(servo['start'] - (servo['start'] - servo['end']) * percent)

    def run(self):
        try:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT:
                        x, y = pygame.mouse.get_pos()
                        px, py  = float(x) / self._screen.get_width(), float(y) / self._screen.get_height()
                        bundle = osc.createBundle()
                        for servo in self.servos:
                            osc.appendToBundle(bundle, "/servo/%i/position" % servo['address'], [servo['range'](1 - py if servo['direction'] else py)])
                        osc.sendBundle(bundle, self.board_address, self.board_port)
                        

        except(KeyboardInterrupt, SystemExit):
            print "\nShutting down, sending close signals"
            osc.sendMsg("/digitalout/4/value",[0], self.board_address, self.board_port)
            sys.exit()


if __name__ == '__main__':
    app = App()
    app.run()
