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
                let $news_item = $('.js-news-item[data-news-id="' + data['news_id'] + '"]');
                $news_item.find('.js-comments-cnt').html(data['comments_cnt']);
                $news_item.find('.js-comments-list').html(data['comments_html']);
            }
        }
    });
}


$('.js-add-comment').on('click', function (event) {
    let $form = $(event.currentTarget).parent();
    let news_item_id = $form.parent().data('news-id');
    let $news_item = $('.js-news-item[data-news-id="' + news_item_id + '"]');

    $.ajax({
        url: "/news/add_comment/",
        type: "POST",
        data: $form.serialize(),
        dataType: "html",

        success: function (data) {
            if (data) {
                $form.find('input[name="content"]').val('');
                $form.parent().find('.js-comments-list').html(JSON.parse(data)['comments_html']);
                $news_item.find('.js-comments-cnt').html(JSON.parse(data)['comments_cnt']);
            }
        }
    });
});