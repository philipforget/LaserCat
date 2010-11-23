import sys
import osc

CLOCKWISE         = True
COUNTER_CLOCKWISE = False
BOARD_ADDRESS     = '192.168.1.8'
BOARD_PORT        = 10000

laser_address     = 0
servos = ({
    'axis':   'y',
    'address': 0,
    'start':   -200,
    'end':     800,
    'speed':   200,
    'direction': COUNTER_CLOCKWISE,
    },{
    'axis':   'x',
    'address': 1,
    'start':   -500,
    'end':     1200,
    'speed':   200,
    'direction': CLOCKWISE,
})

class OSCApp():
    def __init__(self):
        osc.init()
        bundle = osc.createBundle()
        self.set_laser(False)
        for servo in servos:
            servo['range'] = self._range(servo)
            osc.appendToBundle(
                bundle,
                "/digitalout/%i/speed" % servo['address'],
                [servo['speed']]
            )
        osc.sendBundle(bundle, BOARD_ADDRESS, BOARD_PORT)

    @staticmethod
    def _range(servo):
        return lambda percent: int(servo['start'] - (servo['start'] - servo['end']) * percent)

    def update_servos(self, x, y):
        bundle = osc.createBundle()
        for servo in servos:
            p = x if servo['axis'] == 'x' else y
            osc.appendToBundle(
                bundle,
                "/servo/%i/position" % servo['address'],
                [servo['range'](1 - p if servo['direction'] else p)]
            )
        osc.sendBundle(bundle, BOARD_ADDRESS, BOARD_PORT)

        return {
            'x': x,
            'y': y,
        }

    def toggle_laser(self):
        return self.set_laser(not self.laser_state)

    def set_laser(self, state):
        self.laser_state = state
        int_state = 1 if self.laser_state else 0
        osc.sendMsg("/digitalout/%i/value" % laser_address, [int_state], BOARD_ADDRESS, BOARD_PORT)
        return self.laser_state
