
$(window).scroll(function() {
  if($(this).scrollTop() > 50)
  {
      $('.navbar-trans').addClass('afterscroll');
  } else
  {
      $('.navbar-trans').removeClass('afterscroll');
  }  

});

// demo only 
// open link in new tab without ugly target="_blank"
$("a[href^='http']").attr("target", "_blank");

$(document).ready(function(){

  $('#itemslider').carousel({ interval: 3000 });
  
  $('.carousel-showmanymoveone .item').each(function(){
  var itemToClone = $(this);
  
  for (var i=1;i<6;i++) {
  itemToClone = itemToClone.next();
  
  if (!itemToClone.length) {
  itemToClone = $(this).siblings(':first');
  }
  
  itemToClone.children(':first-child').clone()
  .addClass("cloneditem-"+(i))
  .appendTo($(this));
  }
  });
  });
  