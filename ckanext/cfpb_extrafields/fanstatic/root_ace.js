"use strict";

$( document ).ready(function(){
    var editor = ace.edit("editor_div");
    /*<script src="src/theme-xcode.js" type="text/javascript" charset="utf-8"></script> //snl: theme needs to be included */
    editor.setTheme("ace/theme/XCode");
    //snl: this should be chosen in some massive case statement
    editor.getSession().setMode("ace/mode/javascript"); 
});
        
