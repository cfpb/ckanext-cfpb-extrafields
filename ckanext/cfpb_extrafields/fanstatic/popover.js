"use strict";

ckan.module('popover', function ($, _) {
    return {
        initialize: function () {
            $.proxyAll(this, /_on/);
            this.el.popover({title: this.options.title, html: true,
                             content: 'Loading...', placement: 'right'});
            this.el.on('click', this._onClick);
            // Subscribe to 'dataset_popover_clicked' events.
            // Whenever any line of code publishes an event with this topic,
            // our _onPopoverClicked function will be called.
            this.sandbox.subscribe('dataset_popover_clicked',
                                   this._onPopoverClicked);
        },

        teardown: function() {
            this.sandbox.unsubscribe('dataset_popover_clicked',
                                     this._onPopoverClicked);
        },

        _snippetReceived: false,

        _onClick: function(event) {
            if (!this._snippetReceived) {
                this.sandbox.client.getTemplate(this.options.html,
                                                this.options,
                                                this._onReceiveSnippet);
                this._snippetReceived = true;
            }
            // Publish a 'dataset_popover_clicked' event for other interested
            // JavaScript modules to receive. Pass the button that was clicked as a
            // parameter to the receiver functions.
            this.sandbox.publish('dataset_popover_clicked', this.el);
        },

        // This callback function is called whenever a 'dataset_popover_clicked'
        // event is published.
        _onPopoverClicked: function(button) {
            // Wrap this in an if, because we don't want this object to respond to
            // its own 'dataset_popover_clicked' event.
            if (button != this.el) {
                // Hide this button's popover.
                // (If the popover is not currently shown anyway, this does nothing).
                this.el.popover('hide');
            }
        },

        _onReceiveSnippet: function(html) {
            this.el.popover('destroy');
            this.el.popover({title: this.options.title, html: true,
                             content: html, placement: 'right' });
            this.el.popover('show');
        },

        _onReceiveSnippetError: function(error) {
            this.el.popover('destroy');
            var content = error.status + ' ' + error.statusText + ' :(';
            this.el.popover({title: this.options.title, html: true,
                             content: content, placement: 'right'});
            this.el.popover('show');
            this._snippetReceived = true;
        },

    };
});
