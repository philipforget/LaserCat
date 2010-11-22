$(function(){
	var $control = $('#control'),
		offset_x = Math.floor($control.offset().left),
		offset_y = Math.floor($control.offset().top);

	$(window).scroll(function(){
		offset_x = Math.floor($control.offset().left);
		offset_y = Math.floor($control.offset().top);
	});

	$control.mousemove(function(event){
		$.post('/ajax/update/',
			{
				'x': ( event.pageX - offset_x) / $control.height(),
				'y':  (event.pageY - offset_y) / $control.width(),
			},
			function(data){
			}
		)
	})
});
