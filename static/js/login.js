$('#login_form').submit(function(e){
	e.preventDefault();
	login_username = $('#login_username').val();
	login_password = $('#login_password').val();

	$.post('/login',{
		username : login_username,
		password : login_password
	},function(data){
		window.location = data;
	});

	return false;
});