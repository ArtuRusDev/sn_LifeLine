function put_like(pk) {
    $.ajax({
        url: "/news/like/" + pk + "/",

        success: function (data) {
            if (data.result) {
                $('[data-news_pk=' + pk + ']').html(data.result);
            }
        }
    });
}

function delete_comment(pk) {
    $.ajax({
        url: "/news/delete_comment/" + pk + "/",

        success: function (data) {
            if (data) {
                let $news_item = $('.news_item[data-news-id="' + data['news_id'] + '"]');
                $news_item.find('.comments_block span').html(data['comments_cnt']);
                $news_item.find('.comments_wrap').html(data['comments_html']);
            }
        }
    });
}


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
        }
    });
});