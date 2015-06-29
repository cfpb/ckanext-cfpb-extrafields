"use strict";

ckan.module('datadict_post', function ($, _) {
  // A few jQuery helpers for exporting only
  var $EXPORT = $('#export');
  jQuery.fn.pop = [].pop;
  jQuery.fn.shift = [].shift;
  return {
    initialize: function () {
          $.proxyAll(this, /_on/);
          this.el.on('click', this._onClick);
    },
    _onClick: function(event) {
      var $rows = $TABLE.find('tr:not(:hidden)');
      var header_keys = [];
      var header_names=[]; //head
      var record = [];
      
      // Get the headers (add special header logic here)
      $($rows.shift()).find('th:not(:empty)').each(function () {
        header_keys.push($(this).text().toLowerCase());
        header_names.push($(this).text());
      });

      //header_names are the first element (and remain in an ordered array)
      record.push(header_names);
      record.push(header_keys);
      // Turn all existing rows into a loopable array
      $rows.each(function () {
        var $td = $(this).find('td');
        var h = {};
        
        // Use the header_keys from earlier to name our hash keys
        header_keys.forEach(function (header_key, i) {
          h[header_key] = $td.eq(i).text();   
        });
        
        record.push(h);
      });
      
      // Output the result
      record = JSON.stringify(record);
      $EXPORT.text(record);
      $( "input:hidden[name=datadict]" ).val(record);
    },
  }
});

    ///////////////////////


// var $BTN = $('#export-btn');
// $BTN.click(function () {
                                 



