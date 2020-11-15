function update_chats() {

    $.ajax({
        url: "/dialogs/get/update_dialogs/",

        success: function (data) {
            if (data.result) {
                $('.chats_list').html(data.result);
            }

            console.log('ajax done');
        },

        failed: function () {
            console.log('ajax FAILED!');
        }
    });
}

setInterval(update_chats, 2500);