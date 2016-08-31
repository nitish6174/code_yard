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

var editor = ace.edit("editor");
editor.setTheme("ace/theme/terminal");
editor.session.setMode("ace/mode/text");
var editor = ace.edit('editor');
editor.session.setMode("ace/mode/batchfile");
editor.setTheme("ace/theme/monokai");

var input = $('#inp');

editor.getSession().on( "change", function () {
	input.val(editor.getSession().getValue());
	//console.log(input.val());
});