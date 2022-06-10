document.addEventListener("DOMContentLoaded", function(event) {
	let $input = $('.b-search-wrap .b-search-input');
	let $items = $('.b-card-item');
	let is_chat = false;

	if ($items.length === 0) {
		$items = $('.b-chat-item');
		is_chat = true;
	}

	$input.on('input', function (e) {
		let val = e.currentTarget.value.toLowerCase();

		if (!val) {
			$items.each(function (idx) {
				this.style.display = 'flex';
			});
			return;
		}

		$items.each(function (idx) {
			let content = '';

			if (is_chat) {
				content = $(this).find('.b-chat-item__content')[0].innerHTML;
			} else {
				content = $(this).find('.b-card-item__username')[0].innerHTML;
			}

			if (content.toLowerCase().indexOf(val) !== -1) {
				this.style.display = 'flex';
			} else {
				this.style.display = 'none';
			}
		});
	});
});