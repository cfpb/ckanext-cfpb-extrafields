"use strict";

$( document ).ready(function(){
    var textarea = $('textarea[name="code"]').hide();
    
    var editor = ace.edit("editor_div");
    editor.setTheme("ace/theme/idle_fingers");
    //editor.setTheme("ace/theme/monokai");
    //editor.setTheme("ace/theme/tomorrow");
    editor.getSession().setUseWrapMode(true);
    editor.getSession().setMode("ace/mode/javascript");
    editor.getSession().setValue(textarea.val());
    editor.getSession().on('change', function(){
        textarea.val(editor.getSession().getValue());
    });
});
$('#gistType').on('change', function(){
    var editor = ace.edit("editor_div");
    var newMode = $.parseJSON($(this).val());
    console.log(newMode.name);
    editor.session.setMode("ace/mode/" + newMode.name)
});

