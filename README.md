# printer_proxy_server

A Flask server that provides a JSON-RPC interface to an Eltron 2844 CTP label printer, protected by SSL and Basic HTTP Authentication. It is designed for use with [printer_proxy](https://github.com/ryepdx/printer_proxy).

Assumes the printer is named "zebra" by default.

## Usage:

    $ python app.py

## Usage for printers not named "zebra":

    $ python app.py -d "Eltron 2844"

## Adding users

    $ python
    
    >>> from app import add_user
    >>> add_user("user", "password")
    >>> exit()

## Removing users

    $ python
    
    >>> from app import delete_user
    >>> delete_user("user")
    >>> exit()

## Accessing the user database directly

    $ sqlite3 users.db
    
    sqlite> select * from users;

    user|494c884325be4798032547ee6525d03d8bf96977d623a2ebafa0095bf5b194dd|4f1a6f06-c8fd-4526-a375-986fa298c36b

    sqlite> .q
