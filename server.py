from flask import Flask, render_template, url_for
from flask_socketio import SocketIO
from flask import request, session, redirect
from database import Database


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
		if "username" in session:
			# if the user already logged in.
			return redirect (url_for ("chat"))
		else:
			# if the user was not logged in and no session is created.
			return render_template ("login.html")
	else:
		# login the user while request.method is "POST"
		username = request.form.get ("username")
		password = request.form.get ("password")

		# check whether the credentials exists or not.
		query = f"""SELECT * FROM AUTH 
			WHERE Username='{username}' AND Password='{password}';
			"""

		database = Database ()
		database.execute (query)

		cred = database.cursor.fetchone () # ('rintu', '1234')
		database.close_connection ()

		if not cred or cred != (username, password):
			return """<!DOCTYPE html>
			<html>
			<head>
				<title>Failure</title>
			</head>
			<body>
				<h1>Wrong Credentials.</h1>
				Click <a href="/login">here</a> to login again.
			</body>
			</html>"""

		# make the username locked for the user.
		else:
			# insert the username into session
			session["username"] = username

			return redirect (url_for ("chat"))

@application.route ("/signup", methods=["GET", "POST"])
def signup ():
	if request.method == "GET":
		return render_template ("signup.html")
	else:
		# register the user.
		username = request.form.get ("username")
		password = request.form.get ("password")

		query = f""" INSERT INTO AUTH (Username, Password)
				VALUES ('{username}', '{password}'); """

		database = Database ()
		database.execute (query)

		# save the changes in the database
		database.close_connection ()
		del database

		return """
			<!DOCTYPE html>
			<html>
			<head>
				<title>Success</title>
			</head>
			<body>
				<h1>Success.</h1>
				Click <a href="/login">here</a> to go back to login page.
			</body>
			"""

@application.route ("/chat")
def chat ():
	# the basic front page of the server.
	if "username" in session:
		username = session ["username"]
		return render_template ("chat.html", username=username)
	else:
		return redirect (url_for ("index"))

# when "client_message" occurs in client side
@socketio.on ("client_message")
def show (message_data):
	print ("Server Received: ", message_data)

	# send "my response" back to the client.
	socketio.emit ("server_response", message_data)

if __name__ == "__main__":
	# socket created at default port = 5000
	socketio.run (application, debug=True)