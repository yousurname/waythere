# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

import logging
from bluetooth import *

logging.basicConfig(filename='/home/pi/Desktop/rfcomm_log.log',level=logging.DEBUG)

logging.info("rfcommserver_startup begin")

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",22))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
logging.debug("Waiting for connection on RFCOMM channel " + str(port))

client_sock, client_info = server_sock.accept()
logging.debug("Accepted connection from " + str(client_info))

try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        logging.info("received " + str(data))
except IOError:
    pass

logging.debug("disconnected")

client_sock.close()
server_sock.close()