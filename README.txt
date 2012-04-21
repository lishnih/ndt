NDT README
==================

  Данный скрипт является pyramid-приложением (веб-сервер).
  Позволяет в масштабах небольшого отдела/нескольких отделов организовывать
  доступ к заданным базам данных нескольких пользователей.
  Имеет простой инструментарий для фильтровки, сортировки записей в БД.
  Есть экспорт в pdf (русский не поддерживаетя), csv, вывод на печать.

  Скрипт является развитием проекта http://sourceforge.net/projects/phpndt/,
  осуществлён переход на python, сделан упор на использование сторонних
  библиотек, благо, в python'е это дело организовано получше ))

  Также как и phpndt, пакет ndt лишь позволяет работать с данными,
  сами же базы набивает данными скрипт index
  (ранее http://sourceforge.net/projects/pyndt/).

  Пакет создан на основе примера alchemy из пакета pyramid.
  Также wiki создан из соответствующего примера в pyramid.

Запуск
==================

  1. Установите скрипт setup.py install
  2. Произведите инициализацию баз данных
     - ndt/scripts/initializedb.py
     - ndt/wiki/scripts/initializedb.py
  3. Запустите сервер pserve development.ini

Принцип работы
==================

  Работает веб-сервер и принимает запросы через адреса вида
  "/j1", "/j2", где цифра - версия протокола данных.
  Сами html-страницы статические, данные из них запрашиваются
  последством ajax запросов.

Дистрибутивы
==================

  В пакет включены следующие дистрибутивы:

  jquery 1.7.1, jquery-ui 1.8.17 и jquery-themeswitcher
  http://jqueryui.com/
  http://jqueryui.com/themeroller/themeswitchertool/

  jQuery.json 2.3
  http://code.google.com/p/jquery-json/

  jquery.form
  http://jquery.malsup.com/form/

  jquery.tablesorter 2.0.5
  http://tablesorter.com/

  DataTables-1.9.0
  http://datatables.net/

  gtb_pos
  http://jenweb.info/page/plugin-gotopbottom-for-maxsite

  Меню для отладки - солянка из двух пакетов, плюс, статьи в инете:
  SimplejQueryDropdowns http://css-tricks.com/simple-jquery-dropdowns/
  JSDDM 0.25 http://javascript-array.com/scripts/jquery_simple_drop_down_menu/
  http://anton.shevchuk.name/javascript/jquery-for-beginners-2/

  Вообще, спасибо всем, чьи статьи помогли мне при создании данного пакета!
