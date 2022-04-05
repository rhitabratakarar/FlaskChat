var messages_loaded = false;

function appendDivisionToChat(division) {

  $("#chat-section-div").append(`${division}`);

  const chat_section = document.getElementById("chat-section-div");
  chat_section.scrollTop = chat_section.scrollHeight;
}

function getSendingMessageParagraph(message) {
  return `<p class='send'>${message}</p>`;
}

function getReceivingMessageParagraph(message) {
  return `<p class='receive'>${message}</p>`;
}

function getFirstReceivingMessageParagraph(username, message) {
  return `<p class='receive'><strong>${username}</strong></br>${message}</p>`;
}

function appendMessagesToChat(parsed_jsons) {
  let me = getUsername();
  let paragraph = null;
  let i = 0;

  while(i < parsed_jsons.length) {
    let currentUsername = parsed_jsons[i]['username'];

    if (me == currentUsername) {
      paragraph = getSendingMessageParagraph(parsed_jsons[i]['message']);
      appendDivisionToChat(paragraph);
    }
    else {
      let start = i;
      while (i < parsed_jsons.length && parsed_jsons[i]['username'] == currentUsername) {
        if (i == start)
          paragraph = getFirstReceivingMessageParagraph(parsed_jsons[i]['username'], parsed_jsons[i]['message']);
        else
          paragraph = getReceivingMessageParagraph(parsed_jsons[i]['message']);
          appendDivisionToChat(paragraph);
        i++;
      }
      continue;
    }
    i++;
  }
}

$("#search-icon").on('click', function () {
  $(".search").toggle();
  $(".search>input[type='text']").toggle();
});

$("#top-bar-left>.profile-icon").on('click', function () {
  $(".left>.users").toggle();
  $("#search-icon").toggle();

  if ($(".search").is(":visible")) {
    $(".search").toggle();
    $(".search>*").toggle();
  };

  $(".username").css({
    transition: 'all 1s ease-in'
  });
})
