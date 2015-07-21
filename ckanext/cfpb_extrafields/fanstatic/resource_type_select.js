// this generates a warning about unsaved data from CKAN
// public/base/javascript/modules/basic-form.js
$(function() {
    $('#field-format').change( function() {
        $( "#resource_save" ).trigger( "click" );
    });
});

