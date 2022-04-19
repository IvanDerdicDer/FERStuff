import argparse
import os
import pickle
from dataclasses import dataclass
from getpass import getpass
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from typing import Dict


@dataclass
class HashedPasswd:
    secret: bytes
    hashed_passwd: bytes
    force_change: bool = False


DATABASE = Dict[bytes, HashedPasswd]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-a',
        '--add',
        action='store_true',
        default=False
    )

    parser.add_argument(
        '-pass',
        '--passwd',
        action='store_true',
        default=False
    )

    parser.add_argument(
        '-u',
        '--username',
        type=str,
        required=True
    )

    parser.add_argument(
        '-fpass',
        '--force_passwd',
        action='store_true',
        default=False
    )

    parser.add_argument(
        '-d',
        '--delete',
        action='store_true',
        default=False
    )

    return parser.parse_args()


def check_passwd_secure(passwd: str) -> bool:
    return not any((
        passwd == passwd.lower(),
        passwd == passwd.upper(),
        not ''.join(i for i in passwd if i.isnumeric()),
        not ''.join(i for i in passwd if not i.isalnum()),
        len(passwd) < 8
    ))


def add_user(username: str, passwd: str, db: DATABASE) -> None:
    if not check_passwd_secure(passwd):
        print('Password needs to contain at least one upper case letter, lowercase letter, number, and special symbol '
              'and needs to be at least 8 characters long')
        exit(1)

    hasher = SHA256.new()
    hasher.update(username.encode())
    key = hasher.digest()

    if key in db:
        print('User already in the database')
        exit(1)

    secret = get_random_bytes(16) + key

    hashed_passwd = scrypt(passwd, secret.decode('unicode-escape'), 32, 2 ** 14, 8, 2)

    hashed_passwd = HashedPasswd(secret, hashed_passwd)

    db[key] = hashed_passwd

    with open('a', 'wb') as f:
        pickle.dump(db, f)


def change_passwd(username: str, new_passwd: str, db: DATABASE) -> None:
    if not check_passwd_secure(new_passwd):
        print('Password needs to contain at least one upper case letter, lowercase letter, number, and special symbol '
              'and needs to be at least 8 characters long')
        exit(1)

    hasher = SHA256.new()
    hasher.update(username.encode())
    key = hasher.digest()

    secret = get_random_bytes(16) + key

    hashed_passwd = scrypt(new_passwd, secret.decode('unicode-escape'), 32, 2 ** 14, 8, 2)
    hashed_passwd = HashedPasswd(secret, hashed_passwd)

    if key not in db:
        print('Incorrect username.')
        exit(1)

    db[key] = hashed_passwd

    with open('a', 'wb') as f:
        pickle.dump(db, f)


def set_forced_passwd(username: str, db: DATABASE) -> None:
    hasher = SHA256.new()
    hasher.update(username.encode())
    key = hasher.digest()

    if key not in db:
        print('Incorrect username.')
        exit(1)

    db[key].force_change = True

    with open('a', 'wb') as f:
        pickle.dump(db, f)


def delete_user(username: str, db: DATABASE) -> None:
    hasher = SHA256.new()
    hasher.update(username.encode())
    key = hasher.digest()

    if key not in db:
        print('Incorrect username.')
        exit(1)

    db.pop(key)

    with open('a', 'wb') as f:
        pickle.dump(db, f)


def main():
    args = parse_args()

    db = {}
    if os.path.isfile('a'):
        with open('a', 'rb') as f:
            db = pickle.load(f)

    if args.add:
        passwd = getpass('Password: ')
        r_passwd = getpass('Repeat password: ')

        if passwd != r_passwd:
            print('Password mismatch')
            exit(1)

        add_user(args.username, passwd, db)
        print('User added')
        return

    if args.passwd:
        passwd = getpass('Password: ')
        r_passwd = getpass('Repeat password: ')

        if passwd != r_passwd:
            print('Password mismatch')
            exit(1)

        change_passwd(args.username, passwd, db)
        print('Password changed')
        return

    if args.force_passwd:
        set_forced_passwd(args.username, db)
        print('Forced password changed')
        return

    if args.delete:
        delete_user(args.username, db)
        print('User deleted')
        return


if __name__ == '__main__':
    main()
