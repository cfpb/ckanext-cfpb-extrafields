//http://techslides.com/github-gist-api-with-curl-and-ajax
$( document ).ready(function(){
    $('#gauthsubmitbtn').on('click', function(e){
        e.preventDefault();
        $('#gauthapidata').html('<div id="loader"><img src="/loader.gif" alt="loading..."></div>');

        var urlapiauth = 'https://api.github.com/authorizations';
        var username = $('#gauthusername').val();
        var password = $('#gauthpassword').val();
        get_token(urlapiauth, username, password, function(json) {});
        
    }); // end click event handler
    
    //Get Github Authorization Token with proper scope, print to console
    function get_token(url, username, password, callback) {
        console.log(username, password);
        $.ajax({
            //url: 'https://api.github.com/authorizations',
            url: url, 
            type: 'POST',
            beforeSend: function(xhr) {
                //xhr.setRequestHeader("Authorization", "Basic " + btoa(username+":"+password));
                xhr.setRequestHeader("Authorization", "Basic " + btoa("sleitner:quepli32"));
            },
            data: '{"scopes":["gist"],"note":"ajax1 gist test for a user"}'
        }).done(function(response) {
            console.log(response);
        });
    }
    
    function create_gist(url, token, callback) {
        $.ajax({
            url: 'https://api.github.com/gists',
            type: 'POST',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", "token "+ token);
            },
            data: '{"description": "a gist for a user with token api call via ajax","public": true,"files": {"file1.txt": {"content": "String file contents via ajax"}}}'
        }).done(function(response) {
            console.log(response);
        });
    }
        
    //Using Gist ID from the response above, we edit the Gist with Ajax PATCH request
    function edit_gist(url, gistid, token, callback) {
        $.ajax({
            url: 'https://api.github.com/gists/'+gistid,
            type: 'PATCH',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", "token "+token);
            },
            data: '{"description": "updated gist via ajax","public": true,"files": {"file1.txt": {"content": "updated String file contents via ajax"}}}'
        }).done(function(response) {
            console.log(response);
        });
    }
});

