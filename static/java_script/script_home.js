document.addEventListener('DOMContentLoaded', function() {
  var nav = document.querySelector('.nav');
  var navExpand = document.querySelector('.nav_expand');
  var navListItem = document.querySelectorAll('.nav_listitem');

  navExpand.addEventListener('click', function() {
    nav.classList.toggle('nav_closed');
  });
  });