from flask import Flask, render_template
from flask_socketio import SocketIO
import json


application = Flask (__name__)
application.config ["SECRET_KEY"] = "4as5x8xf7g"
socketio = SocketIO (application)


@application.route ("/")
def index ():
	# the basic front page of the server.
	return render_template ("index.html")

# when "client_message" occurs in client side
@socketio.on ("client_message")
def show (message_data):
	print ("Server Received: ", message_data)

	# send "my response" back to the client.
	socketio.emit ("server_response", message_data)

if __name__ == "__main__":
	# socket created at default port = 5000
	socketio.run (application, debug=True)