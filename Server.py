__author__ = 'Joe Munoz'
#!/usr/bin/env python


"""
Server implementation of a client/server inter-application messaging system. This is comprised
of the main server, and alternate thread workers that push updates to existing socket
connections.
"""


import Database
import socket
import sys
import getopt
import thread
import time
import select

# Constants
size = 1024
backlog = 10
host = 'localhost'
port = 54307

# Main server class. Just call #start() and it deploys the DB and socket listener
class Server:
    def __init__(self):
        self.address = (host, port)
        self.clients = dict()

    def start(self):
        db = Database.Deployment()
        db.deploy()

        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind(self.address)
        self.soc.listen(backlog)

        self.acceptor = thread.start_new_thread(self.accept, ())

        # Kick off separate listener thread

        # TODO BUG
        # This thread needs to take a back seat, but this is not the right way.
        time.sleep(500000)


    def stop(self):
        self.soc = None

    def accept(self):
        try:
            input = [self.soc, sys.stdin]
            while self.soc:
                inputready, outputready, exceptready = select.select(input, [], [])
                for s in inputready:
                    if s == self.soc:
                        # handle the server socket
                        connection, name = self.soc.accept()
                        print str(name[0]) + ":" + str(name[1]) + "@ has connected"

                        cli = Client(conn=connection, cl=name)
                        self.clients[name] = cli
                        cli.spoke = self.tell

        except socket.error as e:
            print "Error accepting socket connection\n:" + e.message
            self.soc.close()

    def tell(self, ip, msg):
        print str(ip[0]) + ":" + str(ip[1]) + "@ " + msg
        for id in self.clients:
            self.clients[id].hear(msg)

# Server implementation of the Client Object.
class Client:
    def __init__(self, conn, cl):
        self.soc = conn
        self.ip = cl
        self.cliname = cl
        self.spoke = None
        self.speaker = thread.start_new_thread(self.speak, ())

    def speak(self):
        while self.soc:
            msg = self.soc.recv(size)
            if msg:
                self.spoke(self.cliname, msg)

    def hear(self, msg):
        self.soc.send(msg)

# Command line args to set the host and port
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["host", "port"])
    except getopt.GetoptError:
        print "Client.py -h <host> -p <post>\nDefaults to 'localhost' and '54322'"
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-l':
            print "Client.py -h <host> -p <post>\nDefaults to " + str(host[0]) + " and " + str(port)
            sys.exit()
        elif opt in ("-h", "--host"):
            host = arg
        elif opt in ("-p", "--post"):
            port = arg

    Server().start()

if __name__ == "__main__":
   main(sys.argv[1:])