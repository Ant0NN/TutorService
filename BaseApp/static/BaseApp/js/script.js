$(document).ready(function(){

	$(function() {
		$('.list li').click(function() {
			$(this).children('ul').toggle();
		});
	});

	$(function(){
        $('#id_category').change(function(){
         curselect = $('#id_category :selected').val();
         if(curselect == 2) {
         	$('.tutor').show();
         }else{
         	$('.tutor').hide();
         }
    	});
	});

	$('.bid').children('input:checkbox').click(function() {
		$(this).siblings('#bid').toggle();
	});

	var x = $('.newSubject').children('form p input');

});