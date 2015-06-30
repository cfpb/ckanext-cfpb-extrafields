"use strict";

$( document ).ready(function(){
  var text = _makeTextFile($('#dsn_box').val());
  $('#downloadlink').prop("href",text);
});

var textFile = null;
function _makeTextFile(text) {
  var data = new Blob([text], {type: 'text/plain'});
  // If we are replacing a previously generated file we need to
  // manually revoke the object URL to avoid memory leaks.
  if (textFile !== null) {
    window.URL.revokeObjectURL(textFile);
  }
  textFile = window.URL.createObjectURL(data);
  return textFile;
};