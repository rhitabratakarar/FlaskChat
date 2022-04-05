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

    $('#logout').click(function () {
        var confirmation = confirm("You want to logout?");

        if (confirmation)
            window.location.href = "/logout";
    });

    $("#send").click(function () {

        var message = document.getElementById("message-box").value;

        document.getElementById("message-box").value = "";

        var data = {
            username: getUsername(),
            message: message
        }
        socket.emit("client_message", JSON.stringify(data));
    });


    socket.on("server_response", function (json_message) {
        var json_message = JSON.parse(json_message);

        appendDivisionToChat(`<p class="send">${json_message['message']}</p>`);
    });
});
