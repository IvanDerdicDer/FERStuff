import argparse
import json
import pickle
import os
from Crypto.Hash import HMAC, SHA256
from Crypto.Protocol.KDF import scrypt
from Crypto.Cipher import AES


DB_TYPE = dict[str, tuple[bytes, bytes, bytes]]
ENCRYPTED_PASSWD = tuple[bytes, bytes, bytes]


def parse_args() -> argparse.Namespace:
    """
    Function that parses required command line arguments
    :return:
    """
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
                                     message='When -p/--put is set both '
                                             '-l/--location and -pass/--passwd have to be given')

    if args.get and not args.location:
        raise argparse.ArgumentError(argument=None, message='When -g/--get is set -l/--location has to be given')


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
    secret = b'%vMT8m6XT3u3m!&H'
    h = HMAC.new(secret, digestmod=SHA256)
    h.update(master.encode())

    db = {h.hexdigest(): encrypt_passwd('R^a$NL3W?FX*X&SP', 'www.www.www', master)}

    write_db_to_disc(db)


def check_master_password(master: str, db: DB_TYPE) -> bool:
    """
    Function that checks if the master password is correct
    :param master:
    :param db:
    :return:
    """
    secret = b'%vMT8m6XT3u3m!&H'
    h = HMAC.new(secret, digestmod=SHA256)
    h.update(master.encode())

    if h.hexdigest() in db:
        try:
            db_keys = list(db)
            h.hexverify(db_keys[db_keys.index(h.hexdigest())])
            return True
        except ValueError:
            return False

    return False


def encrypt_passwd(passwd: str, location: str, master: str) -> ENCRYPTED_PASSWD:
    """
    Function that encrypts the password with integrity in mind
    :param passwd: Password to encrypt
    :param location: Location with which th password is associated
    :param master: Master password
    :return:
    """
    key = scrypt(master, location, 32, N=2**14, r=8, p=8)
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce

    cipher_text, tag = cipher.encrypt_and_digest(passwd.encode())

    return cipher_text, tag, nonce


def decrypt_passwd(encrypted_passwd: ENCRYPTED_PASSWD, location: str, master: str) -> str:
    """
    Function that decrypts a password for the given location
    :param encrypted_passwd:
    :param location: Location with which th password is associated
    :param master: Master password
    :return:
    """
    key = scrypt(master, location, 32, N=2**14, r=8, p=8)
    cipher = AES.new(key, AES.MODE_EAX, nonce=encrypted_passwd[2])

    plain_text = cipher.decrypt_and_verify(encrypted_passwd[0], encrypted_passwd[1])

    return plain_text.decode()


def put_passwd_in_db(location: str, passwd: str, master: str, db: DB_TYPE) -> None:
    secret = SHA256.new(location.encode()).digest()
    h = HMAC.new(secret, digestmod=SHA256)
    h.update(location.encode())

    key = h.hexdigest()
    encrypted_passwd = encrypt_passwd(passwd, location, master)

    db[key] = encrypted_passwd

    write_db_to_disc(db)


def get_passwd_from_db(location: str, master: str, db: DB_TYPE) -> str:
    secret = SHA256.new(location.encode()).digest()
    h = HMAC.new(secret, digestmod=SHA256)
    h.update(location.encode())

    if h.hexdigest() in db:
        db_keys = list(db.keys())
        h.hexverify(db_keys[db_keys.index(h.hexdigest())])
    else:
        raise ValueError('Location does not exist in the database')

    return decrypt_passwd(db[h.hexdigest()], location, master)


def main():
    args = parse_args()
    check_arg_conflict(args)

    if args.init:
        init_database(args.master)
        print('Password manager initialized')
        return

    if not os.path.isfile('a'):
        raise FileNotFoundError("Database was not initialized")

    db = read_db_from_disc()

    if not check_master_password(args.master, db):
        raise ValueError('Master password is not correct')

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
