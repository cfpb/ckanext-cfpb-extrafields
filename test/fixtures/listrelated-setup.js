ckan = {
  module: function(m, cb) {
    var methods = cb(window.$);
    methods._onReceiveSnippetError({status: 'out of', statusText: 'pizza'});
    methods._onReceiveSnippet('hot dog');
  }
};
