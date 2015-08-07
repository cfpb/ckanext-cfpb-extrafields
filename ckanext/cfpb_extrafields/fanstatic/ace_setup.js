"use strict";

$( document ).ready(function(){
    var textarea = $('textarea[name="code"]').hide();
    $('#snippet-editor').hide();
    $('#btn_post_related_gist').hide();
    var editor = ace.edit("editor_div");
    //editor.setTheme("ace/theme/idle_fingers");
    //editor.setTheme("ace/theme/monokai");
    editor.setTheme("ace/theme/tomorrow");
    editor.getSession().setUseWrapMode(true);
    editor.getSession().setMode("ace/mode/javascript");
    editor.getSession().setValue(textarea.val());
    editor.getSession().on('change', function(){
        textarea.val(editor.getSession().getValue());
    });
});

$('#gist-description').on('change', function(){
    $('#editor_div').show();
    $('#btn_post_related_gist').show();
});

$('#gistType').on('change', function(){
    $('#snippet-editor').show();
    $('#btn_post_related_gist').show();
    var editor = ace.edit("editor_div");
    var newMode = $.parseJSON($(this).val());
    editor.session.setMode("ace/mode/" + newMode.name)
});

