
import binascii
import socket 
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
		sock352PktHdrData = '!BBBBHHLLQQLL'
		udpPkt_hdr_data = struct.Struct(sock352PktHdrData)
		version =  1
		flags = 1
		opt_ptr = 0
		checksum = 0
		source_port = 0
		dest_port= 0
		sequence_no = 1
		ack_no = 0
		window = 0
		payload_len = 0
		
		header = udpPkt_header_data.pack(version, flags, opt_ptr, protocol, checksum, source_port, dest_port, sequence_no, ack_no, window, payload_len)
		
		self.sock.sendto(header, server_address)
		
        return 
    
    def listen(self,backlog):
        return

    def accept(self):
	
		conn, addr = self.sock.accept()
		with conn:
			print('Connected by', addr)
			while True:
				data = conn.recv(1024)
				header_unpack = udpPkt_header_data.unpack('!BBBBHHLLQQLL',header)
				array = header_unpack.split(', ')
		
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


    


