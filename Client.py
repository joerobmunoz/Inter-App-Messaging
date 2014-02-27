__author__ = 'Joe Munoz'
#!/usr/bin/env python


"""
Client implementation of a client/server inter-application messaging system. This
consists of the main pushing client and an additional open socket to receive pushes
from the server.
"""

import Database
import socket
import sys
import getopt
import datetime
import time
import thread

# Constants
port = 54307
size = 1024
host = 'localhost'

class Client():
    def __init__(self):
        self.address = (host, port)
        self.soc = None

# Database doesn't do anything yet.
    def set_up_database(self):
        db = Database.Deployment()
        db.deploy()

# Kicks off the listener and the initial socket connection
    def establish_socket_connection(self):
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            connected = False
            while connected == False:
                self.soc.connect(self.address)
                self.listener = thread.start_new_thread(self.listen, ())

                connected = True
                self.send_data()
        except socket.error, (value, message):
            if self.soc:
                self.soc.close()
                print "Socket error: " + message
                self.reconnect()

# Reconnect method can be changed to include fixed polling and writing failed messages
# to the DB.
    def reconnect(self):
        connected = False
        try:
            while connected == False:
                if self.soc:
                    self.soc.connect(self.address)
                    conntected = True
        except socket.error as e:
            print "Socket error: " + e.message
            time.sleep(1)

    def listen(self):
        while self.soc:
            msg = self.soc.recv(size)
            print "Received (" + str(datetime.datetime.now()) + "): " + msg + "%"

    def send_data(self):
        sys.stdout.write('%')
        while 1:

            data_to_send = sys.stdin.readline()

            try:
                bytes_sent = self.soc.send(data_to_send)
                if bytes_sent == 0:
                    self.establish_socket_connection()
                else:
                    sys.stdout.write('%')
            except socket.error, (value, message):
                print "Could not send data over socket: " + message + "\n Attempting to reconnect..."
                self.establish_socket_connection()

# Command line args to set the host and port
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["host","port"])
    except getopt.GetoptError:
        print "Client.py -h <host> -p <post>\nDefaults to 'localhost' and '54322'"
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-l':
            print "Client.py -h <host> -p <post>\nDefaults to " + str(host) + " and " + str(port)
            sys.exit()
        elif opt in ("-h", "--host"):
            host = arg
        elif opt in ("-p", "--post"):
            port = arg

    # Set up the client
    cli = Client()
    cli.set_up_database()
    cli.establish_socket_connection()

if __name__ == "__main__":
    main(sys.argv[1:])
