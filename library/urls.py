""" URL patterns for the library app """
from django.urls import path, re_path

from .views import Books, BookDetail, Uploaders, UploaderDetail


urlpatterns = [
    re_path('books/', Books.as_view(), name='books-view'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail-view'),
    path('uploaders/', Uploaders.as_view(), name='uploaders-view'),
    path('uploaders/<int:pk>/', UploaderDetail.as_view(), name='uploader-detail-view'),
]
