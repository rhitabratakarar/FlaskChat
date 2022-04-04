var messages_loaded = false;

function appendDivisionToChat(division) {

    $("#chat-section-div").append(`${division}`);

    const chat_section = document.getElementById("chat-section-div");
    chat_section.scrollTop = chat_section.scrollHeight;
}

let message = function(message) {
    return `<div class='message'>${message}</div>`
}

let first_message = function(username, message) {
    return `<div class='message'><p>${username}</p>${message}</div>`
}

let mine_messages = function(arr) {
    let mine_message = `<div class='mine messages'>`;

    arr.forEach(function(div) {
        mine_message = mine_message + div;
    });

    mine_message = mine_message + "</div>";
    return mine_message;
}

let your_messages = function(arr) {
    let your_message = `<div class='yours messages'>`;
    
    arr.forEach(function(div) {
        your_message = your_message + "</div>";
    });

    your_message = your_message + "</div>";
    return your_message;
}

function appendMessagesToChat(parsed_jsons) {
    let me = "{{username}}";
    let prev_username = parsed_jsons[0]['username'];
    let arr = [];
    let count = 0;


    for(let i = 1; i < parsed_jsons.length; i++) {
        let curr_username = parsed_jsons[i]['username'];
        
        if(prev_username == curr_username) {
            count = count + 1;
            if(count == 1)
                arr.push(first_message(parsed_jsons[i-1]['username'], parsed_jsons[i-1]['message']));
            else 
                arr.push(message(parsed_jsons[i-1]['message']))
        }
        else {
            count = 0;
            arr.push(message[parsed_jsons[i-1]['message']]);
            let message_divs = "";

            if(prev_username == me) 
                message_divs = mine_messages(arr);
            else 
                message_divs = your_messages(arr);

            appendDivisionToChat(message_divs);
        }
        prev_username = curr_username;
    }
}