from rest_framework import serializers

from .models import (
    Book,
    Code,
    Folder,
    Tag,
    Uploader,
)


class CodeSerializer(serializers.ModelSerializer):
    """ Serializer for Code model """

    class Meta:
        model = Code
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for Tag model """

    class Meta:
        model = Tag
        fields = "__all__"


class FolderSerializer(serializers.ModelSerializer):
    """ Serializer for Folder model """

    class Meta:
        model = Folder
        fields = "__all__"


class UploaderSerializer(serializers.Serializer):
    """ Serializer for Uploader model """
    username =  serializers.CharField(max_length=64)
    email = serializers.EmailField(max_length=255)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        """ Creates a new user with the validated data """
        user, created = Uploader.objects.get_or_create(validated_data["username"])
        if created:
            user.email = validated_data.get("email", None)
            user.save()
        return user

    def update(self, instance, validated_data):
        """ Updates an exsting user instance """
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance


class BookSerializer(serializers.ModelSerializer):
    """ Serializer for Book model """
    uploader = UploaderSerializer(required=False)

    class Meta:
        model = Book
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        """ Creates a new book with the validated data """
        user_data = validated_data.pop("uploader")
        user, created = Uploader.objects.get_or_create(username=user_data["username"])
        if created:
            user.email = user_data.get("email", None)
            user.save()
        book = Book.objects.create(uploader=user, **validated_data)
        return book

    def update(self, instance, validated_data):
        """ Updates an exsting book instance """
        instance.title = validated_data.get("title", instance.title)
        instance.level = validated_data.get("level", instance.level)
        instance.size = validated_data.get("size", instance.size)
        instance.tag = validated_data.get("tag", instance.tag)
        instance.code = validated_data.get("code", instance.code)
        instance.session = validated_data.get("session", instance.session)
        instance.downloads = validated_data.get(
            "downloads",
            instance.downloads
        )
        instance.description = validated_data.get(
            "description",
            instance.description
        )
        instance.download = validated_data.get("download", instance.download)
        instance.drive_id = validated_data.get("drive_id", instance.drive_id)
        instance.parents = validated_data.get("parents", instance.parents)
        uploader = validated_data.get("uploader", None)
        if uploader:
            user, created = Uploader.objects.get_or_create(
                username=uploader["username"]
            )
            if created:
                user.email = uploader.get("email", None)
            else:
                user.email = uploader.get("email", user.email)
            user.save()
            instance.uploader = user
        instance.save()
        return instance
