function update_messages () {
    let chat_pk = $('input[name="chat_pk"]').val();

    $.ajax({
        url: "/dialogs/get_messages/" + chat_pk + "/",

        success: function (data) {
            $('.messages_block').html(data.result);
            console.log('ajax done');
        },

        failed: function () {
            console.log('ajax FAILED!');
        }
    });

    var block = document.getElementById("chat_block");
    block.scrollTop = 9999;
}

setInterval(update_messages, 1000);