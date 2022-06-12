$('.js-add-comment-form').submit(function (event) {
    event.preventDefault();
    add_comment($(event.currentTarget));
});

function put_like(pk) {
    $.ajax({
        url: "/news/like/" + pk + "/",
        method: "POST",
        dataType: "json",

        success: function (data) {
            $('[data-news_pk=' + pk + ']').html(data.result);
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function add_comment($form) {
    let news_item_id = $form.parent().data('news-id');
    let $news_item = $('.js-news-item[data-news-id="' + news_item_id + '"]');

    $.ajax({
        url: "/news/add_comment/",
        method: "POST",
        data: $form.serialize(),
        dataType: "json",

        success: function (data) {
            $form.find('input[name="content"]').val('');
            $form.parent().find('.js-comments-list').html(data['comments_html']);
            $news_item.find('.js-comments-cnt').html(data['comments_cnt']);
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function delete_comment(pk) {
    $.ajax({
        url: "/news/delete_comment/" + pk + "/",
        method: "POST",
        dataType: 'json',

        success: function (data) {
            let $news_item = $('.js-news-item[data-news-id="' + data['news_id'] + '"]');
            $news_item.find('.js-comments-cnt').html(data['comments_cnt']);
            $news_item.find('.js-comments-list').html(data['comments_html']);
        },
        error: function (error) {
            console.log(error);
        }
    });
}