var jsdom = require('jsdom');
var fs = require('fs');
var expect = require('expect.js');

describe('data dictionary', function () {

  var $;

  beforeEach(function (done) {
    jsdom.env({
      file: __dirname + '/fixtures/datadict.html',
      scripts: ['http://code.jquery.com/jquery.js', __dirname + '/../ckanext/cfpb_extrafields/fanstatic/datadict_setup.js'],
      done: function(err, window) {
        $ = window.$;
        done();
      }
    });
  })

  it('should render', function () {
    expect($('#datadict-table').length).to.be(1);
  });

  it('should add rows', function () {
    $('.table-add').trigger('click');
    expect($('tr').length).to.be(5);
  });

  it('should remove rows', function() {
    expect($('#cheeseburger')).to.not.be.empty();
    $('.table-remove').trigger('click');
    expect($('#cheeseburger')).to.be.empty();
  });

  it('should move rows up', function() {
    expect($('.lunch').length).to.be(2);
    expect($($('.lunch')[1]).attr('id')).to.be('french-fries');
    $('#french-fries .table-up').trigger('click');
    expect($($('.lunch')[1]).attr('id')).to.be('cheeseburger');
  });

  it('should move rows down', function() {
    expect($('.lunch').length).to.be(2);
    expect($($('.lunch')[0]).attr('id')).to.be('cheeseburger');
    $('#cheeseburger .table-down').trigger('click');
    expect($($('.lunch')[1]).attr('id')).to.be('cheeseburger');
  });

})
