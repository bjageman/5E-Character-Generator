import sys
import requests, json
from optparse import OptionParser

from v1.apps import app, db, socketio
from v1.apps.users.models import User

from v1.apps.config import DATABASE

from socketIO_client import SocketIO

config = {
    "debug":{
        'url':"0.0.0.0:5000",
    },
	"production":{
        'url':"",
	},

}
version = "debug"

parser = OptionParser()
parser.add_option("-a", "--admin", dest="admin_id", type="int",
                  help="set the admin ID", metavar="ADMIN_ID")
parser.add_option('--setup', dest="setup", default = False, action = 'store_true',
                  help="Runs the initial DB setup")
parser.add_option("--pass", dest="password",
                  help="set a password for admin or login", metavar="PASSWORD")
parser.add_option("-r", "--register-user", dest="register_user",
                  help="creates a new user with the password 'password'", metavar="USERNAME")
parser.add_option("-u", "--user", dest="user_id", type="int",
                  help="set the current user ID", metavar="USER_ID")
parser.add_option("--username", dest="username",
                  help="set the current username", metavar="USERNAME")



def on_login_response(*args):
    print('on_login_response', args)

def on_disconnect():
    print('disconnect')

def on_connect():
    print('connect')

def registerUser(username, password = "password"):
    payload = {'username':username, 'password': password}
    r = requests.post("http://" + config[version]['url'] + '/api/v1/users', json=payload)
    print(r.text)

def loginUser(username, password = "password"):
    print("logging user", username)
    socketIO.on('user_login_success', on_login_response)
    print("logging user", username)
    socketIO.emit('login', {
        "username": username,
        "password": password
        }, on_login_response)

def votePlayer(voter_id, choice_id, role_id = None):
    socketIO.on('vote_success', on_vote_success)
    if role_id is None:
        socketIO.emit('set_vote', {
            "voter_id": voter_id,
            "choice_id": choice_id,
        })
    else:
        socketIO.emit('set_vote', {
            "voter_id": voter_id,
            "choice_id": choice_id,
            "role_id": role_id,
        })

def setPlayerRole(player_id, role_id, admin_id, password):
    print("Setting player",player_id, "to role id", role_id )
    socketIO.emit('admin_set_role', {
        "player_id": player_id,
        "role_id": role_id,
        "admin_id": admin_id,
        "password": password
    })

def checkAdmin(admin_id, password):
    if admin_id is not None and password is not None:
        return True
    else:
        print("Input the admin and password for this function")
        return False

if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
    #Initialize flags
    (options, args) = parser.parse_args()
    user_id = options.user_id
    username = options.username
    register_user = options.register_user
    admin_id = options.admin_id
    password = options.password
    if options.setup:
        print("Creating Database...")
        db.create_all()
        print("Database Created")
        db.session.commit()
    if register_user is not None:
        registerUser(register_user)

    #Run socket commands
    with SocketIO(config[version]['url'], 5000) as socketIO:
        socketIO.on('connect', on_connect)
        if username is not None:
            loginUser(username)
        socketIO.wait(seconds=1)
        socketIO.on('disconnect', on_disconnect)
