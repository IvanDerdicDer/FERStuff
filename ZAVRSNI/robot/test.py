import socket as soc
from time import sleep

IP = '192.168.1.1'
PORT = 2390

DEST = (IP, PORT)

s = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)

for i in range(256):
    s.sendto(i.to_bytes(1, 'big', signed=False), DEST)
    sleep(0.01)
