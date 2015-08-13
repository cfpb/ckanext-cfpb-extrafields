"use strict";

ckan.module('listrelated', function ($, _) {
    return {
        initialize: function () {
            $.proxyAll(this, /_on/);
            $( document ).ready(this._onLoad);
            // this.sandbox.subscribe('resources_ready');
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
            $('#list-gists').html(outhtml);
            $("#resource-gists .resource-gist").each(function() {
                if ($(this).data('gist-url')) {
                    // Create an iframe, append it to this document where specified
                    var gistFrame = document.createElement("iframe");
                    gistFrame.setAttribute("width", "100%");
                    gistFrame.id = "gistFrame";

                    $(this).find('.expandable_content').html(gistFrame);
                    
                    // Create the iframe's document
                    var gistFrameHTML = '<html><body style="margin:0"><scr'+'ipt type="text/javascript" src="' + $(this).data('gist-url') + '.js"></sc'+'ript></b'+'ody></h'+'tml><base target="_parent" />';

                    // Set iframe's document with a trigger for this document to adjust the height
                    var gistFrameDoc = gistFrame.document;
                    
                    
                    if (gistFrame.contentDocument) {
                        gistFrameDoc = gistFrame.contentDocument;
                    } else if (gistFrame.contentWindow) {
                        gistFrameDoc = gistFrame.contentWindow.document;
                    }
                    
                    gistFrameDoc.open();
                    gistFrameDoc.writeln(gistFrameHTML);
                    gistFrameDoc.close();
                }
            });
            jQuery('.resource-gist').expandable();
        },

        _onReceiveSnippetError: function(error) {
            var content = error.status + ' ' + error.statusText + ' :(';
            $('#listrelated_output').html(content);
            this._snippetReceived = true;
        },
    };
});
