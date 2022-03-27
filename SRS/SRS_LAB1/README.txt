usage: tajnik.py [-h] [-i] -m MASTER [-l LOCATION] [-pass PASSWD] [-p] [-g]

A simple password manager

options:
  -h, --help            show this help message and exit
  -i, --init            Flag to init the password manager
  -m MASTER, --master MASTER
                        Master password
  -l LOCATION, --location LOCATION
                        URI/URL of the website which password you want to store
  -pass PASSWD, --passwd PASSWD
                        Password you want to store
  -p, --put             Flag to add a password to the database
  -g, --get             Flag to get your password from the database

examples:
    Initialize password database:
    python3 tajnik.py -i -m ExampleMasterPassword

    Put a password into the database:
    python3 tajnik.py -p -m ExampleMasterPassword -l www.example.org -pass ExamplePassword

    Get a password from the database:
    python3 tajnik.py -g -m ExampleMasterPassword -l www.example.org
