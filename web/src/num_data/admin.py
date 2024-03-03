
from django.contrib import admin
from .models import ABC_files, ABC_data, Update_status


@admin.action(description='Откатить обновление')
def activate_links(modeladmin, request, queryset):
    for item in queryset:
        for item_abc_data in item.file.items.all():
            item_abc_data.delete()
        item.delete()


class Update_statusAdmin(admin.ModelAdmin):
    list_display = (
        'created_at', 'status', 'file', 'count'
    )

    list_filter = ('created_at', 'file')
    actions = [activate_links]
    verbose_name = 'Статусы обновлений'
    verbose_name_plural = 'Статус обновления'


class ABC_filesAdmin(admin.ModelAdmin):
    list_display = ('file_url', 'file_short_name',
                    'file_name', 'file', 'created_at')

    list_filter = ('created_at', 'file_short_name')
    verbose_name = 'Исходные файлы'
    verbose_name_plural = 'Исходный файл'


class ABC_dataAdmin(admin.ModelAdmin):
    list_display = ('cod', 'created_at', 'from_range',
                    'to_range', 'inn', 'operator', 'region', 'file')

    list_filter = ('created_at', 'file')
    verbose_name = 'Исходные данные'
    verbose_name_plural = 'Исходные данные'


admin.site.register(ABC_files, ABC_filesAdmin)
admin.site.register(ABC_data, ABC_dataAdmin)
admin.site.register(Update_status, Update_statusAdmin)
