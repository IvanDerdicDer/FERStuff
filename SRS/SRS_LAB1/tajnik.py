import argparse
import pickle
import os
from Crypto.Hash import HMAC, SHA256
from Crypto.Protocol.KDF import scrypt
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from typing import Dict, Tuple

DB_TYPE = Dict[str, Tuple[bytes, bytes, bytes]]
ENCRYPTED_PASSWD = Tuple[bytes, bytes, bytes]


def parse_args() -> argparse.Namespace:
    """
    Function that parses required command line arguments
    :return:
    """

    examples = 'examples:\n'\
        '    Initialize password database:\n'\
        '    python3 tajnik.py -i -m ExampleMasterPassword\n'\
        '\n'\
        '    Put a password into the database:\n'\
        '    python3 tajnik.py -p -m ExampleMasterPassword -l www.example.org -pass ExamplePassword\n'\
        '\n'\
        '    Get a password from the database:\n'\
        '    python3 tajnik.py -g -m ExampleMasterPassword -l www.example.org\n'

    parser = argparse.ArgumentParser(description="A simple password manager",
                                     epilog=examples,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', '--init',
                        action='store_true',
                        default=False,
                        help="Flag to init the password manager")
    parser.add_argument('-p', '--put',
                        action='store_true',
                        default=False,
                        help='Flag to add a password to the database')
    parser.add_argument('-g', '--get',
                        action='store_true',
                        default=False,
                        help='Flag to get your password from the database')
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

    return parser.parse_args()


def check_arg_conflict(args: argparse.Namespace) -> None:
    """
    Function that checks if validity of parsed arguments
    :param args: All command line arguments
    :return:
    """
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
                                     message='When -p/--put is set -m/--master, '
                                             '-l/--location and -pass/--passwd have to be given')

    if args.get and not args.location:
        raise argparse.ArgumentError(argument=None,
                                     message='When -g/--get is set -m/--master and -l/--location have to be given')


def write_db_to_disc(db: DB_TYPE) -> None:
    """
    Function that writes the database to the disc
    :param db: Database
    :return:
    """
    with open('a', 'wb') as f:
        pickle.dump(db, f)


def read_db_from_disc() -> DB_TYPE:
    """
    Function that reads the database of the disc
    :return:
    """
    with open('a', 'rb') as f:
        return pickle.load(f)


def init_database(master: str) -> None:
    """
    Function that initializes the database
    :param master: Master password
    :return:
    """
    db = {}

    put_passwd_in_db('%#b4cbks%CmVUced', master, master, db)

    write_db_to_disc(db)


def check_master_password(master: str, db: DB_TYPE) -> bool:
    """
    Function that checks if the master password is correct
    :param master: Master password
    :param db: Database
    :return:
    """
    return get_passwd_from_db('%#b4cbks%CmVUced', master, db) == master


def encrypt_passwd(passwd: str, master: str, location: str) -> ENCRYPTED_PASSWD:
    """
    Function that encrypts the password with integrity in mind
    :param location:
    :param passwd: Password to encrypt
    :param master: Master password
    :return:
    """
    salt = get_random_bytes(16)
    key = scrypt(master, str(salt) + location, 32, N=2 ** 14, r=8, p=2)
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce

    cipher_text, tag = cipher.encrypt_and_digest(passwd.encode())

    return salt + cipher_text, tag, nonce


def decrypt_passwd(encrypted_passwd: ENCRYPTED_PASSWD, salt: str, master: str) -> str:
    """
    Function that decrypts a password for the given location
    :param encrypted_passwd:
    :param salt: Location with which th password is associated
    :param master: Master password
    :return:
    """
    key = scrypt(master, salt, 32, N=2 ** 14, r=8, p=2)
    cipher = AES.new(key, AES.MODE_EAX, nonce=encrypted_passwd[2])

    try:
        plain_text = cipher.decrypt_and_verify(encrypted_passwd[0][16:], encrypted_passwd[1])
        return plain_text.decode()
    except ValueError:
        print("Master password incorrect or integrity check failed")
        exit()


def put_passwd_in_db(location: str, passwd: str, master: str, db: DB_TYPE) -> None:
    """
    Function that puts the password for the given location in the database
    :param location: Location
    :param passwd: Password associated with the location
    :param master: Master password
    :param db: Database
    :return:
    """
    salt = 'cPf$BPaXx#+!NT24'
    secret = scrypt(location, salt, 16, N=2 ** 10, r=8, p=1)
    h = HMAC.new(secret, digestmod=SHA256)
    h.update(location.encode())

    key = h.hexdigest()
    encrypted_passwd = encrypt_passwd(passwd, master, location)

    db[key] = encrypted_passwd

    write_db_to_disc(db)


def get_passwd_from_db(location: str, master: str, db: DB_TYPE) -> str:
    """
    Function that gets the password from the database
    :param location: Location
    :param master: Master password
    :param db: Database
    :return:
    """
    salt = 'cPf$BPaXx#+!NT24'
    secret = scrypt(location, salt, 16, N=2 ** 10, r=8, p=1)
    h = HMAC.new(secret, digestmod=SHA256)
    h.update(location.encode())

    if h.hexdigest() not in db:
        print('Location does not exist in the database')
        exit()

    encrypted = ''
    try:
        encrypted = db[h.hexdigest()]
    except KeyError:
        print('Location does not exist in the database')
        exit()

    salt = str(encrypted[0][0:16]) + location

    return decrypt_passwd(encrypted, salt, master)


def main():
    args = parse_args()
    check_arg_conflict(args)

    if args.init:
        if not os.path.isfile('a'):
            init_database(args.master)
            print('Password manager initialized')
            return
        else:
            print("Database is already initialized")
            exit()

    if not os.path.isfile('a'):
        print("Database was not initialized")
        exit()

    db = read_db_from_disc()

    if not check_master_password(args.master, db):
        print('Master password is not correct')
        exit()

    if args.put:
        put_passwd_in_db(args.location, args.passwd, args.master, db)
        print(f'Stored password for {args.location}')
        return

    if args.get:
        passwd = get_passwd_from_db(args.location, args.master, db)
        print(f'Password for {args.location} is: {passwd}')
        return


if __name__ == '__main__':
    main()
