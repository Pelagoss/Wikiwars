var image;
$(document).ready(function() {
	(function($) {
		$.fn.wiki_tooltip = function(settings) {
			// Settings to configure the jQuery lightBox plugin how you like
			settings = jQuery.extend({
			wiki_lang : 'fr',
			in_delay : 0,
			out_delay : 0,
			in_speed : 500,
			out_speed : 500
			},settings);
		 var tooltip = $('<div class="mwe-popups mwe-popups-type-page mwe-popups-fade-in-up mwe-popups-no-image-pointer mwe-popups-is-not-tall" aria-hidden="" style="left: 534px; top: auto; bottom: -94px; display: block;height:fit-content;z-index:4000"></div>');
		$('body').append(tooltip);
		$(".popups_hover").hover(function(m){
		$(".mwe-popups").html("");
		$(".mwe-popups").css('display','none');
		$(".mwe-popups").css('opacity','1');
		var _t = m.pageY + 10;
		var _l = m.pageX - 15;

		tooltip.css({ 'top':_t, 'left':_l });
		  title = $(this).attr('title');
		  var namePage = title.toString();
		  $(this).attr('title',"");
		  title = title.replace(' ','_');
		  if (title.length){
			var x;
			if(x) {x = null; x.abort(); }
			 x = $.ajax({
			 url: 'https://'+settings.wiki_lang+'.wikipedia.org/api/rest_v1/page/summary/'+namePage+'?redirect=true',
			 async:false,
			success: function(data) {
			console.log(data);
			  $('.mwe-popups').html('<div class="mwe-popups-container">\n' +
				  '    <span class="mwe-popups-extract" href="/wiki/'+title+'" dir="ltr" lang="fr">'+ data.extract +'</span>\n' +
				  '</div>');
			  $(".mwe-popups").stop(true, true).delay(settings.in_delay).fadeIn(settings.in_speed);

			}
		  });
		  }
		},
		function(){
			$(this).attr('title',title);
			$(".mwe-popups").clearQueue();
			$(".mwe-popups").stop();
			$(".mwe-popups").delay(settings.out_delay).fadeOut(settings.out_speed);

			});
		}
	})(jQuery);

	$(document).ready(function(){
		$('body').find('a:not(.logout), span.target_page, span.started_page').attr('class','popups_hover');

    	$('.popups_hover').wiki_tooltip();
    });
});