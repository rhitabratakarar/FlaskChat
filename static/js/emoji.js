const button = document.querySelector('#emojis');

const picker = new EmojiButton();

button.addEventListener('click', () => {
  picker.togglePicker(button);
});


picker.on('emoji', emoji => {
  document.querySelector('#message-box').value += emoji;
});