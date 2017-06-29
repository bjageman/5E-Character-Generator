from flask_script import Manager, Server

from v1.apps import app, socketio

# manager = Manager(app)
#
# manager.add_command("runserver", Server(
#     use_debugger = True,
#     use_reloader = True,
#     host = '0.0.0.0',
#     port = 5000)
# )

# if __name__ == "__main__":
#     manager.run()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
