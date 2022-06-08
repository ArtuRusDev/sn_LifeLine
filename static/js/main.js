$(document).ready(function () {
    const $body = $('body');

    /*-----------------------------------------*\
       # Burger btn listener
    \*-----------------------------------------*/

    $('#burger-btn').on('click', function (e) {
        $(this).toggleClass('open');
        $('.b-left-menu').toggleClass('b-left-menu_opened');
        $('.js-left-menu-backdrop').toggleClass('b-left-menu-backdrop_active');
        $body.toggleClass('overflow-hidden');
    });

    $('.js-left-menu-backdrop').on('click', function (e) {
        $('#burger-btn').removeClass('open');
        $('.b-left-menu').removeClass('b-left-menu_opened');
        $(e.currentTarget).removeClass('b-left-menu-backdrop_active');
        $body.toggleClass('overflow-hidden');
    })

    /*-----------------------------------*\
        #Form image preview attach
    \*-----------------------------------*/

    $('.js-attach-img').on('click', function (e) {
        let $needle_input = $(e.target).parent().find('input[name="image"]');
        $needle_input.click();
    });

    $('input#id_attach_img_input').on('change', function (e) {
        let $preview_img_wrap = $('.b-preview-img');
        let file = $(e.currentTarget)[0].files[0];
        let reader = new FileReader();
        reader.onload = function (e) {
            $preview_img_wrap.find('img').attr('src', e.target.result);
        }
        reader.readAsDataURL(file);
        $preview_img_wrap.addClass('b-preview-img_filled');
    });

    $('.js-remove-preview').on('click', function (e) {
        let $preview_img = $('.b-preview-img');
        $preview_img.parent().find('input[name="image"]').val(null);
        $preview_img.removeClass('b-preview-img_filled');
    });

    /*-----------------------------------*\
        #Extra friends, communities action
    \*-----------------------------------*/

    $body.on('click', '.b-card-item__extra-actions-btn', function (e) {
        let $actions_block = $(e.currentTarget).parent().find('.b-extra-actions');
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
            $('.b-card-item[data-user]').removeClass('d-none');
        } else {
            $('.b-card-item:not(.d-none)').addClass('d-none');
            $('.b-card-item[data-type="' + $target.attr('data-val') + '"]').removeClass('d-none');
        }
    });

    /*-----------------------------------*\
        #Profile image edit
    \*-----------------------------------*/

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

    /*-----------------------------------*\
        #Ajax actions
    \*-----------------------------------*/

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
});

function subscribe_community(pk) {
    $.ajax({
        url: "/community/subscribe/" + pk + "/",

        success: function (data) {
            window.location.reload();
        }
    });
}