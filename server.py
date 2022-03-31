from flask import Flask, render_template, url_for
from flask_socketio import SocketIO
from flask import request, session, redirect
from database import Database
import json


application = Flask(__name__)
application.config["SECRET_KEY"] = "4as5x8xf7g"
socketio = SocketIO(application)


def user_session_exists(session):
    return "username" in session

def get_user_creds_from_req(request):
    username = request.form.get("username")
    password = request.form.get("password")
    return username, password

def correct_credentials(*creds) -> bool:
    query = f"""SELECT * FROM AUTH 
            WHERE Username='{creds[0]}' AND Password='{creds[1]}';
            """
    database = Database()
    database.execute(query)
    db_creds = database.cursor.fetchone()
    database.commit_and_close_connection()

    return True if db_creds else False

def get_wrong_creds_page() -> str:
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


def create_new_user(*creds):
    database = Database()
    database.create_user(creds[0], creds[1])
    database.commit_and_close_connection()
    del database

def get_success_page():
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

def get_username(request):
    return request.form.get("username")


@application.route("/")
@application.route("/home")
@application.route("/index")
def index():
    return render_template("index.html")


@application.route("/login", methods=["GET", "POST"])
@application.route("/existing-user", methods=["GET", "POST"])
def login():
    if request.method == "GET":

        if user_session_exists(session):
            return redirect(url_for("chat"))
        else:
            return render_template("login.html")

    else:
        creds = get_user_creds_from_req(request)

        if not correct_credentials(*creds):
            return get_wrong_creds_page()

        else:
            session["username"] = get_username(request)
            return redirect(url_for("chat"))


@application.route("/signup", methods=["GET", "POST"])
@application.route("/new-user", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        creds = get_user_creds_from_req(request)
        create_new_user(*creds)
        return get_success_page()


@application.route("/chat")
def chat():
    if user_session_exists(session):
        return render_template("chat.html", username=session["username"])
    else:
        return redirect(url_for("index"))


@application.route("/logout")
def logout():
    if user_session_exists(session):
        session.pop("username", None)

    return redirect(url_for("index"))


@socketio.on("client_message")
def emit_to_everyone(message_data):

    # message_data = {username: <username>, message: <message>}
    message = json.loads(message_data)

    usr = message['username']
    msg = message['message']

    query = f"""INSERT INTO GLOBAL
                            VALUES ('{usr}', '{msg}')"""

    # insert it into database.
    database_obj = Database()
    database_obj.execute(query)

    # close the connection
    database_obj.commit_and_close_connection()
    del database_obj

    # send "my response" back to the client.
    socketio.emit("server_response", message_data)


@socketio.on("request_for_older_messages")
def response_for_older_messages():

    database_obj = Database()
    query = """SELECT * FROM GLOBAL"""
    # execute the query to fetch the messages

    database_obj.execute(query)
    all_messages = database_obj.cursor.fetchall()
    # all_messages = (('username', 'message'), ('username', 'message'))

    database_obj.commit_and_close_connection()
    del database_obj

    json_messages = []
    # json_messages = [{username: message}, {username, message}, ...]

    # convert the tuple into dictionary
    for tup in all_messages:
            username = tup[0]
            message = tup[1]

            # encapsulate it inside dictionary.
            json_messages.append({"username": username, "message": message})

    # convert it into json string.
    json_messages = json.dumps(json_messages)

    # send the messages with a custom event
    socketio.emit("response_for_older_messages", json_messages)


if __name__ == "__main__":
    # socket created at default port = 5000
    socketio.run(application, debug=True)
