// stan 2012-04-20


function build_tabs(tabs_id, table_id) {
  var tabs = $(tabs_id);

  var sys_tabs = 2;   // 2 системные вкладки ("База данных" и "Настройки")

  // Инициализируем вкладки
  var ul = $('<ul>');
  ul.append('<li style="background: #F5F5DC"><a href="#tab_db">База данных</a></li>');
  ul.append('<li style="background: #F5F5DC; float: right"><a href="#tab_options">Настройки</a></li>');
  tabs
    .append(ul)
    .append('<div id="tab_db">Информация о базе данных</div>')
    .append('<div id="tab_options">Настройки</div>');


  var tables = [];          // Cписок таблиц

  // Инициализируем вкладки для таблиц
  tabs.put_action('tables_list', '', function append_tabs(event, self) {
    var tabs = $(self);
    var ul = $('ul', self);
  
    var i = sys_tabs;
    event.rows.sort().forEach( function(val) {
      val2 = val.replace('.', '_');
      ul.append('<li><input class="append_table" type="checkbox" value="' + val + '"><a href="#' + val2 + '">' + val2 + '</a></li>');
      tabs.append('<div id="' + val2 + '">' + val + '</div>');
      tables[i] = val;
      i++;
    } );


    $('.append_table').change( function() {
      var selected_tables = [];   // Выбранные таблицы

      $(".append_table:checked").each( function () {
        selected_tables.push(this.value);
      } );

      if ( selected_tables )
        $(table_id).put_datatable(selected_tables.join('|'));
    } );


    // Инициализируем (именно после цикла event.rows)
  	tabs.tabs({
  		ajaxOptions: {
  			error: function(xhr, status, index, anchor) {
  				$(anchor.hash).text("Хм, странно! Куда подевался этот таб?...");
  			}
  		},
  	});
  } );


  // Биндим
  tabs.bind('tabsselect', function (event, ui) {
    // Objects available in the function context:
    // ui.tab     // anchor element of the selected (clicked) tab
    // ui.panel   // element, that contains the selected/clicked tab contents
    // ui.index   // zero-based index of the selected (clicked) tab

//     debug();      // Очищаем поток

    // При выборе новой вкладки сбрасываем все checkbox'ы
    $(".append_table").attr('checked', false);

    // Загружаем данные из таблицы
    if (ui.index >= sys_tabs) {
      $(".append_table").eq(ui.index - sys_tabs).attr('checked', true);
      $(table_id).put_datatable(tables[ui.index]);
    } else
      $(table_id).html('');
  } );
}
