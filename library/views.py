import json

from django.shortcuts import render
from django.http import Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Book, Uploader
from .serializers import BookSerializer, UploaderSerializer


class Books(APIView):
    """ Books api view """

    def get(self, request):
        """ Handles get requests """
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        """ Handles post requests """
        data = json.loads(request.body)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors)


class BookDetail(APIView):
    """ Book detail api view """

    def get(self, request, pk):
        """ Handles get requests """
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    @csrf_exempt
    def put(self, request, pk):
        """ Handles put requests """
        data = json.loads(request.body)
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    @csrf_exempt
    def delete(self, request, pk):
        """ Handles delete requests """
        book = Book.objects.get(pk=pk)
        book.delete()
        return Response({}, status=204)


class Uploaders(APIView):
    """ Uploaders api view """

    def get(self, request):
        """ Handles get requests """
        uploaders = Uploader.objects.all()
        serializer = UploaderSerializer(uploaders, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        """ Handles post requests """
        data = json.loads(request.body)
        serializer = UploaderSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors)


class UploaderDetail(APIView):
    """ Uploader detail api view """

    def get(self, request, pk):
        """ Handles get requests """
        uploader = Uploader.objects.get(pk=pk)
        serializer = UploaderSerializer(uploader)
        return Response(serializer.data)
    
    @csrf_exempt
    def put(self, request, pk):
        """ Handles put requests """
        data = json.loads(request.body)
        uploader = Uploader.objects.get(pk=pk)
        serializer = UploaderSerializer(uploader, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    @csrf_exempt
    def delete(self, request, pk):
        """ Handles delete requests """
        uploader = Uploader.objects.get(pk=pk)
        uploader.delete()
        return Response({}, status=204)
