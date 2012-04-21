// stan 2012-02-06


// Добавляем элемент 'overlay' на страницу для отображения процессов загрузок
$(document).ready( function() {
  $("body").append('<div id="overlay">Загрузка...</div>');
});


// Настраиваем 'overlay'
jQuery( function($) {

  var overlay = $('#overlay')

  // Настраиваем вид оверлея
  overlay.css('position', 'absolute')
  overlay.css('top', '20px')
  overlay.css('left', '50%')
  overlay.css('margin-top', '-10px')
  overlay.css('margin-left', '-100px')
  overlay.css('z-index', '1001')
  overlay.css('width', '200px')
  overlay.css('text-align', 'center')
  overlay.css('display', 'none')
  overlay.css('background', '#777')
  overlay.css('color', '#FFF')

  // Биндим функции
  overlay.ajaxSend(function() {$(this).show();});
  overlay.ajaxComplete(function() {$(this).hide();});

} );

// Так и не пойму:
// почему здесь нельзя обойтись без 'jQuery( function($) {...}' ?
