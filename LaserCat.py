import osc
import sys

from bottle import route, run, request, post, static_file

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
        """
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
        osc.sendBundle(bundle, BOARD_ADDRESS, BOARD_PORT)
        """
        pass

    @staticmethod
    def _range(servo):
        return lambda percent: int(servo['start'] - (servo['start'] - servo['end']) * percent)

    def update_servos(self, x, y):
        """
        #x, y = pygame.mouse.get_pos()
        bundle = osc.createBundle()
        for servo in servos:
            p = x if servo['axis'] == 'x' else y
            osc.appendToBundle(
                bundle,
                "/servo/%i/position" % servo['address'],
                [servo['range'](1 - p if servo['direction'] else p)]
            )
        osc.sendBundle(bundle, BOARD_ADDRESS, BOARD_PORT)
        """
        return {
            'x': x,
            'y': y,
        }

    def shutdown(self):
        print "\nShutting down, sending close signals"
        osc.sendMsg("/digitalout/%i/value" % laser_address, [0], BOARD_ADDRESS, BOARD_PORT)
        sys.exit()


osc_app = OSCApp()

@route('/')
def index():
    return static_file('index.html', './static/')

@post('/ajax/update/')
def ajax_update():
    x, y = request.forms.get('x'), request.forms.get('y')
    try:
        x = float(x)
        y = float(y)
        return osc_app.update_servos(x, y)

    except:
        return { 'success': False }

@route('/static/:filename')
def static(filename):
    return static_file(filename, './static/')

run()
