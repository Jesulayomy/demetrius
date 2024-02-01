""" URL patterns for the library app """
from django.urls import path, re_path

from .views import (
    Books,
    BookDetail,
    Codes,
    CodeDetail,
    Folders,
    FolderDetail,
    # FolderTree,
    Tags,
    TagDetail,
    Uploaders,
    UploaderDetail,
    view_data
)


urlpatterns = [
    path('books/', Books.as_view(), name='books-view'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail-view'),
    path('uploaders/', Uploaders.as_view(), name='uploaders-view'),
    path(
        'uploaders/<int:pk>/',
        UploaderDetail.as_view(),
        name='uploader-detail-view'
    ),
    path('tags/', Tags.as_view(), name='tags-view'),
    path('tags/<str:pk>/', TagDetail.as_view(), name='tag-detail-view'),
    path('folders/', Folders.as_view(), name='folders-view'),
    path(
        'folders/<str:pk>/',
        FolderDetail.as_view(),
        name='folder-detail-view'
    ),
    path('codes/', Codes.as_view(), name='codes-view'),
    path('codes/<str:pk>/', CodeDetail.as_view(), name='code-detail-view'),
    # path('tree/', FolderTree.as_view(), name='folder-tree-view'),
    path('view/', view_data, name='view-data')
]
