import csv
from django.core.management.base import BaseCommand
import requests
from num_data.models import ABC_files, ABC_data, Update_status
import sys
from os.path import basename
from django.core.files.base import ContentFile
from django.db.utils import DataError
from django.utils import timezone

from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Обновление базы телефонных номеров'
    # Команда вызова обновления всех таблиц кодов из Россвязи

    def handle(self, *args, **options):
        PHONEBASE_ROSSVYAZ = {
            'abc_3xx': 'https://opendata.digital.gov.ru/downloads/ABC-3xx.csv',
            'abc_4xx': 'https://opendata.digital.gov.ru/downloads/ABC-4xx.csv',
            'abc_8xx': 'https://opendata.digital.gov.ru/downloads/ABC-8xx.csv',
            'def_9xx': 'https://opendata.digital.gov.ru/downloads/DEF-9xx.csv',
        }
        sourse = PHONEBASE_ROSSVYAZ

        result_data = []

        def download_object():
            for field_name, link in sourse.items():
                try:
                    response = requests.get(
                        link, allow_redirects=True,
                        timeout=15.000, verify=False)

                    file_instance = ABC_files()
                    file_name = basename(response.url)
                    file_instance.file_url = link
                    file_instance.file_short_name = field_name
                    file_instance.file_name = file_name
                    file_instance.file.save(
                        file_name, ContentFile(response.content))

                    if response.status_code != 200:
                        print(
                            "Получение источника данных не удалось код ответа "
                            + str(response.status_code))
                        break
                    else:
                        print(
                            "Получение источника данных удалось код ответа "
                            + str(response.status_code))

                except requests.exceptions.ReadTimeout:
                    print("Превышение времени ожидания ответа")
                    sys.exit()

                except requests.exceptions.ConnectTimeout:
                    print('Соединение с интернетом отсутсвует')
                    sys.exit()

                except requests.exceptions.ConnectionError:
                    print('Соединение с интернетом отсутсвует')
                    sys.exit()

        def create_object(row, file):
            if len(row) == 8:
                model_meta = ABC_data._meta
                all_fields = model_meta.fields
                instance_object = ABC_data()
                instance_object.file = file
                for i in range(7):
                    name = all_fields[i+1].name
                    field_type = all_fields[i+1].get_internal_type()
                    value = row[i]
                    try:
                        if field_type == 'BigIntegerField' or \
                                field_type == 'IntegerField':
                            try:
                                if value.isdigit():
                                    setattr(instance_object, name, value)
                            except ValueError:
                                setattr(instance_object, name, None)
                        else:
                            setattr(instance_object, name, value)
                    except IndexError:
                        setattr(instance_object, name, None)

                result_data.append(instance_object)

        for field_name, link in sourse.items():
            try:
                objects = ABC_files.objects.filter(
                    file_short_name=field_name).latest('created_at')
                if objects:
                    if objects.created_at.date() != timezone.now().date():
                        download_object()
            except ABC_files.DoesNotExist:
                download_object()

        update_status = []

        for field_name, link in sourse.items():
            row_counter = 0
            stored_file = ABC_files.objects.filter(
                file_short_name=field_name).order_by(
                '-created_at').first()
            file_path = stored_file.file.path
            if not stored_file.items.exists():
                with open(file_path, 'r') as csvfile:
                    csv_reader = csv.reader(csvfile, delimiter=';')
                    next(csv_reader)

                    for row in csv_reader:
                        row_counter += 1
                        create_object(row, stored_file)
            update_status.append(Update_status(
                status='undeined', file=stored_file, count=row_counter))
            row_counter = 0

        try:
            if result_data:
                created_objects = ABC_data.objects.bulk_create(
                    result_data)

                if created_objects:
                    for item in update_status:
                        item.status = 'success'
                    Update_status.objects.bulk_create(
                        update_status)

        except DataError as e:
            for item in update_status:
                item.status = 'filed'
                Update_status.objects.bulk_create(
                    update_status)
            print(f"Произошла ошибка при сохранении данных: {e}")
        except IntegrityError as e:
            for item in update_status:
                item.status = 'filed'
                Update_status.objects.bulk_create(
                    update_status)
            print(f"Ошибка IntegrityError: {e}")
