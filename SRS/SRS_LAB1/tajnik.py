import argparse
import pickle
from Crypto.Hash import HMAC, SHA256, SHA512
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="A simple password manager")
    parser.add_argument('-i', '--init',
                        action='store_true',
                        default=False,
                        help="Flag to init the password manager")
    parser.add_argument('-m', '--master',
                        type=str,
                        required=True,
                        help="Master password")
    parser.add_argument('-l', '--location',
                        type=str,
                        required=False,
                        help='URI/URL of the website which password you want to store')
    parser.add_argument('-pass', '--passwd',
                        type=str,
                        required=False,
                        help='Password you want to store')
    parser.add_argument('-p', '--put',
                        action='store_true',
                        default=False,
                        help='Flag to add a password to the database')
    parser.add_argument('-g', '--get',
                        action='store_true',
                        default=False,
                        help='Flag to get your password from the database')

    return parser.parse_args()


def check_arg_conflict(args: argparse.Namespace) -> None:
    arg_sum = sum([args.init, args.put, args.get])
    if arg_sum > 1:
        raise argparse.ArgumentError(argument=None,
                                     message='You can set only one of the following flags: '
                                             '-i/--init, -p/--put, -g/--get')

    if arg_sum == 0:
        raise argparse.ArgumentError(argument=None,
                                     message='You have to seat at least one of the following flags: '
                                             '-i/--init, -p/--put, -g/--get')

    if args.put and not (args.location and args.passwd):
        raise argparse.ArgumentError(argument=None,
                                     message='When -p/--put is set both '
                                             '-l/--location and -pass/--passwd have to be given')

    if args.get and not args.location:
        raise argparse.ArgumentError(argument=None, message='When -g/--get is set -l/--location has to be given')


def init_database(master: str) -> dict:
    secret = b'%vMT8m6XT3u3m!&H'
    h = HMAC.new(secret, digestmod=SHA256)
    h.update(master.encode())

    print(h.verify(h.digest()))


def main():
    args = parse_args()
    check_arg_conflict(args)
    print(args)

    init_database(args.master)


if __name__ == '__main__':
    main()
