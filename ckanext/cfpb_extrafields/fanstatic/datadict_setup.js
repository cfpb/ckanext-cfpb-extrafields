//create an html table from json in Datastore
$( document ).ready(function(){
    //first get the json if it exists in the data store 
    // {{ h.get_datastore(data.id) }}
    // then convert it to HTML
    // http://www.jqueryscript.net/table/jQuery-Plugin-For-Converting-JSON-Data-To-A-Table-jsonTable.html
    // https://github.com/omkarkhair/jsonTable
    //innerhtml -> textarea
    var textarea = $('textarea[name="oldjson"]').hide();    
    //$("#example-table").jsonTableUpdate(textarea.val());
    console.log('ready');
});

//manipulate the html table using whatever magic datatables and onchanges


// Now convert html table back to json and post it to datastore through an html template
// delete the original first? or upsert.
$('#convert-table').click( function() {
  //var table = $('#example-table').tableToJSON(); // Convert the table into a javascript object
  //console.log(table);
  //alert(JSON.stringify(table));
  alert('submitting new table... are you sure you want to replace?');
});
// http://lightswitch05.github.io/table-to-json/
// Ansible https://github.com/lightswitch05/table-to-json
/*
Install Node.js.
this will also the npm package manager.
run npm install from app root directory.
This installs grunt and other dependencies See package.json for a full list.
run npm install -g grunt-cli.
run grunt to run tests and create a new build in /lib.
*/
