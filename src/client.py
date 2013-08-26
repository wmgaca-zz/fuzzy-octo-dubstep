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

    socket_handler = net.SocketHandler(HOST, PORT, package_dispatcher)
    socket_handler.send(packages.HandShake())

    while True:
        user_input = raw_data()
        print 'Got input: %s -- sending!' % user_input
        socket_handler.send(packages.UserMessage(user_name='Foo',
                                                 message=user_input))


if __name__ == '__main__':
    main()
