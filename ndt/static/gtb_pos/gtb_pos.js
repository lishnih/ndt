	/**
	*‘Back to top’ link using jQuery 
	* Originally written by Lloyd http://agyuku.net/2009/05/back-to-top-link-using-jquery/
	* 
	* Scroll to top or bottom
	* Changed by jen on 2011-08-22 
	*
	* Opera fix: DynamicDrive script ::jQuery Scroll to Top Control v1.1
	* http://www.dynamicdrive.com/dynamicindex3/scrolltop.htm
	*/
	
	$(function() {
		if($.browser.opera && $('div#tooltip')) $('a#toTop, a#toBottom').removeAttr('title'); // temp. toggle for Opera
		var nav = $.browser.mozilla ? 1 : 0; // Fix for Gecko, where  document.height - (window.height + window.scrollTop) == 1px
		
		if($('body').height() > $(window).height()) {
		
			if($(this).scrollTop() == 0) $('#toTop').hide();
			$(window).scroll(function() {
				if($(this).scrollTop() > 0) 
					$('#toTop').fadeIn().click(function() {
						$(this).addClass('toTop-click');
					});
				if ($(this).scrollTop() == 0) 
					$('#toTop').fadeOut().removeClass('toTop-click').click(function() {
						$(this).removeClass('toTop-click');
					});
				if(($(this).scrollTop() + $(this).height() + nav) < $(document).height()) 
					$('#toBottom').fadeIn().click(function() {
						$(this).addClass('toBottom-click');
					});
				if (($(this).scrollTop() + $(this).height() + nav) >= $(document).height()) 
					$('#toBottom').fadeOut().removeClass('toBottom-click').click(function() {
						$(this).removeClass('toBottom-click');
					});
			});
			var mode = (window.opera) ? ((document.compatMode == "CSS1Compat") ? $('html') : $('body')) : $('html,body');
			
			$('#toTop').click(function() {
				mode.animate({scrollTop:0},800);
				return false;
			});
			$('#toBottom').click(function() {
				mode.animate({scrollTop:$(document).height()},800);
				return false;
			});
		}
		else $('#gtb_pos').css('display', 'none');
	});
