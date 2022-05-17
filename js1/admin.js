// Interactiveness now

(function() {

	var clock = document.querySelector('digiclock');
	
	// Hay un problemilla
	// necesitamos poner un extra paea el 0-9
	// 0 a la izquierda de las horas, minutos...
	
	var pad = function(x) {
		return x < 10 ? '0'+x : x;
	};
	
	var ticktock = function() {
		var d = new Date();
		
		var h = pad( d.getHours() );
		var m = pad( d.getMinutes() );
		var s = pad( d.getSeconds() );
		
		var current_time = [h,m,s].join(':');
		
		if (clock) {
		    clock.innerHTML = current_time;
		}
		
	};
	
	ticktock();
	
	// Llamo a ticktock() casa 1 segundo
	setInterval(ticktock, 1000);
	
}());

/* ---------- Notidicaciones ---------- */
	$('.noty').click(function(e){
		e.preventDefault();
		var options = $.parseJSON($(this).attr('data-noty-options'));
		noty(options);
	});

