"use strict";

/*
    <button data-module="example_theme_popover"
data-module-title="{{ package.title }}"
data-module-license="{{ package.license_title }}"
data-module-num_resources="{{ package.num_resources }}">
    <i class="icon-info-sign"></i>
    </button>
url
*/
    
$( document ).ready(function(){
    $('#createrelated_btn').on('click', function() {
        $('#createrelated_output').html('<div id="loader">"loading..."</div>');
        var id = $('#datasetid').data("id");
        var apiurl   = 'http://127.0.0.1:8080/api/3/action/create_related?id='+id;
        requestJSON(apiurl,function(json) {
            console.log(json);
            if(json.success == false ) {
                $('#createrelated_output').html("<h2>Failed to retrieve additional resources</h2>");
            }else {
                var relitems = json.result;
                var len = relitems.length;
                var outhtml = '<p><div class="ghcontent">'
                outhtml = outhtml + '<p>Success: '+json.success+'</div>';
                if(json.result.length)
                if(relitems.length == 0) {
                    outhtml = outhtml + '<p>No related items.</p></div>'; }
                else {
                    outhtml = outhtml + '<p><strong>Repos List:</strong></p> <ul>';
                    $.each(relitems, function(index) {
                        outhtml = outhtml + '<li><a href="'+relitems[index].url+'" target="_blank">'+relitems[index].title + '</a></li>';
                    });
                        outhtml = outhtml + '</ul></div>';
                }
                $('#createrelated_output').html(outhtml);
            } 
        }); 
    });
    function requestJSON(apiurl, callback) {
        $.ajax({
            type: 'GET',
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
        
