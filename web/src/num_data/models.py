from django.db import models


class ABC_files(models.Model):
    file_url = models.CharField(blank=True, default=None, null=True,
                                max_length=1000, verbose_name='Url')
    file_short_name = models.CharField(blank=True, default=None, null=True,
                                       max_length=1000,
                                       verbose_name='Короткое наименование')
    file_name = models.CharField(blank=True, default=None, null=True,
                                 max_length=1000, verbose_name='Имя файла')
    file = models.FileField(
        verbose_name='Содержимое файла', upload_to="downloads")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Исходные файлы'
        verbose_name_plural = 'Исходный файл'

    def __str__(self):
        return self.file_name


class Update_status(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Создано')
    status = models.CharField(blank=True, default=None, null=True,
                              max_length=1000, verbose_name='Url')
    file = models.ForeignKey(ABC_files, on_delete=models.CASCADE,
                             related_name='by_file', verbose_name='Файл')
    count = models.IntegerField(
        blank=True, default=None, null=True, verbose_name='Количество записей')

    class Meta:
        verbose_name = 'Статусы обновлений'
        verbose_name_plural = 'Статусы обновлений'


class ABC_data(models.Model):
    cod = models.IntegerField(blank=True, default=None,
                              null=True, verbose_name='Код оператора')
    from_range = models.IntegerField(
        blank=True, default=None, null=True, verbose_name='Начало диапазона')
    to_range = models.IntegerField(
        blank=True, default=None, null=True, verbose_name='Конец дианазона')
    capacity_range = models.IntegerField(
        blank=True, default=None, null=True, verbose_name='Номерная емкость')
    operator = models.CharField(blank=True, default=None, null=True,
                                max_length=1000,
                                verbose_name='Наименование оператора')
    region = models.CharField(blank=True, default=None, null=True,
                              max_length=1000,
                              verbose_name='Регион присутствия')
    inn = models.BigIntegerField(blank=True, default=None,
                                 null=True, verbose_name='ИНН')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Создано')

    file = models.ForeignKey(ABC_files, on_delete=models.CASCADE, null=True,
                             blank=True,
                             related_name='items', verbose_name='Файл')

    class Meta:
        indexes = [
            models.Index(fields=['cod', 'from_range', 'to_range'])
        ]
        verbose_name = 'Содержимое CSV'
        verbose_name_plural = 'Содержимое CSV'
