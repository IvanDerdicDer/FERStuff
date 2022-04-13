from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import argparse
import pickle
from dataclasses import dataclass
import os
from getpass import getpass


@dataclass
class HashedPasswd:
    secret: bytes
    hashed_passwd: bytes
    force_change: bool = False


DATABASE = dict[bytes, HashedPasswd]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-u',
        '--username',
        type=str,
        required=True
    )

    return parser.parse_args()


def login(username: str, passwd: str, db: DATABASE) -> bool:
    hasher = SHA256.new()
    hasher.update(username.encode())
    key = hasher.digest()

    if key not in db:
        print('Incorrect username or password')
        return False

    hashed_passwd: HashedPasswd = db[key]

    hasher = HMAC.new(hashed_passwd.secret, digestmod=SHA256)
    hasher.update(passwd.encode())

    try:
        hasher.verify(hashed_passwd.hashed_passwd)
    except ValueError:
        print('Incorrect username or password')
        return False

    if hashed_passwd.force_change:
        new_passwd = getpass('New password: ')
        r_new_passwd = getpass('Repeat new password: ')

        if new_passwd != r_new_passwd:
            print('Password missmatch')
            return False

        if not change_passwd(username, new_passwd, db):
            return False
        print('Password changed')
        return True

    print('Logged in')
    return True


def change_passwd(username: str, new_passwd: str, db: DATABASE) -> bool:
    hasher = SHA256.new()
    hasher.update(username.encode())
    key = hasher.digest()

    if key not in db:
        print('Incorrect username or password')
        return False

    secret = get_random_bytes(16) + key

    hasher = HMAC.new(secret, digestmod=SHA256)
    hasher.update(new_passwd.encode())

    hashed_passwd = hasher.digest()
    hashed_passwd = HashedPasswd(secret, hashed_passwd)

    db[key] = hashed_passwd

    with open('a', 'wb') as f:
        pickle.dump(db, f)

    return True


def main():
    args = parse_args()

    if not os.path.isfile('a'):
        print('No users in the database')
        exit(0)

    with open('a', 'rb') as f:
        db = pickle.load(f)

    hasher = SHA256.new()
    hasher.update(args.username.encode())
    key = hasher.digest()

    if key not in db:
        print('Incorrect username or password')
        return

    for _ in range(3):
        passwd = getpass('Password: ')
        if login(args.username, passwd, db):
            return


if __name__ == '__main__':
    main()
