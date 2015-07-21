// this generates a warning about unsaved data from CKAN
// public/base/javascript/modules/basic-form.js
$(function() {
    $('#field-resource_type').change( function() {
        $( "#resource_save" ).trigger( "click" );
    });
});

