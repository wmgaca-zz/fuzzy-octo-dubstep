#!/usr/bin/env python

import socket
import sys
from Tkinter import Tk, W, E, S, N, BOTH, Text, Listbox, END, Scrollbar
from ttk import Frame, Entry, Style, Label, Button

from lib import HOST, PORT
from lib import packages
from lib import net


class MainFrame(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.init()

    def init(self):
        self.parent.title('FuzzyOctoDubstep')

        self.style = Style()
        self.style.theme_use('default')
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        lbl = Label(self, text="Windows")
        lbl.grid(sticky=W, pady=4, padx=5)

        conv_scrollbar = Scrollbar(self)
        conv_scrollbar.grid(row=1, column=2)


        conv = Listbox(self, width=80, height=30, yscrollcommand=conv_scrollbar.set)
        conv.grid(row=1, column=0, columnspan=2, rowspan=4,
            padx=5, sticky=E+W+S+N)
        conv.insert(END, 'Hello')

        conv_scrollbar.config(command=conv.yview)

        abtn = Button(self, text="Activate")
        abtn.grid(row=1, column=3)

        cbtn = Button(self, text="Close")
        cbtn.grid(row=2, column=3, pady=4)

        hbtn = Button(self, text="Help")
        hbtn.grid(row=5, column=0, padx=5)

        obtn = Button(self, text="OK")
        obtn.grid(row=5, column=3)

    def _append(self):
            text = self.user_input.get()
            self.user_input.delete(0, END)

            user_name = 'Gac'
            self.conv.insert(END, "%s: %s" % (user_name, text[:self.CONV_W]))

            while True:
                text = text[self.CONV_W:]
                if not text:
                    break
                self.conv.insert(END, "%s" % (text[:self.CONV_W]))

            self.conv.yview_moveto(1.0)

# class FuzzyOctoClient(object):
#
#     CONV_W = 0
#     CONV_H = 0
#
#     def __init__(self, master):
#
#         master_frame = Frame(master, width=640, height=880)
#         master_frame.pack(fill=BOTH)
#
#         # Conversation
#
#         conv_frame = Frame(master=master_frame)
#         conv_frame.pack(side=LEFT, fill=X)
#
#         self.conv_scrollbar = Scrollbar(master=conv_frame)
#         self.conv_scrollbar.pack(side=RIGHT, fill=BOTH)
#
#         self.conv = Listbox(master=conv_frame,
#                             width=self.CONV_W,
#                             height=self.CONV_H,
#                             yscrollcommand=self.conv_scrollbar.set)
#         self.conv.pack(side=LEFT, fill=X)
#
#         self.conv_scrollbar.config(command=self.conv.yview)
#
#         # User input
#
#         self.user_input = Entry(master=conv_frame, width=self.CONV_W - 8)
#         self.user_input.pack(side=BOTTOM)
#
#         self.append_button = Button(
#             master=conv_frame,
#             text='send',
#             fg='red',
#             command=self._append)
#         self.append_button.pack(side=BOTTOM)
#
#         # User list
#         users_frame = Frame(master=master_frame)
#         users_frame.pack(side=RIGHT)
#
#
#
#     def _append(self):
#         text = self.user_input.get()
#         self.user_input.delete(0, END)
#
#         user_name = 'Gac'
#         self.conv.insert(END, "%s: %s" % (user_name, text[:self.CONV_W]))
#
#         while True:
#             text = text[self.CONV_W:]
#             if not text:
#                 break
#             self.conv.insert(END, "%s" % (text[:self.CONV_W]))
#
#         self.conv.yview_moveto(1.0)


def package_dispatcher(package):
    if isinstance(package, packages.Message):
        print '%s: %s' % (package.user_name, package.message)
    else:
        print 'Unknown package type: %s' % package.__class__.__name__


def main():
    root = Tk()
    MainFrame(root)
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
