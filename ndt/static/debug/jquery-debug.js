// stan 2012-02-06


jQuery( function($) {


  // Добавляем элемент 'debug' на страницу для вывода отладочных данных
  $("body").append('<div id="debug" style="border:1px dashed red; padding:2px">');
  $('div#debug')
    .append('<div id="menu">')
    .append('<div id="log">');

  // Добавляем меню к элементу
  $('<ul/>', {
      'class': 'menu menu_right',
      'id': 'debugmenu'
    })
    .append('<li><a href="#">Меню</a>')
    .appendTo('div#debug div#menu');

  $('<ul/>')
    .append('<li><a href="#" id="debugmenu_clearall">Очистить</a></li>')
    .append('<li><a href="#" id="debugmenu_append_something">Добавить текст</a></li>')
    .append('<li><a href="#" id="debugmenu_hide">Скрыть</a></li>')
    .appendTo('div#debug div#menu ul#debugmenu li');


  // Привязываем к 'debug' функцию ajaxError
//$('div#debug').ajaxError( function() {$(this).html("Ошибка при загрузке данных!");} );
  $('div#debug').ajaxError( function(event, xhr, ajaxOptions, thrownError) {
    if ( xhr.responseText == 'URL to recover this traceback page' )
      debug(1);
    else
      debug(xhr);
    debug('<span style="color: red">ajaxError:</span>');
  } );


  // Логика меню
  $('.menu li').hover(
    function() {
      $('ul:first', this).stop(true, true);
      $('ul:first', this).slideDown();
    },
    function() {
      $('ul:first', this).stop(true, true);
      $('ul:first', this).slideUp('slow');
    }
  );

  $('.menu li').click(
    function() {
      $('ul:first', this).stop(true, true);
      $('ul:first', this).slideUp('slow');
//    $(this).toggleClass("active");
    }
  );


  // Добавляем значки в подменю
  $(".menu li ul li:has(ul)").find("a:first").append(" &raquo; ");


  // Располагаем меню в div#debug div#menu
  $('#debugmenu')
//     .detach()
//     .prependTo('div#debug div#menu')
    .css('float', 'right')
//     .css('position', 'absolute')
//     .css('right', '120px');


  // Биндим функции к элементам меню

  $('#debugmenu_clearall').click(
    function() {
      debug();
    }
  );

  $('#debugmenu_append_something').click(
    function() {
      debug('print something...');
    }
  );

  $('#debugmenu_hide').click(
    function() {
      $('div#debug').hide();
    }
  );

} );


// Вывод отладочных данных
// Очищает поток, если вызвать без параметра 'message'
function debug(message) {
  if (typeof message == "undefined") {
//  $('div#debug').hide();
    $('div#debug div#log').html('');
  } else {
    message = var_dump1(message);
    $('<div/>').html(message).prependTo('div#debug div#log');
//  $("div#debug").scrollTop(0);
//  $('div#debug').show();
  }
}
