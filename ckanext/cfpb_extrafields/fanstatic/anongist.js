//http://blog.teamtreehouse.com/code-a-simple-github-api-webapp-using-jquery-ajax
$( document ).ready(function(){
    $('#anongistsubmitbtn').on('click', function(e){
        e.preventDefault();
        $('#anongistdata').html('<div id="loader"><img src="/loader.gif" alt="loading..."></div>');
        
        var textgist = $('#anongist').val();
        var gistenturl   = 'https://github.cfpb.gov/api/v3/gists';
        
        requestJSON(gistenturl, function(json) {
            console.log(json);
            if(json.message == "Not Found" || gistenturl == '') {
                $('#anongistdata').html("<h2>No User Info Found</h2>");
            }else {
                // else we have a user and we display their info
                var id   = json.id;
                var user   = json.user;
                // var files     = json.files;
                var ncomments = json.comments;
                var link   = json.html_url;
                
                if(user == null) { user = "null user"; }
                
                var outhtml = '<h2>'+user+'</h2>';
                outhtml = outhtml + '<div class="ghcontent"><div class="avi"><a href="'+link+'" target="_blank">'+user+'></a></div>';
                outhtml = outhtml + '<p>Comments: '+ncomments+'<br>id: '+id+'</p></div>';
                outhtml = outhtml + '<div class="repolist clearfix">';
                
                outputPageContent();    
                function outputPageContent() {
                    console.log('id lenght=0?',id.length);
                    if(id.length == 0) {
                        outhtml = outhtml + '<p>No id!</p></div>'; }
                    else {
                        outhtml = outhtml + '<p><strong>id:</strong></p> <ul>';
                        outhtml = outhtml + '</ul></div>';
                    }
                    $('#anongistdata').html(outhtml);
                } // end outputPageContent()
            } // end else statement
        }); // end requestJSON Ajax call
    }); // end click event handler
    function requestJSON(url, callback) {
        console.log('hi');
        $.ajax({
            url: url,
            type: 'POST',
            complete: function(xhr) {
                callback.call(null, xhr.responseJSON);
            },
            data: '{"description": "the description for this gist","public": true,"files": {"file.py": {"content": "def blah(x): x"}}}'
        }).done(function(response) {
            console.log("snl view response:");
            console.log(response);
        });
    }
});
