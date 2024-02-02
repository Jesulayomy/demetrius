from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from .models import Book, Code, Uploader, Tag, Folder


admin.site.site_header = 'Library Admin Panel'
admin.site.site_title = 'Demetrius'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'full_name']


@admin.register(Uploader)
class UploaderAdmin(admin.ModelAdmin):
    ordering = ['username']
    list_display = ['username', 'email']


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'parent']
    list_filter = ('name',)
    search_fields = ['name']


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    ordering = ['code']
    list_display = ['code', 'course']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    ordering = ['session', 'level', 'title']
    list_display = ['title', 'code', 'tag', 'uploader', 'session']
    list_filter = ('tag', 'session', 'level', 'uploader')
    search_fields = ['title', 'code', 'level']
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
