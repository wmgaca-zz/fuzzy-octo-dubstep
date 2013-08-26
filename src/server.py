#!/usr/bin/env python

import SocketServer
import pickle
import socket
import threading
from time import sleep
from lib import packages

from lib import HOST, PORT


class OctoServer(SocketServer.BaseRequestHandler):

    connections = {}

    def handle(self):
        print 'New connection.'

        self.user_name = None

        socket_ = self.request
        socket_.setblocking(0)

        while True:
            try:
                data = socket_.recv(1000000)
            except socket.error as e:
                continue

            if not data:
                continue

            package = packages.OctoPackage.deserialize(data)

            if isinstance(package, packages.HandShake):
                self.user_name = package.user_name

                # Add to connections
                OctoServer.connections[self.user_name] = socket_

            self.dispatch_package(package)

            if isinstance(package, packages.GoodBye):
                return
            #if not OctoServer.client_connected(client_id):
            #    return

    @staticmethod
    def client_connected(client_id):
        return client_id in OctoServer.connections

    @staticmethod
    def broadcast(package, except_=None):
        if isinstance(except_, basestring):
            except_ = (except_,)

        assert except_ is None or isinstance(except_, tuple)

        for user_name, connection in OctoServer.connections.items():
            if user_name in except_:
                print '(%s) Omit %s' % (id(package), user_name)
                continue
            try:
                print '(%s) Send to %s' % (id(package), user_name)
                connection.sendall(package.get_serialized())
            except socket.error:
                print 'Cannot send package %s to %s' % (package, user_name)

    def dispatch_package(self, package):
        assert isinstance(package, packages.OctoPackage)

        if isinstance(package, packages.HandShake):
            OctoServer.broadcast(package.to_user_new(),
                                 except_=self.user_name)
        elif isinstance(package, packages.UserMessage):
            OctoServer.broadcast(package.to_message(),
                                 except_=self.user_name)


def print_user_info():
    while True:
        sleep(2)
        print 'Connected users: %s' % len(OctoServer.connections)


def main():
    server = SocketServer.ThreadingTCPServer((HOST, PORT), OctoServer)

    user_info_thread = threading.Thread(target=print_user_info)
    user_info_thread.start()

    print 'Running server on %s:%s' % (HOST, PORT)
    server.serve_forever()

    user_info_thread.join()


if __name__ == '__main__':
    main()
