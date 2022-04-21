$('body').on('click', '.b-card-item__extra-actions-btn', function (e) {
    let $actions_block = $(e.currentTarget).parent().find('.b-extra-actions');
    console.log($actions_block);
    $('.b-extra-actions:not(.d-none)').not($actions_block).addClass('d-none');

    $actions_block.toggleClass('d-none');
});

$('body').on('click', '.b-extra-actions__cancel-btn', function (e) {
    $(e.currentTarget).parent().toggleClass('d-none');
});

$('.js-card-dropdown').click(function (e) {
    $(e.currentTarget).toggleClass('opened');
});

$('.js-card-dropdowns > div').click(function (e) {
    let $target = $(e.currentTarget);
    let btn_title = $target.html();
    $('.js-card-dropdown .b-dropdown__title').html(btn_title);
    $('.b-dropdown__item.d-none').removeClass('d-none');

    $target.addClass('d-none');

    if ($target.attr('data-val') === 'all') {
        $('.b-card-item.d-none').removeClass('d-none');
    } else {
        $('.b-card-item:not(.d-none)').addClass('d-none');
        $('.b-card-item[data-type="' + $target.attr('data-val') + '"]').removeClass('d-none');
    }
});

$('body').on('click', '.js-follow-community-btn', function (e) {
    let $btn = $(e.currentTarget);
    let pk = $btn.attr('data-community-id');
    let $card_wrap = $('.b-card-item[data-community-id="' + pk + '"]').parent();

    $.ajax({
        url: "/community/subscribe/" + pk + "/",

        success: function (data) {
            if (data.result) {
                $card_wrap.html(data.result);
            }
        }
    });
});

function subscribe_community(pk) {
    $.ajax({
        url: "/community/subscribe/" + pk + "/",

        success: function (data) {
            // if (data.result) {
            //     $btn.html(data.result);
            // }
            console.log('success');
        }
    });
}