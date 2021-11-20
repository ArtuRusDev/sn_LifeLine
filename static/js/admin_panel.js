function accept_news(pk) {

    $.ajax({
        url: "/admin/news/moderate/accept/" + pk + "/",

        success: function (data) {
            let $item = $('.news_item[data-news-id=' + pk + ']');
            $item.removeClass('canceled');
            $item.addClass('accepted');
        },

        failed: function () {
            console.log('ajax FAILED!');
        }
    });
}

function cancel_news(pk) {

    $.ajax({
        url: "/admin/news/moderate/cancel/" + pk + "/",

        success: function (data) {
             let $item = $('.news_item[data-news-id=' + pk + ']');
            $item.removeClass('accepted');
            $item.addClass('canceled');
        },

        failed: function () {
            console.log('ajax FAILED!');
        }
    });
}
