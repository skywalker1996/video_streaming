from configs.config import Config
import json
import time
from queue import Queue  
import numpy 
import socket
import ctypes
from threading import Thread, Lock
import numpy as np
import ipaddress
import select
#创建socket对象
#SOCK_DGRAM    udp模式
# sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# sock.bind(("127.0.0.1",8871))  #绑定服务器的ip和端口
# i = 0

# while(True):
# 	data, address=sock.recvfrom(60016)  #一次接收60016字节
# 	print('===========  ', i)
# 	print(data, address)# decode()解码收到的字节
# 	i+=1
class Middleware(object):
	def __init__(self):
		self.recv_buffer = Queue(1000000)

	def recv_thread(self):

		server_recv_proxy = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		server_recv_proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_recv_proxy.bind(("192.168.0.102", 9303))
		start_time = time.time()
		send_count = 0
		while(True):
			data = server_recv_proxy.recv(2000)
			self.recv_buffer.put(data)
			current_time = time.time()
			###modify the bandwidth every 1 second
			if(current_time - start_time >= 1):
				send_throughput = (send_count*8)/(10**6) 
				start_time = time.time()
				send_count = 0
				print('******recv throughput = {}'.format(send_throughput))
			else:
				send_count+=len(data)

	def send_thread(self):

		server_send_proxy=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		server_send_proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		start_time = time.time()
		send_count = 0
		while(True):
			data = self.recv_buffer.get()
			server_send_proxy.sendto(data, ("192.168.0.141",9002))
			# print('send data index', send_index)
			current_time = time.time()
			if(current_time - start_time >= 1):
				send_throughput = (send_count*8)/10**6 
				start_time = time.time()
				send_count = 0
				print('******send throughput = {}'.format(send_throughput))
			else:
				send_count+=len(data)
		# print('send data')
	def start(self):
		sendthread = Thread(target=self.send_thread, args=())
		sendthread.daemon = True

		recvthread = Thread(target=self.recv_thread, args=())
		recvthread.daemon = True

		# sendthread.start()
		recvthread.start()
		print('Monax server start!')

		# sendthread.join()
		recvthread.join()
	                              
if __name__ == '__main__': 

	middleware = Middleware()
	middleware.start()
	print('Experiment finish!')