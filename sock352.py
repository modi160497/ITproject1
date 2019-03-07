
import binascii
import socket as syssock
import struct
import sys

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
	UDP_port = UDPportRx
	UDP_IP = UDPportRx
    pass 
    
class socket:
    
    def __init__(self):  # fill in your code here 
		 if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.sock = sock
        return
    
    def bind(self,address):
		server_address = (address, UDP_IP)
		self.sock.bind(server_address)
        return 

    def connect(self,address):  # fill in your code here 
		server_address = (address, UDP_port)
		self.sock.connect(server_address)
        return 
    
    def listen(self,backlog):
        return

    def accept(self):
        (clientsocket, address) = (1,1)  # change this to your code 
        return (clientsocket,address)
    
    def close(self):   # fill in your code here 
        return 

    def send(self,buffer):
        bytessent = 0     # fill in your code here 
        return bytesent 

    def recv(self,nbytes):
        bytesreceived = 0     # fill in your code here
        return bytesreceived 


    


