$(function(){
	var $control = $('#control'),
		offset_x = Math.floor($control.offset().left),
		offset_y = Math.floor($control.offset().top),
		laser_state;

	$.get('/laser/', state_handler)

	$(window).scroll(function(){
		offset_x = Math.floor($control.offset().left);
		offset_y = Math.floor($control.offset().top);
	});

	$control.mousemove(function(event){
		if(laser_state){
			$.post('/ajax/update/',
				{
					'x': ( event.pageX - offset_x) / $control.height(),
					'y':  (event.pageY - offset_y) / $control.width(),
				},
				function(data){
				}
			)
		}
	}).click(function(event){
		$.post('/toggle/', state_handler)
	});

	function state_handler(data){
		laser_state = data.state;
		$control.toggleClass('active', laser_state);
	}
});
