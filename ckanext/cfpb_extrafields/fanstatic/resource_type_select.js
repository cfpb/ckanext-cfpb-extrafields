// this generates a warning about unsaved data from CKAN
// public/base/javascript/modules/basic-form.js
$(function() {
    $('#field-resource_type').change( function() {
        var rtype = $('#field-resource_type').val();
        if(      rtype == 'Data Dictionary'){
            $( "#resource_save" ).trigger( "click" );
        }else if(rtype == 'Report'){ 
            $( "#resource_save" ).trigger( "click" );
        }else if(rtype == 'Documentation'){ 
            $( "#resource_save" ).trigger( "click" );
        }else if(rtype == 'Data File'){ 
            $( "#resource_save" ).trigger( "click" );
        }else if(rtype == 'Database'){
            $( "#resource_save" ).trigger( "click" );
        }else{
        }
    });
});
