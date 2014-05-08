$(document).ready(function(){

	var count = 0;

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


	$(function() {
		$('.newSubject').each(function() {
			$(this).find('p input').each(function() {
				var name = $(this).attr('name');
				$(this).attr('name', name + count);
			});

			count++;

		});
	});

	$("#registration").validate({
		rules: {
			username: {
				required: true,
				minlength: 4
			},
			password: {
				required: true,
			},
			confirm_password: {
				required: true,
				equalTo: "password"
			},
			email: {
				required: true,
				email: true
			},
			city: {
				required: true,
			},
			experience: {
				digits: true
			}
		},

		messages: {
			username: {
				required: "Это поле обязательно для заполнения",
				minlength: "Минимум 4 символа"
			}
		}
	});

});