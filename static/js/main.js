editor_codes = [ "" , "" , "" ];
current_code = "";
current_question = 1;


var editor = ace.edit('editor');
editor.session.setMode("ace/mode/python");
editor.setTheme("ace/theme/monokai");
editor.getSession().on( "change", function () {
	current_code = editor.getSession().getValue();
    $('#code').val(current_code);
});


$('#submit').click(function() {    
    console.log($('#userform').serialize()+'&which='+current_question);
    $.ajax({
                url: '/submit',
                method: 'post',
                data: $('#userform').serialize()+'&which='+current_question
            })
                    .success(function (success) {
                        alert(success);                        

                    })
                    .fail(function () {
                        alert('There was an error. Please Try Again');
                    });

});

$('#run').click(function() {
    console.log($('#userform').serialize());
	$.ajax({
                url: '/simulate',
                method: 'post',
                data: $('#userform').serialize()
            })
                    .success(function (result) {
                    	if(result[0]=='0')
                    		$('#outputConsole').removeClass('success').addClass('error');
                    	else if(result[0]=='1')
                   			$('#outputConsole').addClass('success').removeClass('error');
                        result = result.substr(1);
                        $('#outputConsole').html(result);
                        // alert(result);
                    })
                    .fail(function () {
                        alert('There was an error. Please Try Again');
                    });

});

$('#clear').click(function() {
	$("textarea").val('');
	editor.setValue(""); 
});



$('.question_select').click(function(){
	$('.question_select').removeClass('active');
	$(this).addClass('active');
	editor_codes[current_question-1] = current_code;
	current_question = ($('a',this).attr('id'))[1];
	editor.setValue(editor_codes[current_question-1]);	
    $('#code').val('');
});


$('#q1').click(function(){
$('#myModal1').modal('show');
});

$('#q2').click(function(){
$('#myModal2').modal('show');
});

$('#q3').click(function(){
$('#myModal3').modal('show');
});

$('#q4').click(function(){
$('#myModal4').modal('show');
});

$('#q5').click(function(){
$('#myModal5').modal('show');
});

$('#q6').click(function(){
$('#myModal6').modal('show');
});

