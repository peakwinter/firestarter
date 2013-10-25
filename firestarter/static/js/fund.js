$(document).ready(function() {
	$(".videocol").fitVids();
	$('#rewardamtbtnusd').toggleClass('active');
	$('.rewardamtusd').show();
});

jQuery(function($){
	$('[id^="rewardamtbtn"]').click(function() {
		var currency = $(this).attr('id').slice(-3);
		$('.rewardamt').hide();
		$('[id^="rewardamtbtn"]').removeClass('active');
		$(this).toggleClass('active');
		$('.rewardamt'+currency).show();
		return false;
	});
});
