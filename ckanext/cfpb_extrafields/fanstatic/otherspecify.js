$(function() {
    $('select').change( function() { <!--select#type_of_entries-->
                var value = $(this).val();
                if (value == "__Other") {
                    var custom = prompt( "Please enter custom value:" );
                    if (!custom) return false;
                        <!-- clear selections -->
                        $(this).find($('option')).attr('selected',false)
                        <!-- add and select new option -->
                        $(this).prepend('<option value="' + custom + '" selected="selected">' + custom
                                        + '</option>');
                }
                                   });
});
