function update_new_mes_counter() {

    $.ajax({
        url: "/dialogs/get/new_mes_count/",

        success: function (data) {
            if (data.result) {
                $('.new_messages_counter').html(data.result);
            }

            // console.log('ajax done');
        },

        failed: function () {
            console.log('ajax FAILED!');
        }
    });
}

setInterval(update_new_mes_counter, 2500);