"use strict";

ckan.module('post_related_gist', function ($, _) {
    return {
        initialize: function () {
            $.proxyAll(this, /_on/);
            this.el.on('click', this._onClick);
        },

        _onClick: function(event) {
            var editor = ace.edit("editor_div");
            this.el.attr("disabled", "disabled");
            this.el.addClass("disabled");
            this.options.gistdesc = $('#gist-description').val();
            if (this.options.gistdesc == ''){
                var outhtml = '<h3><font color="red">Fill in description field.</font></h3>';
                $('#ace_output').html(outhtml);
                $('#gist-description').focus();
                return;
            }
            if (this.options.resource_name == true){
                // module change '' to  true so this corresponds to an unnamed resource
                this.options.resource_name = 'Unnamed'; 
            }
            var textgist = editor.getSession().getValue();
            $('#gist-loading').removeClass('hidden');
            var apiurl   = this.options.github_api_url+'gists';
            this._postGIST(apiurl,textgist, function(json) {
                if (!json) {
                    $('#ace_output').html("<h2>GitHub failed to connect</h2><br>");
                }else if (!("html_url" in json)){
                    $('#ace_output').html("<h2>GitHub post failed</h2><br>",json);
                }else {
                    this.options.gistlink = json.html_url;
                    if (!this._snippetReceived) {
                        this.sandbox.client.getTemplate(this.options.html,
                                                        this.options,
                                                        null);
                        this._snippetReceived = true;
                    }
                    window.location.reload();
                } 
            });
        },

        _postGIST: function(apiurl, basecontent, callback) {
            var mythis=this; // code review?
            var description = mythis.options.gistdesc;
            var ext = $.parseJSON($('#gistType').val());
            ext = ext.ext;
            var fp= "file."+ext;
            var filedata = {"description": description, "public": true,
                            "files": {"file" : {"filename" : fp, "content": basecontent}}}; 
            $.ajax({
                type: 'POST',
                data: JSON.stringify(filedata),
                url: apiurl,
                complete: function(xhr) {
                    callback.call(mythis, xhr.responseJSON);
                }
            }).done(function(response) {
                console.log("GitHub response:");
                console.log(response);
            });
        }
                     
    };
    
});
