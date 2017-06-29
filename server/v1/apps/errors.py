from flask_socketio import emit

def emit_error(error, room=None):
    emit('send_error',{
        'error': error
        }, room=room)
