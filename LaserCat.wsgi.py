import sys
sys.path.append("/home/philipforget/workspace/LaserCat")

import bottle
import OSCApp
bottle.debug(True)

STATIC_DIR  = '/home/philipforget/workspace/LaserCat/static/'
osc_app = OSCApp.OSCApp()

@bottle.route('/')
def index():
    return bottle.static_file('index.html', STATIC_DIR)

@bottle.post('/ajax/update/')
def ajax_update():
    x, y = bottle.request.forms.get('x'), bottle.request.forms.get('y')
    try:
        x = float(x)
        y = float(y)
        return osc_app.update_servos(x, y)

    except:
        return { 'success': False }

@bottle.route('/static/:filename')
def static(filename):
    return bottle.static_file(filename, STATIC_DIR)

@bottle.post('/toggle/')
@bottle.route('/toggle/')
def toggle():
    return {
        'state': osc_app.toggle_laser()
    }

@bottle.route('/shutdown/')
@bottle.post('/shutdown/')
def shutdown():
    return {
        'state': osc_app.set_laser(False)
    }

@bottle.route('/laser/')
@bottle.post('/laser/')
def shutdown():
    return {
        'state': osc_app.laser_state
    }

application = bottle.default_app()
