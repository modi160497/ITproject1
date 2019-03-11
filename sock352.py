import binascii
import socket as syssock
import sys
import threading
import struct

# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from
from time import sleep

# global variables for the header packet
version = 1
flags = 0
opt_ptr = 0
checksum = 0
source_port = 0
dest_port = 0
sequence_no = 1
ack_no = 0
window = 0
payload_len = 0
protocol = 0
UDP_port = 0
UDP_IP = 0

# get the header length in bytes
header_len = struct.calcsize('!BBBBHHLLQQLL')

sock352PktHdrData = '!BBBBHHLLQQLL'

packet_max = 1000

# total bytes recieved by the server
total = []


def init(UDPportTx, UDPportRx):  # initialize your UDP socket here
	global UDP_port
	global UDP_IP
	UDP_port = UDPportTx  # transmitting port
	UDP_IP = UDPportRx  # receiving port

	pass


class socket:

	def __init__(self):  # fill in your code here

		# create a socket to send
		self.sock = syssock.socket(
			syssock.AF_INET, syssock.SOCK_DGRAM)

		# create a socket to receive
		self.sock_rec = syssock.socket(
			syssock.AF_INET, syssock.SOCK_DGRAM)

		self.str_len = -1

		# array to store packets
		self.packetarr = []

		self.data_packets = []

		self.ack_no = 0

		self.sequence_no = 0

		return

	def bind(self, address):

		# do nothing

		return

	def connect(self, address):  # fill in your code here

		# first step of handshake
		syn = 1
		header = struct.pack(sock352PktHdrData, version, syn, opt_ptr, protocol, header_len, checksum, source_port,
							 dest_port, sequence_no, ack_no, window, payload_len)

		send_address = ('127.0.0.1', int(UDP_port))
		# print("in connect")

		self.sock.sendto(header, send_address)

		# the sender has sent a packet. 3rd step of handshake

		self.sock_rec.settimeout(1)

		# socket binds to the receiving port of the server

		self.sock_rec.bind(('', int(UDP_IP)))
		(data, address) = self.sock_rec.recvfrom(40)

		self.sock_rec.settimeout(0)

		header_unpack = struct.unpack('!BBBBHHLLQQLL', data)
		# print(header_unpack)

		ack_rec = header_unpack[8]
		seq = header_unpack[7]

		# the sender acks the 1st packet sent by client

		if (ack_rec > 0):
			print("hello from client")
			ack_send = seq + 1
			seq = ack_rec
			syn = 0

			header = struct.pack(sock352PktHdrData, version, syn, opt_ptr, protocol, header_len, checksum,
								 source_port, dest_port, seq, ack_send, window, payload_len)

			self.sock.sendto(header, send_address)

		# no packet is received
		return

	def listen(self, backlog):

		# do nothing

		return

	def accept(self):

		# 2nd step of handshake

		# socket binds to the receiving port of the client

		self.sock_rec.bind(('', int(UDP_IP)))

		while(True):
			(data, address) = self.sock_rec.recvfrom(1024)

			header_unpack = struct.unpack('!BBBBHHLLQQLL', data)
			#print(header_unpack)

			send_address = ('127.0.0.1', int(UDP_port))

			flag = header_unpack[1]

			# the client has sent a syn

			if flag is 1:
				print("hello from server")
				seq = header_unpack[6]
				ack_no = seq + 1

				header = struct.pack(sock352PktHdrData, version, flags, opt_ptr, protocol, checksum, header_len,
									 source_port, dest_port, sequence_no, ack_no, window, payload_len)
				self.sock.sendto(header, send_address)
			if flag is 0:
				if (ack_no == seq + 1):
					break

		return (self, address)

	def close(self):  # fill in your code here

		# close both recieving and sending sockets

		self.sock.close()

		self.sock_rec.close()

		return

	def create_packets(self, buffer):

		# max bytes from buffer in one packet can be the max payload size minus the header length

		max_payload = (packet_max - header_len)
		indexbeg = 0
		indexend = max_payload

		# get total number of packets
		number_packets = sys.getsizeof(buffer) / max_payload
		print(number_packets)

		# one packet sent if buffer is less than max packet size
		if (sys.getsizeof(buffer) < max_payload):
			header = struct.pack(sock352PktHdrData, version, flags, opt_ptr, protocol, checksum, header_len,
								 source_port, dest_port, sequence_no, ack_no, window, sys.getsizeof(buffer))
			number_packets = 1
			packet = header + buffer
			self.packetarr.append(packet)

		# create multiple packets
		else:

			for i in range(0, number_packets):
				print("index beg: " + str(indexbeg))
				print("index end: " + str(indexend))

				header = struct.pack(sock352PktHdrData, version, flags, opt_ptr, protocol, checksum, header_len,
									 source_port, dest_port, sequence_no, ack_no, window, sys.getsizeof(buffer))
				packet = header + buffer[indexbeg:indexend]
				print(sys.getsizeof(packet))
				self.packetarr.append(packet)
				indexbeg = indexend + 1
				indexend = indexbeg + max_payload

		# create packet for leftover bytes if length of the buffer is not divisible by the max packet size

		if(sys.getsizeof(buffer) % max_payload!= 0):
			print("index beg: " + str(indexbeg))
			print("index end: " + str(indexend))
			number_packets = number_packets + 1
			left_over = sys.getsizeof(buffer) - (number_packets * max_payload)
			header = struct.pack(sock352PktHdrData, version, flags, opt_ptr, protocol, checksum, header_len,
								 source_port, dest_port, sequence_no, ack_no, window, payload_len)
			packet = header + buffer[indexbeg+1:]
			print(sys.getsizeof(packet))
			self.packetarr.append(packet)

		return number_packets

	def send(self, buffer):

		print("in send")

		# address to transmit to
		send_address = ('127.0.0.1', int(UDP_port))

		bytessent = 0

		# the client sends over the file size

		if (self.str_len == -1):
			filesize = struct.unpack('!L', buffer)[0]
			self.str_len = filesize
			bytessent = sys.getsizeof(buffer)

			buffer = struct.pack('!L', bytessent)
			self.sock.sendto(buffer, send_address)

			print("filesize: " + str(filesize))

			return bytessent

		else:
			#print(buffer)

			number_packets = self.create_packets(buffer)

			# counter of packets sent
			counter = 0

			while(counter < number_packets):
				bytessent += sys.getsizeof(self.packetarr[counter])
				print("number of bytes sent: " + str(bytessent))
				self.sock.sendto(self.packetarr[counter], send_address)
				counter = counter + 1

		return bytessent

	def recv(self, nbytes):

		print("in recv")

		to_rcv = nbytes

		send_address = ('127.0.0.1', int(UDP_port))

		if (self.str_len == -1):
			print("file size sent")
			file_size_packet = self.sock_rec.recv(1024)
			self.str_len = struct.unpack("!L", file_size_packet)[0]
			longPacker = struct.Struct("!L")
			fileLenPacked = longPacker.pack(self.str_len)
			return fileLenPacked


		else:
			# while there is more to receive
			while to_rcv > 0:
				# receive packet and separate header from payload
				packet = self.sock_rec.recv(header_len + to_rcv)
				packet_header = packet[:header_len]
				packet_header = struct.unpack(sock352PktHdrData, packet_header)
				print("packet header" + str(packet_header))
				packet_data = packet[header_len:]
				print("packet data: " + str(packet_data))

				# if ack is not what we expect, ignore

				#if  packet_header[8] != self.ackno:
					#return


				# add data packets to the list of data in total we received and send ack
				self.data_packets.append(packet_data)
				self.ack_no += 1
				ack_flag = 0x04
				payload_len = len(packet_data)
				ack_pack = struct.pack(sock352PktHdrData, version, ack_flag, opt_ptr, protocol, checksum, header_len,
							 source_port, dest_port, self.sequence_no, self.ack_no, window, payload_len)
				self.sequence_no += 1
				self.sock.sendto(ack_pack, send_address)
				to_rcv -= sys.getsizeof(packet_data)
				print("number of bytes left: " + str(to_rcv))
				# add to total packets received

				total.append(packet_data)

		print(self.data_packets)

		return ' '.join(total)








