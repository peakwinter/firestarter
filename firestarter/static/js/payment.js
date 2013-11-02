var paymentType = window.location.pathname.replace('/', '').slice(-2).toLowerCase();
var currencyType = 'usd';

$(document).ready(function() {
	if ($('input[id^=ctype]:checked').length == 0 && paymentType != 'bc') {
		changeCurrency('usd');
		$('#ctype-usd').prop('checked', true)
	} else if (paymentType != 'bc') {
		var active = $('input[id^=ctype]:checked').attr('id').split('-')[1];
		changeCurrency(active);
		$('#ctype-'+active).prop('checked', true)
	};
	$('#submitbutton').prop('disabled', false);
	$('#submitbutton').html('Next <i class="icon-arrow-right"></i>');
});

var updatePrice = function(row) {
	if (paymentType == 'bc' && (parseFloat($('#amount').val()) < parseFloat($(row).children('.price').text().split(' ')[1]) || !($('#amount').val()))) {
		$('#amount').val(parseFloat($(row).children('.price').text().split(' ')[1]));
	} else if (paymentType != 'bc' && (!($('#amount').val()) || parseFloat($('#amount').val()) < parseFloat($(row).find('.rewardamt'+currencyType).text().split(' ')[1]))) {
		$('#amount').val(parseFloat($(row).find('.rewardamt'+currencyType).text().split(' ')[1]).toFixed(2));
	};
};

var changeCurrency = function(currency) {
	$('[class^="rewardamt"]').hide();
	$('#currency-icon').attr('class', 'icon-'+currency);
	$('#amount').prop('placeholder', currency.toUpperCase())
	if (currency == 'usd') {
		$('.currency-symbol').text('$');
	} else if (currency == 'eur') {
		$('.currency-symbol').text('€');
	} else if (currency == 'gbp') {
		$('.currency-symbol').text('₤');
	};
	$('.rewardamt'+currency).show();
	currencyType = currency;
};

var stripeResponseHandler = function(status, response) {
	var $form = $('#payform');

	if (response.error) {
		// Show the errors on the form
		$('#validate').text(response.error.message);
		$('#validate').attr('class', 'alert alert-danger');
		$('#validate').show();
		$('html').scrollTop(0);
		$('#submitbutton').html('Next <i class="icon-arrow-right"></i>');
		$('#submitbutton').prop('disabled', false);
	} else {
		// token contains id, last4, and card type
		var token = response.id;
		// Insert the token into the form so it gets submitted to the server
		$form.append($('<input type="hidden" name="stripeToken" />').val(token));
		$form.append($('<input type="hidden" name="ctype" />').val(currencyType));
		$form.append($('<input type="hidden" name="cc_type" />').val(response.card.type));
		$form.append($('<input type="hidden" name="cc_last4" />').val(response.card.last4));
		// and submit
		$('#submitbutton').prop('disabled', false);
		$form.get(0).submit();
	};
};

jQuery(function($){
	// Restrict payment details to proper formats
	if (paymentType == 'cc') {
		$('#cc-number').payment('formatCardNumber');
		$('#cc-exp').payment('formatCardExpiry');
		$('#cc-cvc').payment('formatCardCVC');
	};

	if (paymentType != 'bc') {
		// Change the currency via clicks from form div
		$('.ctypes').click(function() {
			$(this).children('input').prop('checked', true);
			changeCurrency($(this).find('input').attr('id').split('-')[1]);
		});

		// Change the currency via clicks from radio button
		$('input[id^=ctype]').change(function() {
			changeCurrency($(this).attr('id').split('-')[1]);
		});
	};

	// Allow checking radio buttons by clicking the parent table row
	// Also show/hide the shipping form if reward is claimed or not
	//   via clicks from table row
	$('[id^="rewardslist"] tr').click(function() {
		$(this).find('[id^=rsel]').prop('checked', true);
		if ($(this).find('input').attr('id').slice(-1) == '0') {
			$('#sh-form').hide();
		} else {
			$('#sh-form').show();
		};
		updatePrice(this);
	});

	// Show/hide the shipping form if reward is claimed or not
	//   via clicks from radio button
	$('input[id^=rsel]').change(function() {
		if (!($(this).attr('id').endsWith('0'))) {
			$('#sh-form').show();
		} else {
			$('#sh-form').hide();
		};
		updatePrice($(this).closest('tr'));
	});

	// On attempted form submit
	$('#submitbutton').click(function(){
		$('.form-group').removeClass('has-error');
		$('#rewards-grp').removeClass('text-danger');
		$('#validate').hide();

		// Validate payment info
		var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
		$('#donate-grp').toggleClass('has-error', !($('#amount').val()) || $('#amount').val() == 0 || isNaN($('#amount').val()));
		if (paymentType == 'bc') {
			$('#rewards-grp').toggleClass('text-danger', !($('[id^=rsel]').is(':checked')));
			$('#ref-grp').toggleClass('has-error', !($('#ref').val()));
			$('#email-grp').toggleClass('has-error', !($('#email').val()) || !emailReg.test($('#email').val()));
		} else if (paymentType == 'pp') {
			$('#rewards-grp').toggleClass('text-danger', !($('[id^=rsel]').is(':checked')));
		} else {
			var cardType = $.payment.cardType($('#cc-number').val());
			$('#rewards-grp').toggleClass('text-danger', !($('[id^=rsel]').is(':checked')));
			$('#cc-name-grp').toggleClass('has-error', !($('#cc-name').val()));
			$('#cc-email-grp').toggleClass('has-error', !($('#email').val()) || !emailReg.test($('#email').val()));
			$('#cc-num-grp').toggleClass('has-error', !$.payment.validateCardNumber($('#cc-number').val()));
			$('#cc-exp-grp').toggleClass('has-error', !$.payment.validateCardExpiry($('#cc-exp').payment('cardExpiryVal')));
			$('#cc-cvc-grp').toggleClass('has-error', !$.payment.validateCardCVC($('#cc-cvc').val(), cardType));
		};

		// Validate shipping info if reward is claimed, and check if the
		//    price entered is high enough for the selected reward
		if (!($('[id^=rsel][id$=0]').is(':checked'))) {
			$('#sh-name-grp').toggleClass('has-error', !($('#sh-name').val()));
			$('#sh-addr1-grp').toggleClass('has-error', !($('#sh-addr1').val()));
			$('#sh-city-grp').toggleClass('has-error', !($('#sh-city').val()));
			$('#sh-state-grp').toggleClass('has-error', !($('#sh-state').val()));
			$('#sh-post-grp').toggleClass('has-error', !($('#sh-post').val()));
			$('#sh-country-grp').toggleClass('has-error', !($('#sh-country').val()));
			if (paymentType == 'bc' && parseFloat($('#amount').val()) < parseFloat($('input[id^="rsel"]:checked').closest('tr').children('.price').text().split(' ')[1])) {
				$('#rewards-grp').toggleClass('text-danger', !($('#rewards-grp').hasClass('text-danger')));
			} else if (paymentType != 'bc' && parseInt($('#amount').val()) < parseInt($('input[id^="rsel"]:checked').closest('tr').find('.rewardamt'+currencyType).text().split(' ')[1])) {
				$('#rewards-grp').toggleClass('text-danger', !($('#rewards-grp').hasClass('text-danger')));
			};
		};

		// If validation fails anywhere, show an error, else create token and proceed
		if ($('input').parent('.has-error').length || $('#rewards-grp').hasClass('text-danger').length) {
			$('#validate').text('There was an error in processing this information. Please verify that the fields in red below are correct.')
			$('#validate').attr('class', 'alert alert-danger');
			$('#validate').show();
			$('html').scrollTop(0);
		} else if (paymentType == 'bc') {
			$('#payform').get(0).submit();
			return false;
		} else if (paymentType == 'pp') {
			$('#payform').append($('<input type="hidden" name="ctype" />').val(currencyType));
			$('#payform').get(0).submit();
			$('#submitbutton').prop('disabled', true);
			$('#submitbutton').html('<i class="icon-spinner icon-spin"></i> Verifying...');
			return false;
		} else {
			// Disable the submit button to prevent repeated clicks
			$('#submitbutton').prop('disabled', true);
			$('#submitbutton').html('<i class="icon-spinner icon-spin"></i> Verifying...');

			Stripe.card.createToken({
				name: $('#cc-name').val(),
				number: $('#cc-number').val(),
				cvc: $('#cc-cvc').val(),
				exp_month: parseInt($('#cc-exp').val().split('/')[0]),
				exp_year: parseInt($('#cc-exp').val().split('/')[1])
			}, stripeResponseHandler);

			// Prevent the form from submitting with the default action
			return false;
		}
	});
});