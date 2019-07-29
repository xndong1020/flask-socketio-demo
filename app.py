# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_socketio import SocketIO,send,emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

clients = {}

@app.route('/')
def index():
    import ipdb
    ipdb.set_trace()
    emit('myEvent', { 'data': 'test data' },namespace='/', broadcast=True)
    return "Hello, World!"
 

@socketio.on('message')
def handle_message(message):
    print('received message', message)
    send(message)
    # emit('my response', message)

@socketio.on('json')
def handle_json(json):
    print('json', json)
    # send(json, json=True)

@socketio.on('myEvent')
def handle_my_custom_event(json):
    print('handle_my_custom_event', json)
    # emit('message', request.sid, room=clients[request.sid])
    emit('myEvent', json)
    # send(request.sid, broadcast=True)
    # send({'data': 'Connected'},json=True)

@socketio.on('connect')
def test_connect():
    print('{} connected'.format(request))
    print('{} connected'.format(request.sid))
    clients[request.sid] = request.sid
    print('clients', clients)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    clients.remove(request.sid)

if __name__ == '__main__':
    socketio.run(app,debug=True,host='0.0.0.0',port=9999)