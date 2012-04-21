// stan 2012-02-04

var json_url = "/j1"


// Запрашивает действие 'action' с опциями 'options'
// Полученный ответ передаёт в функцию success_callback с вызовом
function request_action(action, options, success_callback, content_type_needed, async) {
  if (typeof async == "undefined")
      async = true;

  var data_array = $.extend({action: action}, options);
  $.ajax({
    url: json_url,
    type: "GET",
    data: data_array,
    dataType: "json",
    cache: false,
    async: async,
    beforeSend: function(xhr) {
      xhr.setRequestHeader("Content-type", "application/json; charset=utf-8");
    },
    success: function(event, xhr, ajaxOptions) {
      if (typeof event.debug != "undefined")
        debug(event);

      if (typeof event.content_type == "undefined")
        debug('Нестандартный ответ!');
      else if (event.content_type == "error")
        debug('Ошибка: ' + event.content);
      else if (typeof content_type_needed != "undefined" & event.content_type != content_type_needed)
        debug('Получен ответ: "' + event.content_type + '", требуется: "' + content_type_needed + '"');
      else
        success_callback.call(this, event, xhr, ajaxOptions);
    }
  })
}


jQuery.fn.extend({


  // Запрашивает действие 'action' с опциями 'options'
  // Полученный ответ передаёт в функцию callback, возвращённое значение
  // присваивается вызываемому элементу/элементам
  put_action: function(action, options, callback, content_type_needed) {
    return this.each( function() {
	    var self = this;

      request_action(action, options, function (event, xhr, ajaxOptions) {
        content = callback.call(this, event.content, self);
        if (typeof content != "undefined")
            self.innerHTML = content
      }, content_type_needed);

    } );
  },


  put_table: function(table, columns, filter) {
    return this.each( function() {
	    var self = this;
      var jself = $(self);

      table_id = "#table";
      var filter_json = $.toJSON(filter);
      options = {table: table, limit: 100, filter_json: filter_json};
      request_action('table_view', options, function(event, xhr, ajaxOptions) {
  
        $('#filter_count').text(event.content.filter_count);
  
        var tabledata = event.content
        jself.html('');
      
        var tableisempty = true;
      
        if (typeof tabledata.thead != "undefined") {
          tableisempty = false;
          jself.append('<thead><tr>');
          tabledata.thead.forEach( function(val) {
            $("thead tr", self).append('<th>' + val + '</th>');
          } )
        }
      
        if (typeof tabledata.tbody != "undefined") {
          tableisempty = false;
          jself.append('<tbody>');
          var i = 0;
          tabledata.tbody.forEach( function(tr_vals) {
            $("tbody", self).append('<tr id="tr' + i + '">');
            tr_vals.forEach( function(val) {
              $("tbody tr#tr" + i, self).append('<td>' + val + '</td>');
            } )
            i++;
          } )
        }
      
        if (tableisempty) {
          $(table).html('Данные отсутствуют!');
          return;
        }

        jself.tablesorter({debug: true, widgets: ['zebra']});
        jself.click( function(event) {
          onTdClick(event, function(target) {
            target_tr = target.parentNode;
            $(target_tr).toggleClass('highlighted');
          } );
        });
      }, 'table');

    } );
  },


});
