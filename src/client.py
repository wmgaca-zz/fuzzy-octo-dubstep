#!/usr/bin/env python

import socket
import sys

from lib import HOST, PORT
from lib import packages
from lib import net


def package_dispatcher(package):
    if isinstance(package, packages.Message):
        print '%s: %s' % (package.user_name, package.message)
    else:
        print 'Unknown package type: %s' % package.__class__.__name__


def main():
    try:
        socket_handler = net.SocketHandler(HOST, PORT, package_dispatcher)
    except socket.error as exc:
        print 'Cannot connect: %s' % exc

    user_name = raw_input('User name: ')

    socket_handler.send(packages.HandShake(user_name=user_name))

    while True:
        user_input = raw_input()
        print 'Got input: %s -- sending!' % user_input
        socket_handler.send(packages.UserMessage(user_name=user_name,
                                                 message=user_input))


if __name__ == '__main__':
    main()
