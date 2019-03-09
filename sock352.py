
import binascii
import socket as syssock 
import sys
import threading
import struct


# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from


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
protocol = 0
sock352PktHdrData = '!BBBBHHLLQQLL'
UDP_port = 0
UDP_IP = 0
header_len = 00001100
udpPkt_hdr_data = struct.Struct(sock352PktHdrData)

def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
	UDP_port = UDPportTx
	UDP_IP = UDPportRx
	pass 
	
sock = None

class socket:
	
	def __init__(self):  # fill in your code here 
	
		if sock is None:
			self.sock = syssock.socket(
				syssock.AF_INET, syssock.SOCK_DGRAM)
			#self.sock.setblocking(0)
			self.sock.settimeout(1) 
		else:
			self.sock = sock
			self.sock.settimeout(1) 
			#self.sock.setblocking(0)
		return
	
	def bind(self,address):
		return 

	def connect(self,address):  # fill in your code here 
		
		#first step of handshake
		
		server_address = (address, UDP_port)
		
		udpPkt_header_data = struct.Struct(sock352PktHdrData)
		
		header = udpPkt_header_data.pack(version, flags, opt_ptr, protocol, checksum, header_len,source_port, dest_port, sequence_no, ack_no, window, payload_len)
		
		self.sock.sendto(header, server_address)
		
		#look for connections 
		#the sender sends a packet, 3rd step of handshake 
		self.sock.bind(server_address)
		(data,address) = self.sock.recv(1024)
		
		header_unpack = udpPkt_header_data.unpack('!BBBBHHLLQQLL',header)
		array = header_unpack.split(', ')

		unpack_list=header_unpack.split(', ')
		ack_rec = unpack_list(8)
		seq = unpack_list(7)
		if(ack_rec > 1):
			print("hello from client")
			ack_send = seq + 1
			seq = ack_rec
			
			udpPkt_header_data = struct.Struct(sock352PktHdrData)

			header = udpPkt_header_data.pack(version, flags, opt_ptr, protocol, checksum, header_len, source_port, dest_port, seq, ack_send, window, payload_len)

			self.sock.sendto(header, server_address)
		else:
			return 
		#no packet is received 
		
			
	
	def listen(self,backlog):
		return

	def accept(self):

		#2nd step of handshake
		self.sock.bind(('',UDP_port))
		
		(data,address) = self.sock.recv(1024)
		header_unpack = udpPkt_header_data.unpack('!BBBBHHLLQQLL',header)

		array = header_unpack.split(', ')

		unpack_list=header_unpack.split(', ')
		flag=unpack_list(1)
		if flag is 1:
			print("hello from server")
			seq=unpack_list(6)
			ack_no = seq + 1
			
			udpPkt_header_data = struct.Struct(sock352PktHdrData)

			header = udpPkt_header_data.pack(version, flags, opt_ptr, protocol, checksum, header_len, source_port, dest_port, sequence_no, ack_no, window, payload_len)
			self.sock.sendto(header, address)
				
		
	   # change this to your code 
		return (self.sock,address)
	
	def close(self):   # fill in your code here 
		return 

	def send(self,buffer):
		bytessent = 0     # fill in your code here 
		return bytesent 

	def recv(self,nbytes):
		bytesreceived = 0     # fill in your code here
		return bytesreceived 


	


