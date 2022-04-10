import socket as soc
from time import sleep

IP = '192.168.1.1'
PORT = 2390

DEST = (IP, PORT)

MY_IP = '192.168.1.2'


def ip_to_bytes(ip: str) -> bytes:
    return b''.join(int(i).to_bytes(1, 'big', signed=False) for i in ip.split('.'))


def main():
    with soc.socket(soc.AF_INET, soc.SOCK_DGRAM) as s:
        for i in range(256):
            s.sendto(i.to_bytes(1, 'big', signed=False), DEST)
            a = s.recvfrom(1024)
            print(f"{a[0][0] = }")
            sleep(0.01)


if __name__ == '__main__':
    main()
