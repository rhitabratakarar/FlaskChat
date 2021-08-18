from flask import Flask, render_template
from flask_socketio import SocketIO
from flask import request


application = Flask (__name__)
application.config ["SECRET_KEY"] = "4as5x8xf7g"
socketio = SocketIO (application)


@application.route ("/")
def index ():
	# redirect the page to login.
	return render_template ("index.html")

@application.route ("/login", methods=["GET", "POST"])
def login ():
	if request.method == "GET":
		return render_template ("login.html")
	else:
		# method is "POST"
		...

@application.route ("/signup", methods=["GET", "POST"])
def signup ():
	if request.method == "GET":
		return render_template ("signup.html")
	else:
		# method is "POST", thus register the user
		...

@application.route ("/chat")
def chat ():
	# the basic front page of the server.
	return render_template ("chat.html")

# when "client_message" occurs in client side
@socketio.on ("client_message")
def show (message_data):
	print ("Server Received: ", message_data)

	# send "my response" back to the client.
	socketio.emit ("server_response", message_data)

if __name__ == "__main__":
	# socket created at default port = 5000
	socketio.run (application, debug=True)