$(document).ready(function () {
    const profileSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/profile/' + user_id + '/'
    );

    profileSocket.onmessage = function (e) {
        let data = JSON.parse(e.data);

        if (data['event'] === 'notice') {
            if (typeof chatSocket !== 'undefined' && chat_id === data['chat_id']) {
                return;
            }

            if (data['obj'] === 'message') {
                if ($('.b-chats-list')[0]) {
                    update_chats();
                }

                let $notice = $('.js-new-msg-header-counter'),
                    cnt = $notice.attr('data-value'),
                    unread_chats = $notice.attr('data-chats').split(',');

                if (unread_chats.indexOf(data['chat_id']) !== -1) {
                    return;
                }

                unread_chats.push(data['chat_id']);
                cnt++;

                $notice[0].innerHTML = cnt;
                $notice.attr('data-value', cnt);
                $notice.attr('data-chats', unread_chats.join(','));
                $notice.removeClass('d-none');
            }
        }
    };

    profileSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    function update_chats() {
        $.ajax({
            url: "/dialogs/get/update_dialogs/",

            success: function (data) {
                if (data.result) {
                    $('.b-chats-list').html(data.result);
                }
            },

            failed: function () {
                console.log('ajax FAILED!');
            }
        });
    }
});