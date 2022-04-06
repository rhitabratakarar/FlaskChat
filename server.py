from flask import Flask, render_template, url_for
from flask_socketio import SocketIO
from flask import request, session, redirect
from database import Database
from dotenv import load_dotenv
import json
import os
import sqlite3


load_dotenv()
SECRET_KEY = "SECRET_KEY"
application = Flask(__name__)
application.config[SECRET_KEY] = os.getenv(SECRET_KEY)
socketio = SocketIO(application)


def user_session_exists() -> bool:
    return "username" in session


def get_user_creds_from_req(request) -> tuple:
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


def wrong_creds_page() -> str:
    return """<!DOCTYPE html>
        <html>
            <head>
                <title>Failure</title>
            </head>
            <body>
                <h1>Wrong Credentials.</h1>
                Click <a href="/login">here</a> to login again.
            </body>
        </html>
    """


def build_session_for_user(creds) -> None:
    session["username"] = creds[0]


def create_new_user(*creds) -> None:
    database = Database()
    database.create_user(creds[0], creds[1])
    print("user created")
    database.commit_and_close_connection()


def get_page(page_data) -> str:
    return f"""<!DOCTYPE html>
                <html>
                <head><title>error</title><head>
                <body><h1>{page_data}</h1></body>
                </html>
            """


@application.route("/")
@application.route("/home")
@application.route("/index")
def index():
    if user_session_exists():
        username = request.cookies.get('username')
        return redirect(url_for("chat", username=username))
    return redirect(url_for("login"))


@application.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if user_session_exists():
            username = request.cookies.get('username')
            return redirect(url_for("chat", username=username))
        return render_template("login.html")
    else:
        creds = get_user_creds_from_req(request)

        if not correct_credentials(*creds):
            return "Wrong Credentials", 401

        build_session_for_user(creds)
        return redirect(url_for("chat")), 200


@application.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        creds = get_user_creds_from_req(request)
        message = ""
        try:
            create_new_user(*creds)
        except sqlite3.IntegrityError:
            message = "Username Already Exists."
        except Exception:
            message = "Something wrong!"
        else:
            message = "You've successfully registered."
        return message


@application.route("/chat")
def chat():
    if user_session_exists():
        return render_template("chat.html", username=session["username"])
    return redirect(url_for("index"))


@application.route("/logout")
def logout():
    if user_session_exists():
        session.pop("username", None)
    return redirect(url_for("index"))


def insert_message_into_global(message_data):
    message_data = json.loads(message_data)

    database = Database()
    database.append_message_into_global(message_data['username'], message_data["message"])
    database.commit_and_close_connection()

    del database


def get_last_2nd_message_from_global() -> set:
    database = Database()
    database.execute('select * from global order by rowid desc limit 1,1')
    last_2nd_row = database.cursor.fetchone()
    database.commit_and_close_connection()
    return last_2nd_row


@socketio.on("client_message")
def emit_to_everyone(message_data):
    # message_data = "{username: <username>, message: <message>}"
    insert_message_into_global(message_data)

    last_2nd_row = get_last_2nd_message_from_global()

    if not last_2nd_row:
        json_to_send = [{"username": "", "message": ""}, json.loads(message_data)]
    else:
        json_to_send = [{"username": last_2nd_row[0], "message": last_2nd_row[1]}, json.loads(message_data)]

    socketio.emit("server_response", json.dumps(json_to_send))


def get_all_messages():
    database = Database()
    database.execute("select * from global")
    all_messages = database.cursor.fetchall()
    database.commit_and_close_connection()
    return all_messages


def get_converted_json_messages(messages) -> str:
    json_messages = []
    for tupl in messages:
        json_messages.append({"username": tupl[0], "message": tupl[1]})
    return json.dumps(json_messages)


@socketio.on("request_for_older_messages")
def response_for_older_messages():
    all_messages = get_all_messages()  # ((username, message), (username, message), ...)

    json_messages = get_converted_json_messages(all_messages)

    # send the messages with a custom event to the client.
    socketio.emit("response_for_older_messages", json_messages)


if __name__ == "__main__":
    # socket created at default port = 5000
    socketio.run(application, debug=True)
