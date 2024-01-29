from rest_framework import serializers

from .models import Book, Uploader


class UploaderSerializer(serializers.ModelSerializer):
    """ Serializer for Uploader model """

    class Meta:
        model = Uploader
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    """ Serializer for Book model """
    uploader = UploaderSerializer()

    class Meta:
        model = Book
        fields = "__all__"
