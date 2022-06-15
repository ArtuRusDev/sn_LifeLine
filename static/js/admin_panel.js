$('.js-moderate-news').on('click', function (e) {
    let action = e.currentTarget.getAttribute('data-action'),
        link = e.currentTarget.getAttribute('data-url');
    $.ajax({
        url: link,
        dataType: 'json',
        method: 'POST',
        data: {
            'action': action
        },

        success: function (data) {
            let pk = link.replace(/^\D+/g, '').replace('/', '');
            let $item = $('.b-news-item[data-news-id=' + pk + ']');

            if (action === 'accept') {
                $item.removeClass('b-news-item_canceled');
                $item.addClass('b-news-item_accepted');
            } else {
                $item.removeClass('b-news-item_accepted');
                $item.addClass('b-news-item_canceled');
            }
        },
        error: function (data) {
            console.log(data);
        }
    });
});