var CSSParentSelector = function(){
  var MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
  
  var observeElement = function(obj, callback){
    if(!MutationObserver)return;
    new MutationObserver(function(mutations, observer){
      callback(mutations[0].target);
    }).observe( obj, { childList:1, attributes:1 });
    $(obj).hover(function(e){
      var t = this;
      $(t).attr('hover', 1);
      callback(t);
    }, function(e){
      $(this).removeAttr('hover');
      callback(this);
    });
  };
  
  var updateNodeTreeSelectorList = function(root){
    var $root = $(root),
    id = $root.attr('id'),
    classs = ($root.attr('class')||'').split(' '),
    tag = root.tagName.toLowerCase(),
    has_hover = $root.attr('hover'),
    sels = ($('body').attr('contains') || '').split(','),
    sels_str = '',
    add = function(s){ s!='' && $.inArray(s, sels)==-1 && sels.push(s); };
    // add ids and classes
    if(id)add('#'+id);
    for(var x in classs){
      var clas = classs[x];
      if(clas!=''){
        add('.'+clas);
        add('#'+id+'.'+clas);
      }
    }
    // remove previous hover events
    var tmp = sels; sels = [];
    for(x in tmp){
      var match = 0;
      if(id && tmp[x].match('#'+id+':hover'))match = 1;
      for(var y in classs){
        var clas = classs[y];
        if(clas!=''){
          if(tmp[x].match('.'+clas+':hover'))match = 1;
          else if(tmp[x].match('#'+id+'.'+clas+':hover'))match = 1;
        }
      }
      if(!match)sels.push(tmp[x]);
    }
    // add current hover events
    if(has_hover){
      if(id)add('#'+id+':hover');
      for(var x in classs){
        var clas = classs[x];
        if(clas!=''){
          add('.'+clas+':hover');
          add('#'+id+'.'+clas+':hover');
        }
      }
    }
    // store
    sels_str = sels.join(',');
    $(document.body).attr('contains', sels_str);
    console.log(sels_str);
  }
  
  $(document.body).find('*').each(function(){
    observeElement(this, function(target){
      updateNodeTreeSelectorList(target);
    });
  });
}
  
  
$(function(){
  CSSParentSelector();
});