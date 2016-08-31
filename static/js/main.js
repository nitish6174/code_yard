editor_codes = [ "" , "" , "" , "" ];
current_code = "";
current_question = 1;


// var editor = ace.edit("editor");
// editor.setTheme("ace/theme/terminal");
// editor.session.setMode("ace/mode/text");
var editor = ace.edit('editor');
editor.session.setMode("ace/mode/batchfile");
editor.setTheme("ace/theme/monokai");
editor.getSession().on( "change", function () {
	current_code = editor.getSession().getValue();
	// console.log(input.val());
});



$('#compile').click(function() {
	var textarea_value = $("#inp").val();
	if(textarea_value=='') {
		alert("Enter Some Text In Textarea");
	}else{
		alert(textarea_value);
	}
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



// function getset(pactive, pnew)
// {
// 	pactive=input
// 	input=pnew
// }