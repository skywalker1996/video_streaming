import socket
import select
from threading import Thread, Lock
from queue import Queue
import time
import asyncio

## transfer bandwidth(Mbps) to sending intervals between packets
async def bw2interval(bw):

    pkts_per_sec = bw*(10**6)/8/1316
    sending_interval = 1/pkts_per_sec

    return sending_interval

recv_buffer = Queue(10000)
recv_count = 0

async def recv():
    global recv_count
    global recv_buffer
    server_recv_proxy = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server_recv_proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_recv_proxy.bind(("127.0.0.1", 8873))
    while(True):
        data = server_recv_proxy.recv(2000)
        start_time = time.time()
        # recv_buffer.put(data)
        recv_count = recv_count + 1
        # print('recv count = ', recv_count)
        # print("queue put cost time: ")
        print('recv ack')


async def send():
    global recv_buffer
    server_send_proxy=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # server_send_proxy.set
    start_time = time.time()
    last_send_time = time.time()
    send_count = 0
    real_sending_interval = await bw2interval(1000)
    print(real_sending_interval)
    server_send_proxy.connect(("192.168.0.143",8876))
    while(True):
        current_send_time = time.time()

        # await asyncio.sleep(0.000000001)
        # print(current_send_time-last_send_time)
        # if(current_send_time-last_send_time>=real_sending_interval):
        current_send_time = time.time()
        # print(current_send_time-last_send_time)
        data = ('1'*1316).encode() 
        # data = recv_buffer.get()
        res = server_send_proxy.send(data)
        current_time = time.time()
        ###modify the bandwidth every 1 second
        if(current_time - start_time >= 1):
            send_throughput = (send_count*8)/(10**6) 
            start_time = time.time()
            send_count = 0
            print('******server send throughput = {}'.format(send_throughput))
        else:
            send_count+=len(data)

        last_send_time = current_send_time
            # break

def recv_thread():
    asyncio.run(recv())

def send_thread():
    asyncio.run(send())


sendthread = Thread(target=send_thread, args=())
sendthread.daemon = True

recvthread = Thread(target=recv_thread, args=())
recvthread.daemon = True

sendthread.start()
recvthread.start()
print('Monax server start!')

sendthread.join()
recvthread.join()
