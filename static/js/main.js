editor_codes = [ "" , "" , "" , "" ];
current_code = "";
current_question = 1;


var editor = ace.edit('editor');
editor.session.setMode("ace/mode/python");
editor.setTheme("ace/theme/monokai");
editor.getSession().on( "change", function () {
	current_code = editor.getSession().getValue();
});


$('#submit').click(function() {
	$.ajax({
                url: '',
                method: 'post',
                data: $('#userform').serialize()
            })
                    .success(function () {
                        alert('Reload for change to reflect.');
                        // location.reload();

                    })
                    .fail(function () {
                        alert('There was an error. Please Try Again');
                    });

});

$('#run').click(function() {
	$.ajax({
                url: '',
                method: 'post',
                data: $('#userform').serialize()
            })
                    .success(function (result) {
                        alert(result+'\nReload for change to reflect.');
                        // location.reload();

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
