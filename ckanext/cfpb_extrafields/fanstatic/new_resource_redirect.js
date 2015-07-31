"use strict";

function urlExists(url, callback){
    $.ajax({
        type: 'HEAD',
        url: url,
        success: function(){
            callback(true);
        },
        error: function() {
            callback(false);
        }
    });
}

ckan.module('new_resource_redirect', function ($, _) {
    return {
        initialize: function () {
            $.proxyAll(this, /_on/);
            this.el.on('click', this._onReady);
        },
        _onReady: function(event) {
            //$('#new_resource_redirect').html('<span id="loader"><img src="/loader.gif" alt="loading..."></span>');
            console.log('before');
            this.sandbox.client.getTemplate(this.options.html,
                                            this.options,
                                            this._onReceiveSnippet);
            console.log('after');
        },
        _onReceiveSnippet: function(html) {
            /* check that html is an accessible url */
            var url = html;
            console.log('after'+url);
            
            urlExists(url, function(exists){
                if(exists){
                    window.location.href = html
                }else{
                    alert('failure to create a resource.');
                    console.log('ckanext-cfpb failed to create a fully formed resource: '+url);
                }
            });
            console.log('how after');
        },
    }
});
