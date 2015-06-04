"use strict";

$( document ).ready(function(){
    var editor = ace.edit("editor_div");
    /*<script src="src/theme-xcode.js" type="text/javascript" charset="utf-8"></script> //snl: theme needs to be included */
    editor.setTheme("ace/theme/XCode");
    editor.getSession().setMode("ace/mode/javascript"); //snl: this should be chosen in some massive case statement
    /* 
    <script src="mode-xml.js" type="text/javascript" charset="utf-8"></script>
    var XmlMode = require("ace/mode/xml").Mode;
    editor.getSession().setMode(new XmlMode());
    */
    
   var textarea = $('textarea[name="editor"]');
//   textarea.hide();
    $('#acesubmitbtn').on('click', function() {
        var textgist = editor.getSession().getValue();
        textarea.val(textgist);
        $('#ace_output').html('<div id="loader"><img src="/loader.gif" alt="loading..."></div>');
        var apiurl   = 'https://github.cfpb.gov/api/v3/gists';
        requestJSON(apiurl,textgist, function(json) {
            console.log("response json:",json);
            if(json.message == "Not Found" || apiurl == '') {
                $('#ace_output').html("<h2>No User Info Found</h2>");
            }else {
                var id   = json.id;
                var user   = json.user;
                if(user == null) { user = "null user"; }
                var ncomments = json.comments;
                var link   = json.html_url;
                var outhtml = '<p><div class="ghcontent"><h3><a href="'+link+'"><h2>link to new gist</a></h3>'; 
                outhtml = outhtml + '<p>Comments: '+ncomments+'<br>id: '+id+'</p></div>';
                $('#ace_output').html(outhtml);
            } // end else statement
        }); // end requestJSON Ajax call
    }); // end click event handler
    function requestJSON(apiurl, basecontent, callback) {
        console.log('snl content: '+basecontent);
        var description = 'the description for this gist';
        var filedata = {"description": description, "public": true,
                        "files": {"file.py": {"content": basecontent}}};
        $.ajax({
            type: 'POST',
            data: JSON.stringify(filedata),
            url: apiurl,
            complete: function(xhr) {
                callback.call(null, xhr.responseJSON);
            }
        }).done(function(response) {
            console.log("snl view response:");
            console.log(response);
        });
    }
});
        
