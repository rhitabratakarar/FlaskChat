$(document).ready(function () {

    const socket = io.connect("http://" + document.domain + ":" + location.port);

    socket.emit("request_for_older_messages");

    socket.on("response_for_older_messages", function (json_messages) {

        let parsed_jsons = JSON.parse(json_messages);
        /* json_messages = [
            {username: <username>, 
            message: <message>}, 
            {usern: asdfasdf, message: abcdhsd}, .....  ] */

        appendMessagesToChat(parsed_jsons);

        socket.off("response_for_older_messages");

    });

    function sendMessage() {
        var message = document.getElementById("message-box").value;

        if (message.trim() == "") {
            alert("THIS IS A CHAT APPLICATION... WRITE SOME MESSAGE, PLEASE!");
        }
        else {
            document.getElementById("message-box").value = "";

            var data = {
                username: getUsername(),
                message: message
            }
            socket.emit("client_message", JSON.stringify(data));
        }
    }

    $("#send").click(function () {
        sendMessage();
    });

    $("#message-box").on("keypress", function (e) {
        if (e.keyCode == 13)
            sendMessage();
    });

    socket.on("server_response", function (json_message) {

        var json_message = JSON.parse(json_message);

        let my_username = getUsername();

        if (my_username == json_message[1]['username']) {
            appendDivisionToChat(`<p class="send">${json_message[1]['message']}</p>`);
        }
        else {
            if (json_message[0]['username'] != json_message[1]['username']) {
                let username = json_message[1]['username'];
                let message = json_message[1]['message'];

                appendDivisionToChat(getFirstReceivingMessageParagraph(username, message));
            }
            else {
                console.log("here!");
                appendDivisionToChat(getReceivingMessageParagraph(json_message[1]['message']));
            }
        }
    });
});
