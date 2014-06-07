# Explicit import to enable 'python app.py'
import __init__ 

import hashlib, uuid, sqlite3
from OpenSSL import SSL
from flask import Flask
from flask_cors import cross_origin
from flask_jsonrpc import JSONRPC
from flask.ext.httpauth import HTTPBasicAuth
from printer import PrinterController
from header_decorators import json_headers

DB = 'users.db'
PRINTER = PrinterController()

app = Flask(__name__)
auth = HTTPBasicAuth()
jsonrpc = JSONRPC(app, "/api", decorators=[
    cross_origin(methods=['POST', 'OPTIONS'], headers=["accept", "authorization", "content-type"]),
    json_headers
])


# Not a route on purpose.
# Use an interactive Python shell to add users.
def add_user(username, password):
    '''Adds a new JSON-RPC user to the database.'''

    salt = str(uuid.uuid4())
    db = sqlite3.connect(DB)
    db.cursor().execute('''
        INSERT INTO users(username, pwd_hash, salt) VALUES (?, ?, ?)
    ''', (username, hashlib.sha256(password + "\x00" + salt).hexdigest(), salt))
    db.commit()
    db.close()


@auth.verify_password
def verify_pwd(username, password):
    '''Verifies the given username and password.'''

    db = sqlite3.connect(DB)
    cr = db.cursor()
    cr.execute('''
        SELECT pwd_hash, salt FROM users WHERE username = ?
    ''', (username,))
    user = cr.fetchone()
    db.close()

    return bool(user) and (
        user[0] == hashlib.sha256(password + "\x00" + user[1]).hexdigest()
    )

## Routes & JSON-RPC methods ##

@app.route("/")
def index():
    return "SSL exception added for this session."


@jsonrpc.method("output")
@auth.login_required
def output(printer_name="zebra_python_unittest", format="epl2", data=[]):
    '''Print something on the printer.'''
    return PRINTER.output(printer_name=printer_name, format=format,
                          data=data, raw=False, test=False)


if __name__ == "__main__":
    # Setup database
    db = sqlite3.connect(DB)
    db.cursor().execute('''
        CREATE TABLE IF NOT EXISTS
        users(username TEXT PRIMARY KEY, pwd_hash TEXT, salt TEXT)
    ''')
    db.commit()
    db.close()

    # Setup SSL cert
    ssl_context = SSL.Context(SSL.SSLv23_METHOD)
    ssl_context.use_privatekey_file('server.key')
    ssl_context.use_certificate_file('server.crt')

    app.run(debug=True, port=5001, ssl_context=ssl_context)
