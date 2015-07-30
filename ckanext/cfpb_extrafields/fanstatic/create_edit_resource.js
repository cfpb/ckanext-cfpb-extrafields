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

ckan.module('create_edit_resource', function ($, _) {
    return {
        initialize: function () {
            $.proxyAll(this, /_on/);
            this.el.on('click', this._onClick);
        },
        _onClick: function(event) {
            $('#create_edit_resource').html('<span id="loader"><img src="/loader.gif" alt="loading..."></span>');
            this.sandbox.client.getTemplate(this.options.html,
                                            this.options,
                                            this._onReceiveSnippet);
        },
        _onReceiveSnippet: function(html) {
            /* check that html is an accessible url */
            var url = html;
            urlExists(url, function(exists){
                if(exists){
                    window.location.href = html
                }else{
                    alert('failure to create a resource.');
                    console.log('ckanext-cfpb failed to create a fully formed resource: '+url);
                }
            });
        },
    }
});
