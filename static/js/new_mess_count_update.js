function update_new_mes_counter() {

    $.ajax({
        url: "/dialogs/get/new_mes_count/",

        success: function (data) {
            if (data.result) {
                let $counter = $('.js-new-msg-header-counter');
                $counter.html(data.result);
                $counter.removeClass('d-none');
            }
        },

        failed: function () {
            console.log('ajax FAILED!');
        }
    });
}

// setInterval(update_new_mes_counter, 2500);