## Определяем информацию(регион, оператор) по номеру телефона

Веб-приложение позволяет получить информацию по оператору на основании номера, приложение позволяет обовить базу номеров и откатить обновление на предыдущую дату обновления. 

### Реестр российской системы и плана нумерации
https://opendata.digital.gov.ru/registry/numeric/downloads/
![alt text](web/src/num_data/static/num_data/num_lookup.png)

### Стек  
Django  
Vue.js  
Postgres  
Docker

### Описание настроек
В файле проекта `/num_data/management/commands/update_phone_base.py` в опции `PHONEBASE_ROSSVYAZ`
установлены адреса источника данных в виде ссылки на загружаемый документ, формате csv для последуюшего импорта в postgres

### Периодическое обновление данных
Обновление реализовано через вызов management команды django в каталоге проекта: ` python manage.py update_phone_base`  
Проект поддерживает возможность отката к предыдущей дате обновления, данная опция доступна в административном интерфейсе Django

### Скрипт API расположен по адресу
`http://localhost:80/api/v1/info`

Пример ответа:
```json
{
    "number": [
        {
            "number": "89600586532",
            "cod": 960,
            "from_range": 300000,
            "to_range": 899999,
            "capacity_range": 600000,
            "operator": "ПАО \"ВЫМПЕЛКОМ\"",
            "region": "Республика Татарстан"
        }
    ]
}
```
### Запуск проекта в среде Docker
В дирректории с проектом выполнить команду `docker-compose up`  
Команда запуска получения данных из Реестр российской системы и плана нумерации  `docker-compose exec WEB python3 manage.py update_phone_base`




