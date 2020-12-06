function put_like(pk) {

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
