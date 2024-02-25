""" URL patterns for the library app """
from django.urls import path, re_path

from .views import (
    Books,
    BookDetail,
    Codes,
    CodeDetail,
    CodeBooks,
    Folders,
    FolderDetail,
    Tags,
    TagDetail,
    Uploaders,
    UploaderDetail,
)


urlpatterns = [
    path(
        'books/',
        Books.as_view(),
        name='books'
    ),
    path(
        'books/<int:pk>/',
        BookDetail.as_view(),
        name='book-detail'
    ),
    path(
        'uploaders/',
        Uploaders.as_view(),
        name='uploaders'
    ),
    path(
        'uploaders/<int:pk>/',
        UploaderDetail.as_view(),
        name='uploader-detail'
    ),
    path(
        'tags/',
        Tags.as_view(),
        name='tags'
    ),
    path(
        'tags/<str:pk>/',
        TagDetail.as_view(),
        name='tag-detail'
    ),
    path(
        'folders/',
        Folders.as_view(),
        name='folders'
    ),
    path(
        'folders/<int:pk>/',
        FolderDetail.as_view(),
        name='folder-detail'
    ),
    path(
        'codes/',
        Codes.as_view(),
        name='codes'
    ),
    path(
        'codes/<str:pk>/',
        CodeDetail.as_view(),
        name='code-detail'
    ),
    path(
        'codes/<str:pk>/books/',
        CodeBooks.as_view(), name='code-books'
    ),
]
