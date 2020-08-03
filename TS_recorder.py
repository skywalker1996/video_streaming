import socket
import select
from queue import Queue
import pickle
import time


print('TS receiver start!')

client_recv_proxy = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_recv_proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_recv_proxy.bind(("192.168.0.100",8878))

recv_count = 0  
recv_buffer = []

flag = 1                     
cold_start = True
timestamp = 0

while(flag):
	data = client_recv_proxy.recv(2000)
	if(cold_start):
		cold_start = False
		start_time = time.time()
		timestamp = 0
	else:
		timestamp = time.time() - start_time

	recv_buffer.append((timestamp,data))
	print(f"*** {timestamp}")
	recv_count+=len(data)
	# print("Lsize=", recv_count/1024)
	if((recv_count/1024)>=200000):
		flag=0
		break

with open ('./ts/video_ts','wb') as f:
	pickle.dump(recv_buffer,f)
	print("finish dumping!")


                                                       