// stan 2012-04-20


// На основе массива 'event.response' создаёт вкладки
function build_tabs(event, xhr, ajaxOptions) {
//$("body").prepend('<div id="tabs">');
  $("div#tabs").append('<ul>');
  $("div#tabs ul").append('<li style="background: #F5F5DC"><a href="#tab_db">База данных</a></li>');
  $("div#tabs ul").append('<li style="background: #F5F5DC; float: right"><a href="#tab_options">Настройки</a></li>');
  $("div#tabs").append('<div id="tab_db">');
  $("div#tab_db").append('Информация о базе данных');
  $("div#tabs").append('<div id="tab_options">');
  $("div#tab_options").append('Настройки');


  event.content.sort().forEach( function(val) {
    $('div#tabs ul').append('<li><a href="#' + val + '">' + val + '</a></li>');

    var tab_div = $('<div id="' + val + '">').appendTo('div#tabs');

  } );


  // Инициализируем
	$( 'div#tabs' ).tabs({
//  cookie: {expires: 1},   // пока не работает
		ajaxOptions: {
			error: function(xhr, status, index, anchor) {
				$(anchor.hash).html("Хм, странно! Куда подевался этот таб?...");
			}
		},
	});
}


// Обработчик выбора вкладки
function onTabsSelect(event, ui) {
  var table_id = "#table";
  var tablename = ui.tab.text;

  debug();                    // Очищаем поток
  // Objects available in the function context:
  // ui.tab     // anchor element of the selected (clicked) tab
  // ui.panel   // element, that contains the selected/clicked tab contents
  // ui.index   // zero-based index of the selected (clicked) tab
  if (ui.index > 1) {
//     $(table_id).put_table(tablename);
    options = {table: tablename, limit: 10};
    request_action('table_view', options, function(event, xhr, ajaxOptions) {
      build_table(table_id, event.content);
      $(table_id).tablesorter({debug: true, widgets: ['zebra']});
      $(table_id).click( function(event) {
        onTdClick(event, function(target) {
          target_tr = target.parentNode;
          $(target_tr).toggleClass('highlighted');
        } );
      });
    }, 'table');
  }
}


function onTdClick(event, callback) {
  event = event || window.event;
  var target = event.target || event.srcElement;
   
  while(target != this) { // ( ** )
    if (target.tagName == 'TD') { // ( * )
       callback.call(this, target);
    }
    target = target.parentNode;
  }
}


function onAClick(e) {
  var target = e && e.target || event.srcElement; // целевой элемент
  if (target.tagName != 'A')
    return;   // если не ссылка - не интересует!
  var href = target.getAttribute('href');
  alert(href); // обработать клик по элементу
  return false; // отменить переход по ссылке
}


// Построение таблицы 'table' из данных 'tabledata'
// Если 'tabledata' не задан - очищает таблицу
function build_table(table, tabledata) {
  $(table).html('');

  if (typeof tabledata == "undefined")
    return;

  var tableisempty = true;

  if (typeof tabledata.thead != "undefined") {
    tableisempty = false;
    $(table).append('<thead><tr>');
//  tr = $(table).append('<thead><tr>');
    tabledata.thead.forEach( function(val) {
      $(table + " thead tr").append('<th>' + val + '</th>');
    } )
//  $(table).append('</tr></thead>');
  }

  if (typeof tabledata.tbody != "undefined") {
    tableisempty = false;
    $(table).append('<tbody>');
    var i = 0;
    tabledata.tbody.forEach( function(tr_vals) {
      $(table + " tbody").append('<tr id="tr' + i + '">');
      tr_vals.forEach( function(val) {
        $(table + " tbody tr#tr" + i).append('<td>' + val + '</td>');
      } )
//    $(table + " tbody").append('</tr>');
      i++;
    } )
//  $(table).append('</tbody>');
  }

  if (tableisempty) {
    $(table).html('Данные отсутствуют!');
    return;
  }

  if ( tabledata.offset + tabledata.limit < tabledata.count)
    $(table).after('<a id="append_table_rows" href="#">Показать ещё записи</a>');
}
