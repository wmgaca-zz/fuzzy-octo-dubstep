#!/usr/bin/env python

import socket
import sys
from Tkinter import *

from lib import HOST, PORT
from lib import packages
from lib import net


class FuzzyOctoClient(object):

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.conversation_body = StringVar(value='')
        self.users_body = StringVar(value='')

        self.conversation = Message(master=frame,
                                    textvariable=self.conversation_body,
                                    width=80)
        self.conversation.pack(side=LEFT)

        self.users = Message(master=frame,
                             textvariable=self.users_body,
                             width=20)
        self.users.pack(side=LEFT)

        self.quit_button = Button(
            master=frame,
            text='QUIT',
            fg='red',
            command=frame.quit)
        self.quit_button.pack(side=LEFT)

        self.quit_button = Button(
            master=frame,
            text='APPEND',
            fg='red',
            command=self._append)
        self.quit_button.pack(side=LEFT)

    def _append(self):
        self.conversation_body.set(self.conversation_body.get() + '\nHello World')

def package_dispatcher(package):
    if isinstance(package, packages.Message):
        print '%s: %s' % (package.user_name, package.message)
    else:
        print 'Unknown package type: %s' % package.__class__.__name__


def main():
    root = Tk()

    FuzzyOctoClient(root)
    root.mainloop()
    root.destroy()

    return

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
