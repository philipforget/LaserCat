#!/usr/bin/env python

import optparse
import sys
import osc
import curses

# Configure your shell here
BOARD_ADDRESS = '192.168.1.8'
BOARD_PORT    = 10000


class App():
    def __init__(self):
        osc.init()

    def run(self):
        while True:
            uin = raw_input("> ").strip()
            if not uin:
                pass
            else:
                parts = uin.split(' ')
                message = parts[0]
                value = int(parts[1]) if len(parts) > 1 else ""
                osc.sendMsg(message, [value], BOARD_ADDRESS, BOARD_PORT)


if __name__ == '__main__':
    p = optparse.OptionParser()
    p.add_option('--board-address', '-a', dest='board_address')
    p.add_option('--board-port', '-p', dest='board_port')
    options, arguments = p.parse_args()
    BOARD_ADDRESS = options.board_address if options.board_address else BOARD_ADDRESS
    BOARD_PORT = options.board_port if options.board_port else BOARD_PORT

    app = App()
    app.run()
