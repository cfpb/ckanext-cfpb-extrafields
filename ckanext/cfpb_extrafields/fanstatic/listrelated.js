"use strict";
// now insert the data-module stuff so you can use that here instead of hidden data- stuff
// then do the filtering in javascript but maybe the loop over returned values in jinja?
ckan.module('listrelated', function ($, _) {
    return {
        initialize: function () {
            $.proxyAll(this, /_on/);
            $( document ).ready(this._onLoad);
            this.sandbox.subscribe('resources_ready');
        },

        teardown: function() {
            this.sandbox.unsubscribe('resources_ready');
        },
        _snippetReceived: false,

        _onLoad: function(event) {
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
