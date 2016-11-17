import logging
import socket
import subprocess
import sys

from thread import start_new_thread


class PtracksNet:

    LOG_FILE = "/tmp/ptracks-net.log"
    LOG_LEVEL = logging.DEBUG

    BUFFER_SIZE = 1024

    def __init__(self, listen_ip="0.0.0.0", port=5005):

        logging.basicConfig(filename=self.LOG_FILE, level=self.LOG_LEVEL, filemode='w',
                            format='%(asctime)s %(levelname)s: %(message)s')

        self.TCP_IP = listen_ip
        self.TCP_PORT = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.TCP_IP, self.TCP_PORT))
        self.s.listen(1)

    def start(self):

        logging.info("Starting ptracks-server on port %d" % self.TCP_PORT)

        while True:
            conn, addr = self.s.accept()
            print "New income connection: %s" % addr[0]
            logging.info("New income connection: %s" % addr[0])
            start_new_thread(self.client_thread, (conn, addr,))

    @staticmethod
    def client_thread(conn, addr):
        conn.send("Welcome to the ptracks-net server. Type commands and press enter to send.\r\n\r\n")
        conn.send("Available commands:\r\n")
        conn.send("  START <EXERCISE>\r\n")
        conn.send("  STOP\r\n")
        conn.send("  DISCONNECT\r\n")

        while True:
            conn.send("\r\n> ")
            data = conn.recv(1024)
            if not data:
                break

            logging.info("%s:%d - %s" % (addr[0], addr[1], data.strip()))

            if data.strip() == "DISCONNECT":
                conn.send("Bye!\r\n")
                break
            # Handles start exercise
            elif data.strip().startswith("START"):
                tokens = data.strip().split()

                if len(tokens) == 2:
                    output = subprocess.check_output(["service", "ptracks", "start", tokens[1]])
                    conn.send(output)
                else:
                    conn.send("Invalid input\r\n")

            # Handles stop (all exercises)
            elif data.strip() == "STOP":
                output = subprocess.check_output(["service", "ptracks", "stop"])
                conn.send(output)

            else:
                conn.send("Invalid command\r\n")

        conn.close()

if __name__ == "__main__":

    if len(sys.argv) > 1:
        server = PtracksNet(port=int(sys.argv[1]))
    else:
        server = PtracksNet()

    server.start()
