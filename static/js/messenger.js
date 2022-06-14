let chat = document.getElementsByClassName("js-chat-block")[0];
chat.scrollTop = chat.scrollHeight;

let chatSocket = new ReconnectingWebSocket(
    'ws://' + window.location.host + '/ws/chat/' + chat_id + '/');

chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data),
        event = data['event'];

    console.log(data);

    if (event === 'new_msg') {
        process_message(data);
    } else if (event === 'read' && data['user_id'] !== user_id) {
        $('.b-msg-item.b-msg-item_unread').removeClass('b-msg-item_unread');
    }
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

function process_message(data) {
    let is_own_class = '',
        is_read_class = '',
        is_img = '';

    if (data['author_id'] === user_id) {
        is_own_class = 'current_user';
        is_read_class = "b-msg-item_unread";
    } else {
        chatSocket.send(JSON.stringify({
            'action': 'read',
            'chat_id': chat_id
        }));
    }

    if (data['image']) {
        is_img = '' +
            '<a href="' + data['image'] + '" data-fancybox class="b-msg-item__img-link">' +
            '   <img src="' + data['image'] + '" class="b-msg-item__img" loading="lazy">' +
            '</a>';
    }

    let msg = '' +
        '<div class="b-msg-item-wrap ' + is_own_class + '">' +
        '   <div style="background-image: url(' + data['author_img'] + ')" class="b-msg-item__avatar"></div>' +
        '   <div class="b-msg-item ' + is_read_class + '">' +
        '       <div class="b-msg-item__username">' + data['author_name'] + '</div>' +
        '       <div class="b-msg-item__username__content">' +
        '           <span class="b-msg-item__text">' + data['message'] + '</span>' +
        '           <span class="b-msg-item__time">' + data['time'] + '</span>' +
        '       </div>' + is_img +
        '   </div>' +
        '</div>';

    $('.b-chat__content__messages')[0].innerHTML += msg;
    $(".js-chat-block")[0].scrollTop = 9999;
}

document.querySelector('.b-chat__form').addEventListener('submit', function (e) {
    e.preventDefault();

    let messageInputDom = document.querySelector('.b-form__input');
    let inputFile = document.querySelector('.b-chat__form input[name="image"]');
    let message = messageInputDom.value;
    let file = inputFile.files[0];

    if (!message && !file) {
        return;
    }

    let date = new Date();
    if (file) {
        let reader = new FileReader();
        let image;

        reader.onload = function (e) {
            chatSocket.send(JSON.stringify({
                'action': 'message',
                'message': message,
                'time': date.getHours() + ':' + (date.getMinutes() < 10 ? '0' : '') + date.getMinutes(),
                'author_id': user_id,
                'author_name': user_name,
                'author_img': user_img,
                'members': chat_members,
                'image': e.target.result
            }));
        }

        reader.readAsDataURL(file);
    } else {
        chatSocket.send(JSON.stringify({
            'action': 'message',
            'message': message,
            'time': date.getHours() + ':' + (date.getMinutes() < 10 ? '0' : '') + date.getMinutes(),
            'author_id': user_id,
            'author_name': user_name,
            'author_img': user_img,
            'members': chat_members,
            'image': false
        }));
    }

    $('.b-chat__content__no-msg').addClass('d-none');

    let $preview_img = $('.b-preview-img');
    $preview_img.parent().find('input[name="image"]').val(null);
    $preview_img.removeClass('b-preview-img_filled');

    messageInputDom.value = '';
});