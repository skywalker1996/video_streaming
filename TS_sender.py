import socket
import select
from threading import Thread, Lock
from queue import Queue
import time
import pickle
import re
from H264_Stream import H264_Stream
import numpy as np


def send_thread():
    server_send_proxy=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    start_time = time.time()
        
    H264_stream=H264_Stream(video='./h264/dance2_h264', loss_mode='frame')

    while(True):

        (data, priority) = H264_stream.getNextPacket()

        server_send_proxy.sendto(data, ("192.168.0.107",8878))


sendthread = Thread(target=send_thread, args=())
sendthread.daemon = True

sendthread.start()

print('TS sender start!')

sendthread.join()