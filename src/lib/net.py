import socket
import pickle
import threading
import time
from lib import packages

class SocketHandler(object):

    _listen = True

    def __init__(self, host, port, handler):
        # Create socket
        print 'Opening socket...'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server
        print 'Trying to connect...'
        self.socket.connect((host, port))
        print 'Connected!'

        # Make the socket non-blocking
        self.socket.setblocking(0)

        # Create listening thread
        self.listening_thread = threading.Thread(target=SocketHandler.listen,
                                                 args=(self.socket, handler))
        # Start the thread
        self.listening_thread.start()

    def __del__(self):
        self.close()

    def send(self, package):
        assert isinstance(package, packages.OctoPackage)

        if self.socket:
            try:
                self.socket.sendall(package.get_serialized())
            except socket.error as exc:
                print 'Cannot send package: %s (%s)' % (package, exc)

    def close(self):
        SocketHandler._listen = False
        self.listening_thread.join()

        if self.socket:
            self.socket.close()

    @staticmethod
    def listen(socket_, handler):
        """Listen on given socket to intercept server's packages.

        Args:
            socket: Socket instance to listen on
            handler: Function called to handle received data
        """

        while SocketHandler._listen:
            try:
                data = socket_.recv(100000)
            except socket.error as e:
                time.sleep(0.1)
                continue
            try:
                package = pickle.loads(data)
            except EOFError:
                continue
            if not package:
                continue

            print 'Received! Handling!'
            handler(package)

