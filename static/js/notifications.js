const profileSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/profile/' + user_id + '/'
);

$(document).ready(function () {
    profileSocket.onmessage = function (e) {
        let data = JSON.parse(e.data);
        console.log(data);

        if (data['event'] === 'notice') {
            if (typeof chatSocket !== 'undefined' && chat_id === data['chat_id']) {
                return;
            }

            if (data['obj'] === 'message' || data['obj'] === 'friend_request') {
                if ($('.b-chats-list')[0]) {
                    update_chats();
                }

                let $notice,
                    new_id;

                if (data['obj'] === 'message') {
                    $notice = $('.js-new-msg-header-counter');
                    new_id = data['chat_id'];
                } else {
                    $notice = $('.js-new-requests-header-counter');
                    new_id = data['user_id'];
                }

                let cnt = $notice.attr('data-value'),
                    ids = $notice.attr('data-ids').split(',');

                if (ids.indexOf(new_id) !== -1) {
                    return;
                }

                ids.push(new_id);
                cnt++;

                $notice[0].innerHTML = cnt;
                $notice.attr('data-value', cnt);
                $notice.attr('data-ids', ids.join(','));
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
            dataType: 'json',
            method: 'POST',

            success: function (data) {
                if (data.result) {
                    $('.b-chats-list').html(data.result);
                }
            },
            error: function (data) {
                console.log(data);
            }
        });
    }
});