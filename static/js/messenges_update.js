function update_messages() {
    let chat_pk = $('input[name="chat_pk"]').val();

    $.ajax({
        url: "/dialogs/get_messages/" + chat_pk + "/",

        success: function (data) {

            if (data.result) {
                $('.b-chat__content__messages').html(data.result);
                $(".js-chat-block")[0].scrollTop = 9999;
            }

            console.log('ajax done');
        },

        failed: function () {
            console.log('ajax FAILED!');
        }
    });
}

setInterval(update_messages, 1000);