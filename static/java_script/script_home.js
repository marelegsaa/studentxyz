document.addEventListener('DOMContentLoaded', function() {
  var nav = document.querySelector('.nav');
  var navExpand = document.querySelector('.nav_expand');

  if (window.innerWidth <= 768) {
    nav.classList.remove('nav_closed');
  } else {
    navExpand.addEventListener('click', function() {
      nav.classList.toggle('nav_closed');
    });
  }
});