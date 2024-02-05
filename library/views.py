import json

from django.db.models.functions import Lower
from django.http import (
    Http404,
    HttpResponse,
)
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .manager import Manager
from .models import (
    Book,
    Code,
    Folder,
    Tag,
    Uploader,
)
from .serializers import (
    BookSerializer,
    CodeSerializer,
    FolderSerializer,
    TagSerializer,
    UploaderSerializer,
)


manager = Manager()  # Manages the file uploads with Drive V3 API


class Books(APIView):
    """ Books api views """

    def get(self, request):
        """ Handles get requests """
        query_params = request.GET.dict()
        params = ["level", "tag", "uploader", "code", "session", "title"]
        filters = {}
        for param in params:
            if param in query_params.keys():
                if (
                    param == "level" or
                    param == "uploader" or
                    param == "session"
                ):
                    filters[param] = int(query_params[param])
                elif param == "title":
                    filters["title__icontains"] = query_params[param]
                else:
                    filters[param] = query_params[param]
        books = Book.objects.filter(**filters).order_by(
            Lower("session").desc(),
            Lower("code").asc()
        )
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        """ Handles post requests """
        data = json.loads(request.data.get('data'))
        file = request.FILES.get('book')
        college = Folder.objects.get(
            name=data.pop('college', 'COLENG'),
            parent=None
        )
        dept = Folder.objects.get(
            name=data.get('tag'),
            parent=college.id
        )
        level = Folder.objects.get(
            name=str(data.get('level')),
            parent=dept.id
        )
        parents = [
            college.folder_id,
            dept.folder_id,
            level.folder_id,
        ]
        if level.name != "TXT":
            semester = Folder.objects.get(
                name=data.get('semester'),
                parent=level.id
            )
            session = Folder.objects.get(
                name=str(data.get('session')),
                parent=semester.id
            )
            course = Folder.objects.get(
                name=data.get('code'),
                parent=session.id
            )
            parents.append(session.folder_id)
            parents.append(course.folder_id)

        book = manager.create_file(parents[-1], request.FILES.get('book'))
        book_data = {
            'level': int(level.name) if level.name != 'TXT' else 0,
            'size': book.get('size'),
            'tag': dept.name,
            'title': data.get('title', book['drive_name']),
            'code': data.get('code', None),
            'uploader': data.get('uploader'),
            'session': data.get('session', None),
            'description': data.get('description'),
            'download': book.get('download'),
            'drive_id': book.get('drive_id'),
            'parents': parents,
        }
        print(book_data)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors)


class BookDetail(APIView):
    """ Book detail api view """

    def get(self, request, pk):
        """ Handles get requests """
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return HttpResponse(status=404)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    @csrf_exempt
    def put(self, request, pk):
        """ Handles put requests """
        data = JSONParser().parse(request)
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return HttpResponse(status=404)
        serializer = BookSerializer(book, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @csrf_exempt
    def delete(self, request, pk):
        """ Handles delete requests """
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return HttpResponse(status=404)
        manager.delete_book(book.drive_id)
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
        data = JSONParser().parse(request)
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
        data = JSONParser().parse(request)
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


class Codes(APIView):
    """ Code api view """

    def get(self, request):
        """ Handles get requests """
        query_params = request.GET.dict()
        courses = []
        if query_params.get("level") and query_params.get("tag"):
            dept = Folder.objects.get(name=query_params.get('tag'))
            level = Folder.objects.get(
                name=query_params.get('level'),
                parent=dept
            )
            for semester in level.children.all():
                for session in semester.children.all():
                    for course in session.children.all():
                        courses.append(course.name)
            codes = Code.objects.filter(code__in=courses)
            serializer = CodeSerializer(codes, many=True)
            return Response(serializer.data)
        codes = Code.objects.all()
        serializer = CodeSerializer(codes, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        """ Handles post requests """
        data = JSONParser().parse(request)
        serializer = CodeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors)


class CodeDetail(APIView):
    """ Code detail api view """

    def get(self, request, pk):
        """ Handles get requests """
        code = Code.objects.get(pk=pk)
        serializer = CodeSerializer(code)
        return Response(serializer.data)

    @csrf_exempt
    def put(self, request, pk):
        """ Handles put requests """
        data = JSONParser().parse(request)
        code = Code.objects.get(pk=pk)
        serializer = CodeSerializer(code, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @csrf_exempt
    def delete(self, request, pk):
        """ Handles delete requests """
        code = Code.objects.get(pk=pk)
        code.delete()
        return Response({}, status=204)


class Tags(APIView):
    """ Tag api view """

    def get(self, request):
        """ Handles get requests """
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        """ Handles post requests """
        data = JSONParser().parse(request)
        serializer = TagSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors)


class TagDetail(APIView):
    """ Tag detail api view """

    def get(self, request, pk):
        """ Handles get requests """
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    @csrf_exempt
    def put(self, request, pk):
        """ Handles put requests """
        data = JSONParser().parse(request)
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @csrf_exempt
    def delete(self, request, pk):
        """ Handles delete requests """
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response({}, status=204)


class Folders(APIView):
    """ Folder api view """

    def get(self, request):
        """ Handles get requests """
        folders = Folder.objects.all()
        serializer = FolderSerializer(folders, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        """ Handles post requests """
        data = JSONParser().parse(request)
        folders = data.get('parents')
        college = Folder.objects.get(name=folders[0])
        dept = Folder.objects.get(name=folders[1], parent=college.id)
        level = Folder.objects.get(name=folders[2], parent=dept.id)
        semester = Folder.objects.get(name=folders[3], parent=level.id)
        # Check the session and course, and create as needed
        try:
            session = Folder.objects.get(
                name=folders[4],
                parent=semester.id
            )
        except Folder.DoesNotExist:
            session = manager.create_folder(
                folders[4],
                semester.folder_id
            )
            result = Folder.objects.create(
                name=session['name'],
                folder_id=session['folder_id'],
                parent=semester
            )
        try:
            course = Folder.objects.get(
                name=folders[5],
                parent=session.id
            )
        except KeyError:
            pass
        except Folder.DoesNotExist:
            course = manager.create_folder(
                folders[5],
                parent=session.folder_id
            )
            result = Folder.objects.create(
                name=course['name'],
                folder_id=course['folder_id'],
                parent=session
            )
        return Response(
            {
                'id': result.id,
                'name': result.name,
                'folder_id': result.folder_id,
                'parent': result.parent
            },
            status=201
        )


class FolderDetail(APIView):
    """ Folder detail api view """

    def get(self, request, pk):
        """ Handles get requests """
        folder = Folder.objects.get(pk=pk)
        serializer = FolderSerializer(folder)
        return Response(serializer.data)

    @csrf_exempt
    def put(self, request, pk):
        """ Handles put requests """
        data = JSONParser().parse(request)
        folder = Folder.objects.get(pk=pk)
        serializer = FolderSerializer(folder, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @csrf_exempt
    def delete(self, request, pk):
        """ Handles delete requests """
        folder = Folder.objects.get(pk=pk)
        folder.delete()
        return Response({}, status=204)


# class FolderTree(APIView):
#     """ Resolves the folders tree """

#     def get(self, request):
#         """ Handles get requests """
#         colleges = Folder.objects.filter(parent=None)
#         tree = {}
#         for college in colleges:
#             tree[college.name] = {}
#             for dept in college.children.all():
#                 tree[college.name][dept.name] = {}
# for level in dept.children.all():
# tree[college.name][dept.name][level.name] = {}
# for semester in level.children.all():
# tree[college.name][dept.name][level.name][semester.name] = {}
# for session in semester.children.all():
# tree[college.name][dept.name][level.name][semester.name][session.name]
# = None
# for course in session.children.all():
# tree[college.name][dept.name][level.name][semester.name][session.name]
# = course.name

#         return Response(tree)

class CodeBooks(APIView):
    """ View for displaying books through codes """
    def get(self, request, pk):
        """ Gets a dict of books with the code given"""
        query_params = request.GET.dict()
        params = [
            "level", "title",
            "uploader", "tag",
            "session", "code"
        ]
        filters = {}
        for param in params:
            if param in query_params.keys():
                if (
                    param == "level" or
                    param == "uploader" or
                    param == "session"
                ):
                    filters[param] = int(query_params[param])
                elif param == "title":
                    filters["title__icontains"] = query_params[param]
                else:
                    filters[param] = query_params[param]
        books = Code.objects.get(pk=pk).books.filter(**filters)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


def view_data(request):
    """ Handles html requests """
    books = Book.objects.all().order_by(
        Lower("session").desc(),
        Lower("code").asc()
    )
    return render(request, "library/view.html", {"books": books})
