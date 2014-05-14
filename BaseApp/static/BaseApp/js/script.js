$(document).ready(function(){

	var count = 0;
	var push = false;
	var pushTwo = false;
	var pushThree = false;

	$(function() {
		$('.list li').click(function() {
			$(this).children('ul').toggle();
		});

		$('.center .person .about').each(function() {
			$(this).children('.subject:eq(0)').css('display', 'block');
		});
	});

	$(function(){
        $('#id_category').change(function(){

         curselect = $('#id_category :selected').val();

         if(curselect == 2) {

         	$('.tutor').show();

         	$('#id_name').rules('add' , {
         		required: true,
         		regex: '^[а-яА-ЯёЁa-zA-Z][а-яА-ЯёЁa-zA-Z]{1,}[а-яА-ЯёЁa-zA-Z]$',
         		messages: {
         			required: ' Необходимо указать имя',
         			regex: ' Введите корректное имя'
         		}
         	});

         	$('#id_patronymic').rules('add', {
         		required: true,
         		messages: {
         			required: 'Введите отчество'
         		}
         	});

         	$('#id_experience').rules('add', {
         			required: true,
         			digits: true,
         			messages: {
         				required: ' Необходимо указать стаж',
         				digits: ' Только цифры'
         			}
         	});
         	$('#id_education').rules('add', {
         		required: true,
         		messages: {
         			required: ' Необходимо указать образование'
         		}
         	});
         	$('#id_work').rules('add', {
         		required: true,
         		messages: {
         			required: ' Необходимо указать место работы'
         		}
         	});
         	$('#id_venue_of').rules('add', {
         		required: true,
         		messages: {
         			required: ' Необходимо указать место проведения занятий'
         		}
         	});
         	$('#id_subject_name').rules('add', {
         		required: true,
         		messages: {
         			required: ' Выберете предмет из списка'
         		}
         	});
         	$('#id_price').rules('add', {
         		required: true,
         		messages: {
         			required: ' Необходимо указать цену занятий'
         		}
         	});
         	$('#id_pupil_category').rules('add', {
         		required: true, 
         		messages: {
         			required: ' Необходимо указать категорию ученика'
         		}
         	});
         	$('#id_section').rules('add', {
         		required: true,
         		messages: {
         			required: ' Необходимо выбрать раздел'
         		}
         	});

         }else{

         	$('.tutor').hide();

         	$('#id_name').rules('remove');
         	$('#id_patronymic').rules('remove');
         	$('#id_experience').rules('remove');
         	$('#id_education').rules('remove');
         	$('#id_work').rules('remove');
         	$('#id_venue_of').rules('remove');
         	$('#id_subject_name').rules('remove');
         	$('#id_price').rules('remove');
         	$('#id_pupil_category').rules('remove');
         	$('#id_section').rules('remove');

         }

    	});
	});

	$(function() {
		$('#id_section').change(function() {

			curselect = $('#id_section :selected').val();

			if(curselect != 1) {
				
				$('#id_subject_name').show();

				if(curselect == 'Основные предметы') {
					$('#id_subject_name .firstSelect').css('display', 'inline');
					$('#id_subject_name .secondSelect').css('display', 'none');
					$('#id_subject_name .thirdSelect').css('display', 'none');
				}else if(curselect == 'Иностранные языки') {
					$('#id_subject_name .firstSelect').css('display', 'none');
					$('#id_subject_name .secondSelect').css('display', 'inline');
					$('#id_subject_name .thirdSelect').css('display', 'none');
				}else if(curselect == 'Предметы высшей школы') {
					$('#id_subject_name .firstSelect').css('display', 'none');
					$('#id_subject_name .secondSelect').css('display', 'none');
					$('#id_subject_name .thirdSelect').css('display', 'inline');
				}

			} else {
				$('#id_subject_name').hide();
			}

			console.log(curselect);
		});
	})

	$(function() {
		$('.list li .circle:eq(1)').css('border', '2px solid #02b8ea');
		$('.list li .circle:eq(2)').css('border', '2px solid #78be74');
	});


	$('.list').each(function() {
		
		$(this).children('li:eq(0)').click(function() {
			if(push == false) {
				$(this).children('.circle').css('background', '#e7694f');
				push = true;
			} else {
				$(this).children('.circle').css('background', 'none');
				push = false;
			}
		});

		$(this).children('li:eq(1)').click(function() {
			if(pushTwo == false) {
				$(this).children('.circle').css('background', '#02b8ea');
				pushTwo = true;
			} else {
				$(this).children('.circle').css('background', 'none');
				pushTwo = false;
			}
		});

		$(this).children('li:eq(2)').click(function() {
			if(pushThree == false) {
				$(this).children('.circle').css('background', '#78be74');
				pushThree = true;
			} else {
				$(this).children('.circle').css('background', 'none');
				pushThree = false;
			}
		});

	});

	$('.bid').each(function() {
		$(this).find('#img').click(function() {
			$(this).siblings('.fix').children('.formToBid').css('display', 'block');
		});
		$(this).find('.formToBid .btn').click(function() {
			$(this).parent('.formToBid').css('display', 'none');
		});
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

	$.validator.addMethod("valueNotEquals", function(value, element, arg){
 		 return arg != value;
 	}, "Выберете категорию");

 	$.validator.addMethod("regex", function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        }, "Введите корректное значение");

	$("#registration").validate({
				rules: {
					username: {
						required: true,
						minlength: 4,
						maxlength: 50,
					},
					password: {
						required: true,
						rangelength: [8, 30],
					},
					confirm_password: {
						required: true,
						equalTo: "#id_password"
					},
					email: {
						required: true,
						email: true
					},
					city: {
						required: true,
						regex: '^[а-яА-ЯёЁa-zA-Z][A-Za-zА-Яа-я\\s\\\(\\\-]{1,30}[A-Za-zА-Яа-я\\\)]$'
					},
					category: {
						valueNotEquals: 1
					}
				},
				messages: {
						username:{
							required: " Необходимо выбрать логин",
							minlength: " Логин слишком короткий",
							maxlength: " Логин слишком длинный"
						},
						password: {
							required: " Необходимо выбрать пароль",
							rangelength: " Пароль должен состоять из 8-30 символов"
						},
						confirm_password: {
							required: " Пожалуйста, введите пароль еще раз",
							equalTo: " Пароли не совпадают"
						},
						email: {
							required: " Необходимо указать email",
							email: " Некорректный email"
						},
						city: {
							required: " Необходимо указать город проживания"
						}
					}
			});

	
		$('.center .person').each(function() {
			$(this).find('#sendBid').click(function() {

				var first = $(this).parent('#bid').find('#id_first_name');
				var last = $(this).parent('#bid').find('#id_last_name');
				var category = $(this).parent('#bid').find('#id_category :selected');
				var number = $(this).parent('#bid').find('#id_number_telephone');
				var email = $(this).parent('#bid').find('input[name=to_email]');

				$.ajax({
					url: '/repetito.ru/my%20account/homepage/statement',
					type: 'POST',
					dataType: 'html',
					data: {
						'first_name': first.val(),
						'last_name' : last.val(),
						'category' : category.val(),
						'number_telephone' : number.val(),
						'to_email' : email.val(),
					},
					error: function() {
						console.log('error');
					},
					success: function() {
						console.log('send');
					},
					// CSRF механизм защиты Django
		            beforeSend: function(xhr, settings) {
		                function getCookie(name) {
		                    var cookieValue = null;
		                    if (document.cookie && document.cookie != '') {
		                        var cookies = document.cookie.split(';');
		                        for (var i = 0; i < cookies.length; i++) {
		                            var cookie = jQuery.trim(cookies[i]);
		                            // Does this cookie string begin with the name we want?
			                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
			                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
			                            break;
			                        }
		                    	}
		                	}
		                	return cookieValue;
		                }
		                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
		                    // Only send the token to relative URLs i.e. locally.
		                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
		                }
        			}
				});

				first.val('');
				last.val('');
				number.val('');
				$(this).parent('#bid').parent('.formToBid').css('display', 'none');

			});
		});

});