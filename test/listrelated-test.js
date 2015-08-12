var jsdom = require('jsdom');
var fs = require('fs');
var expect = require('expect.js');

describe('list related module', function () {

  var $;

  beforeEach(function(done) {
    jsdom.env({
      file: __dirname + '/fixtures/listrelated.html',
      scripts: ['http://code.jquery.com/jquery.js', __dirname + '/fixtures/listrelated-setup.js', __dirname + '/../ckanext/cfpb_extrafields/fanstatic/listrelated.js'],
      done: function(err, window) {
        $ = window.$;
        done();
      }
    });
  })

  it('should insert snippet into the DOM', function () {
    expect($('#list-gists').html()).to.be('hot dog');
  });

  it('should have expandables', function () {
    expect($('.expandable_content').length).to.be(3);
  });

  it('should inject gist iframes into the DOM', function () {
    expect($('iframe').length).to.be(3);
  });

  it('should gracefully handle snippet errors', function () {
    expect($('#listrelated_output').html()).to.be('out of pizza :(');
  });

});
