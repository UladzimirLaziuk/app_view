# app_view
Тестовое задание Python.

Нужно сделать загрузку данных со сторонего сервера в БД, доступ к ним через rest сервис, админка для редактирования категорий с загрузкой картинок.


БД проектируется испытуемым.
Аутентификация на сервере:


Программы складываем в БД с определенной периодичностью (добавление а далее обновление).

Из программы важно, название, детали акций (action details), картинка, категории (вложенность не важна, важен сам набор категорий), URL для покупок (gotolink) и главный фид продуктов (products_xml_link).


В продуктах важно — название, модель, цена, картинки, УРЛ для покупки.--------------------------я нашел только vendor -вместо модели поставил-



Загружаем магазины и продукты с определенной периодичностью (она задается к конфиге).

Делаем рест сервис для получения магазинов из нашей БД. Постраничный.
И делаем поиск — возвращает найденные товары (ищем по модели и названию) из нашей БД. Результаты возвращаем постранично.

Делаем админку (со входом — логины для входа просто храним в БД — управление ими не входит в тестовое задание) —
в админке делаем редактирование списка категорий (по факту название и картинка).------------------Совсем не понял))


И делаем рест для получения этих категорий.
********************************************************************************************************************

Не хватило времени на деталирование действий и ответов таких как:
- обновление токенов
-интерфейс задание перодичности загрузки магазинов(сам функционал записи и получения xml даннах реализован)
-не реализовано -редактирование списка категорий (по факту название и картинка) в админке - по причине-не понял задачу.
Реализация без (Elasticsearch, django-sphinxsearch), хотя судя по данным они там нужны))
