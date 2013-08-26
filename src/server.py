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

        client_id = id(self)

        socket_ = self.request
        socket_.setblocking(0)

        # Add socket to connection list
        OctoServer.connections[client_id] = socket_

        while True:
            try:
                data = socket._recv(1000000)
            except socket.error as e:
                continue

            if not data:
                continue

            package = packages.OctoPackage.deserialize(data)
            OctoServer.dispatch_package(package, client_id)

            if isinstance(package, packages.GoodBye):
                return
            if not OctoServer.client_connected(client_id):
                return

    @staticmethod
    def client_connected(client_id):
        return client_id in OctoServer.connections

    @staticmethod
    def broadcast(package):
        for client_address, connection in OctoServer.connections.items():
            try:
                connection.sendall(package.get_serialized())
            except socket.error:
                print 'Cannot send package %s to %s' % (package, client_addr)
                OctoServer.remove_client(client_addr)

    @staticmethod
    def dispatch_package(package, client_id):
        assert isinstance(package, packages.OctoPackage)

        if isinstance(package, packages.HandShake):
            OctoServer.broadcast(packages.UserNew(user_name=client_id))
        elif isinstance(package, packages.UserMessage):
            OctoServer.broadcast(package.to_message())


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
