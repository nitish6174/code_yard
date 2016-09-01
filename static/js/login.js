$('#login_form').submit(function(e){
	e.preventDefault();
	console.log($('#login_username').val());
	console.log($('#login_password').val());
	return false;
});