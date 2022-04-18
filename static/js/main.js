$('.b-friend-item__extra-actions-btn').click(function (e) {
    let $actions_block = $(e.currentTarget).parent().find('.b-extra-actions');
    console.log($actions_block);
    $('.b-extra-actions:not(.d-none)').not($actions_block).addClass('d-none');

    $actions_block.toggleClass('d-none');
});

$('.b-extra-actions__cancel-btn').click(function (e) {
    $(e.currentTarget).parent().toggleClass('d-none');
});

$('.js-friends-dropdown').click(function (e) {
    $(e.currentTarget).toggleClass('opened');
});

$('.js-friends-dropdowns > div').click(function (e) {
    let $target = $(e.currentTarget);
    let btn_title = $target.html();
    $('.js-friends-dropdown .b-dropdown__title').html(btn_title);
    $('.b-dropdown__item.d-none').removeClass('d-none');

    $target.addClass('d-none');

    $('.js-usr-cat:not(.d-none)').addClass('d-none');
    $('.js-usr-cat[data-id="' + $target.attr('data-val') + '"]').removeClass('d-none');
});

