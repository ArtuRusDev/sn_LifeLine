$('button[name="send_comment"]').on('click', function (event) {
    let $form = $(event.currentTarget).parent();

    $.ajax({
        url: "/news/add_comment/",
        type: "POST",
        data: $form.serialize(),
        dataType: "html",

        success: function (data) {
            $form.find('input[name="content"]').val('');
            $form.parent().find('.comments-list').html(JSON.parse(data)['result']);
        },

        failed: function () {
            console.log('ajax FAILED!');
        }
    });
});

function delete_comment(pk) {
     let like_el = $('[data-news_pk=' + pk + ']');
    console.log(like_el);

    $.ajax({
        url: "/news/like/" + pk + "/",

        success: function (data) {
            if (data.result) {
                $('[data-news_pk=' + pk + ']').html(data.result);
            }
        },

        failed: function () {
            console.log('ajax FAILED!');
        }
    });
}