"use strict";
// now insert the data-module stuff so you can use that here instead of hidden data- stuff
// then do the filtering in javascript but maybe the loop over returned values in jinja?
ckan.module('listrelated', function ($, _) {
    return {
        initialize: function () {
            console.log('snl here!2');
            $.proxyAll(this, /_on/);
            $( document ).ready(this._onLoad);
            this.sandbox.subscribe('resources_ready');
                                   
            console.log('snl here!1');
        },

        teardown: function() {
            this.sandbox.unsubscribe('resources_ready');
        },
        _snippetReceived: false,

        _onLoad: function(event) {
            console.log('snl here!0');
            /*
            $('#listrelated_output').html('<div id="loader">"loading..."</div>');
            var dataset_id = $('#datasetid').data("dataset_id");
            var resource_id = $('#datasetid').data("resource_id");
            var apiurl   = 'http://127.0.0.1:8080/api/3/action/related_list?id='+dataset_id;
            $.getJSON(apiurl, function(json) {
                console.log(json);
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
            */

            this.options.newthing='123'
            
            if (!this._snippetReceived) {
                this.sandbox.client.getTemplate(this.options.html,
                                                this.options,
                                                this._onReceiveSnippet);
                this._snippetReceived = true;
            }
            // Publish a 'resources_ready' event for other interested
            // JavaScript modules to receive. 
            this.sandbox.publish('resources_ready');
        },

        _onReceiveSnippet: function(outhtml) {
            $('#listrelated_output').html(outhtml);
        },

        _onReceiveSnippetError: function(error) {
            var content = error.status + ' ' + error.statusText + ' :(';
            $('#listrelated_output').html(content);
            this._snippetReceived = true;
        },
    };
});
            
        
