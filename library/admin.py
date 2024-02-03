from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from .models import (
    Book,
    Code,
    Folder,
    Tag,
    Uploader,
)


admin.site.site_header = 'Library Admin Panel'
admin.site.site_title = 'Demetrius'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ Tag Admin Panel """

    ordering = ['name']
    list_display = ['name', 'full_name']


@admin.register(Uploader)
class UploaderAdmin(admin.ModelAdmin):
    """ Uploader Admin Panel """

    ordering = ['username']
    list_display = ['username', 'email']


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    """ Folder Admin Panel """

    ordering = ['name']
    list_display = ['name', 'parent']
    list_filter = ('name',)
    search_fields = ['name']


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    """ Code Admin Panel """

    ordering = ['code']
    list_display = ['code', 'course']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """ Book Admin Panel """

    ordering = ['session', 'level', 'title']
    list_display = ['title', 'code', 'tag', 'uploader', 'session']
    list_filter = ('tag', 'session', 'level', 'uploader')
    search_fields = ['title', 'code__code', 'level']
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
