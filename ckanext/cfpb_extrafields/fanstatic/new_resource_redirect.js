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

function redirect(html) {
    var url = html;    
    urlExists(url, function(exists){
        if (exists) {
            window.location.href = html
        } else {
            alert('failure to create a resource.');
            console.log('ckanext-cfpb failed to create a fully formed resource: '+url);
        }
    });
}

ckan.module('new_resource_redirect', function ($, _) {
    return {
        initialize: function () {
            $.proxyAll(this, /_on/);
            if (window.location.pathname.indexOf('new_resource') > -1) {
                this.sandbox.client.getTemplate(this.options.html,
                                                this.options,
                                                redirect);
            }
        }
    }
});
