import serial
import tornado.ioloop
import tornado.web

SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_BAUD = 19200

serial = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1)

class OnHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Lights On!")
        serial.write('light on')

class OffHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Lights Off!")
        serial.write('light on')

application = tornado.web.Application([
    (r"/on", OnHandler),
    (r"/off", OffHandler),
])


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
