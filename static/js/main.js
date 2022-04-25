$body = $('body');
$body.on('click', '.b-card-item__extra-actions-btn', function (e) {
    let $actions_block = $(e.currentTarget).parent().find('.b-extra-actions');
    console.log($actions_block);
    $('.b-extra-actions:not(.d-none)').not($actions_block).addClass('d-none');

    $actions_block.toggleClass('d-none');
});

$body.on('click', '.b-extra-actions__cancel-btn', function (e) {
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

$body.on('click', '.js-follow-community-btn', function (e) {
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

$('.js-profile-attach-img-btn').on('click', function (e) {
    e.preventDefault();
    let $needle_input = $('.b-profile-edit-img').parent().find('input[name="avatar"]');
    $needle_input.click();
});

$('input#id_avatar').on('change', function (e) {
    let $profile_img_wrap = $('.b-profile-edit-img');
    let file = $(e.currentTarget)[0].files[0];
    let reader = new FileReader();
    reader.onload = function (e) {
        $profile_img_wrap.find('.b-profile-edit-img__img').attr('src', e.target.result);
    }
    reader.readAsDataURL(file);
    $profile_img_wrap.addClass('b-profile-edit-img_filled');
    $profile_img_wrap.parent().find('input#avatar-clear_id').prop('checked', false);
});

$('.js-profile-clear-img').on('click', function (e) {
    let $profile_img_wrap = $('.b-profile-edit-img');
    $profile_img_wrap.parent().find('input[name="avatar"]').val(null);
    $profile_img_wrap.parent().find('input#avatar-clear_id').prop('checked', true);
    $profile_img_wrap.find('.b-profile-edit-img__img').attr('src', '');
    $profile_img_wrap.removeClass('b-profile-edit-img_filled');
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