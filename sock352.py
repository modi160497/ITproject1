
import binascii
import socket as syssock 
import sys
import threading
import struct


# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from
from time import sleep

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
header_len = 12
udpPkt_hdr_data = struct.Struct(sock352PktHdrData)

def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
	global UDP_port
	global UDP_IP
	UDP_port = UDPportTx
	UDP_IP = UDPportRx

	pass

class socket:
	
	def __init__(self):  # fill in your code here 
	
		# if sock is None:
		self.sock = syssock.socket(
			syssock.AF_INET, syssock.SOCK_DGRAM)

		# if sock_rec is None:
		self.sock_rec = syssock.socket(
			syssock.AF_INET, syssock.SOCK_DGRAM)


		return
	
	def bind(self,address):
		return 

	def connect(self,address):  # fill in your code here

		#first step of handshake

		header = struct.pack(sock352PktHdrData, version, flags, opt_ptr, protocol, header_len, checksum, source_port, dest_port, sequence_no, ack_no, window, payload_len)

		send_address = ('127.0.0.1', int(UDP_port))
		print("in connect")
		print(send_address)

		print(header)
		self.sock.sendto(header, send_address)
		
		#look for connections 
		#the sender sends a packet, 3rd step of handshake

		self.sock_rec.settimeout(1)

		self.sock_rec.bind(('', int(UDP_IP)))
		(data, address) = self.sock_rec.recvfrom(1024)

		self.sock_rec.settimeout(0)

		header_unpack = struct.unpack('!BBBBHHLLQQLL',data)

		ack_rec = header_unpack[8]
		seq = header_unpack[7]
		if(ack_rec > 0):
			print("hello from client")
			ack_send = seq + 1
			seq = ack_rec

			header = struct.pack(sock352PktHdrData,version, flags, opt_ptr, protocol,  header_len, checksum, source_port, dest_port, seq, ack_send, window, payload_len)

			self.sock.sendto(header, send_address)
		else:
			return 
		#no packet is received 
		
			
	
	def listen(self,backlog):
		return

	def accept(self):

		#2nd step of handshake
		self.sock_rec.bind(('',int(UDP_IP)))
		
		(data, address) = self.sock_rec.recvfrom(1024)
		print (address)
		header_unpack = struct.unpack('!BBBBHHLLQQLL',data)
		print(header_unpack)

		send_address = ('127.0.0.1', int(UDP_port))

		flag= header_unpack[1]
		if flag is 1:
			print("hello from server")
			seq= header_unpack[6]
			ack_no = seq + 1

			header = struct.pack(sock352PktHdrData,version, flags, opt_ptr, protocol, checksum, header_len, source_port, dest_port, sequence_no, ack_no, window, payload_len)
			self.sock.sendto(header, send_address)
		
	   # change this to your code 
		return (self.sock,address)
	
	def close(self):   # fill in your code here 
		return 

	def send(self,buffer):
		bytessent = 0     # fill in your code here 
		return

	def recv(self,nbytes):
		bytesreceived = 0     # fill in your code here
		return bytesreceived 


	


