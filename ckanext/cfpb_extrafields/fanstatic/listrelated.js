"use strict";

$( document ).ready(function(){
//    $('#listrelated_btn').on('click', function() {
        $('#listrelated_output').html('<div id="loader">"loading..."</div>');
        var dataset_id = $('#datasetid').data("dataset_id");
        var resource_id = $('#datasetid').data("resource_id");
        var apiurl   = 'http://127.0.0.1:8080/api/3/action/related_list?id='+dataset_id;
        $.getJSON(apiurl, function(json) {
            if(json.success == false ) {
                $('#listrelated_output').html("<h2>Failed to retrieve additional resources</h2>");
            }else {
                var relitems = json.result;
                var len = relitems.length;
                var outhtml = '<p><div class="ghcontent">'
                outhtml = outhtml + '<p>Success: '+json.success+'</div>';
                if(relitems.length == 0) {
                    outhtml = outhtml + '<p>No related items.</p></div>'; }
                else {
                    outhtml = outhtml + '<p><strong>Repos List:</strong></p> <ul>';
                    $.each(relitems, function(index) {
                        var desc = relitems[index].description;
                        if(desc != null && desc.indexOf(resource_id) >= 0) {
                            outhtml = outhtml + '<li><a href="'+relitems[index].url+'" target="_blank">'+relitems[index].title + '</a></li>';
                        }
                    });
                        outhtml = outhtml + '</ul></div>';
                }
                $('#listrelated_output').html(outhtml);
            } 
        }); 
//    });
});
        
