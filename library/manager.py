"""
    This module contains the Manager class
    (Mostly for creating files and folders)
"""
from __future__ import print_function

import os

from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import (
    MediaFileUpload,
    MediaIoBaseUpload,
)
from io import BytesIO
from mimetypes import guess_type, guess_extension
from uuid import uuid4

# Models
from .models import Book, Code, Folder, Tag, Uploader


COLLEGES = ['COLENG']
DEPTS = ['ABE', 'CVE', 'ELE', 'MCE', 'MTE', 'GEN']
LEVELS = ['100', '200', '300', '400', '500', 'TXT']
COURSES = ['PQS']
SESSIONS = [
    '2016', '2017', '2018',
    '2019', '2020', '2021',
    '2022', '2023', '2024'
]


class Manager:
    """ Manager class  for handling fule uploads in the proper channels """
    CREDS = None
    SCOPES = [
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive.metadata.readonly',
        ]

    SERVICE = None

    def __init__(self):
        """ Initialization of the Manager and service """
        if os.path.exists('token.json'):
            Manager.CREDS = Credentials.from_authorized_user_file(
                'token.json',
                Manager.SCOPES
            )
        self.validate_creds(Manager.CREDS)
        self.get_service(Manager.CREDS)

    def validate_creds(self, creds):
        """
            Validates the credentials sent or generates a new one
        """
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json',
                    Manager.SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as tokenfile:
                tokenfile.write(creds.to_json())

    def get_service(self, creds):
        """ Builds a service object for the api """
        try:
            Manager.SERVICE = build('drive', 'v3', credentials=creds)
        except HttpError as err:
            print(err)

    def build_db_tree_from_drive(self):
        """ Builds the database from scratch, following a drive folder"""
        if Manager.SERVICE is None:
            return None
        # Call the Drive v3 API to build the database
        try:
            uploader = Uploader.objects.get_or_create(
                username='Jesulayomi',
            )[0]
        except Exception:
            raise Exception('Could not create or find uploader')
        try:
            gen_tag = Tag.objects.get_or_create(
                name='GEN',
                full_name='General'
            )[0]
        except Exception:
            raise Exception('Could not create or find general tag')
        print(f"Generating DB from Drive by {uploader.username}...")
        for college in COLLEGES:
            data = {}
            college_drive = self.get_folder_details(college)[0]
            try:
                college_obj = Folder.objects.get(name=college)
            except Folder.DoesNotExist:
                college_obj = Folder.objects.create(
                    name=college_drive['name'],
                    parent=None,
                    folder_id=college_drive['id']
                )
            data['college'] = college_obj.folder_id
            print(f"{college_obj.name}: ")
            dept_folders = self.get_folder_details(
                parents=college_drive['id']
            )
            for dept in dept_folders:
                try:
                    dept_obj = Folder.objects.get(name=dept['name'])
                except Folder.DoesNotExist:
                    dept_obj = Folder.objects.create(
                        name=dept['name'],
                        parent=college_obj,
                        folder_id=dept['id']
                    )
                data['dept'] = dept_obj.folder_id
                # Can also say dept folders are tags, hence;
                tag = Tag.objects.get_or_create(
                    name=dept.get('name')
                )[0]
                print(f" Dept: {dept.get('name')}")
                level_folders = self.get_folder_details(
                    parents=dept.get('id')
                )
                for level in level_folders:  # Include TXT filters
                    try:
                        level_obj = Folder.objects.get(
                            name=level.get('name'),
                            parent=dept_obj
                        )
                    except Folder.DoesNotExist:
                        level_obj = Folder.objects.create(
                            name=level.get('name'),
                            parent=dept_obj,
                            folder_id=level.get('id')
                        )
                    data['level'] = level_obj.folder_id
                    data['level_name'] = level_obj.name
                    print(f"  Level: {level.get('name')}")
                    if level_obj.name == 'TXT':
                        texts = self.get_files_details(parent=level.get('id'))
                        for text in texts:
                            self.create_db_book(
                                text,
                                data,
                                tag or gen_tag,
                                None,
                                uploader
                            )
                        continue
                    semester_folders = self.get_folder_details(
                        parents=level.get('id')
                    )
                    for semester in semester_folders:
                        try:
                            semester_obj = Folder.objects.get(
                                name=semester.get('name'),
                                parent=level_obj
                            )
                        except Folder.DoesNotExist:
                            semester_obj = Folder.objects.create(
                                name=semester.get('name'),
                                parent=level_obj,
                                folder_id=semester.get('id')
                            )
                        data['semester'] = semester_obj.folder_id
                        print(f"   Semester: {semester.get('name')}")
                        session_folders = self.get_folder_details(
                            parents=semester.get('id')
                        )
                        for session in session_folders:
                            try:
                                session_obj = Folder.objects.get(
                                    name=session.get('name'),
                                    parent=semester_obj
                                )
                            except Folder.DoesNotExist:
                                session_obj = Folder.objects.create(
                                    name=session.get('name'),
                                    parent=semester_obj,
                                    folder_id=session.get('id')
                                )
                            data['session'] = session_obj.folder_id
                            data['session_name'] = session_obj.name
                            print(f"    Session: {session.get('name')}")
                            course_folders = self.get_folder_details(
                                parents=session.get('id')
                                )
                            for course in course_folders:  # and PQS
                                try:
                                    course_obj = Folder.objects.get(
                                        name=course.get('name'),
                                        parent=session_obj
                                    )
                                except Folder.DoesNotExist:
                                    course_obj = Folder.objects.create(
                                        name=course.get('name'),
                                        parent=session_obj,
                                        folder_id=course.get('id')
                                    )
                                data['course'] = course_obj.folder_id
                                try:
                                    code = Code.objects.get_or_create(
                                        code=course.get('name')
                                    )[0]
                                except Exception:
                                    raise Exception(
                                        'Could not create or find code'
                                    )
                                print(f"     Course: {course.get('name')}")
                                book_files = self.get_files_details(
                                    parent=course.get('id')
                                )
                                for book in book_files:
                                    if (book.get('name') not in
                                            [book.title
                                                for book in
                                                Book.objects.all()]):
                                        book_file = self.create_db_book(
                                            book, data,
                                            tag, code,
                                            uploader
                                        )
        print('Done!')

    def create_db_book(self, book, data, tag, code, uploader):
        """ Creates new book object """
        parents = [
            data.get('college'),
            data.get('dept'),
            data.get('level')
        ]
        if data.get('level_name') == 'TXT':
            data['level_name'] = 0
        else:
            parents.append(data['session'])
            parents.append(data['course'])
        book_file = Book.objects.create(
            title=book.get('name'),
            parents=parents,
            drive_id=book.get('id'),
            download=book.get('webContentLink'),
            size=book.get('size', 0),
            level=int(data['level_name']),
            session=data.get('session_name', 2023),
            uploader=uploader,
            tag=tag,
            code=code
        )
        print(f"      {book.get('name')}")
        return book_file

    def get_folder_details(self, name=None, parents=None):
        """
            Gets the details of a folder. You must have called
            MANAGER.get_service() before calling this method.
        """
        q = "mimeType='application/vnd.google-apps.folder'"
        if name:
            q += f" and name='{name}'"
        if parents:
            q += f" and '{parents}' in parents"
        results = Manager.SERVICE.files().list(
            q=q,
            pageSize=10,
            fields="nextPageToken, files(id, name, parents)"
        ).execute()
        folders = results.get('files', None)

        return folders

    def get_files_details(self, parent):
        """
            Gets the details of a file. You must have called
            MANAGER.get_service() before calling this method.
            Retrieves all the filesin teh directory given as parent.
        """
        q = "mimeType!='application/vnd.google-apps.folder'"
        flds = "nextPageToken, files(id, name, parents, webContentLink, size)"
        if parent:
            q += f" and '{parent}' in parents"
        results = Manager.SERVICE.files().list(
            q=q,
            pageSize=500,
            fields=flds
        ).execute()
        files = results.get('files', None)

        return files

    def create_folder(self, name, parent=None):
        """ Creates a folder in the parent directory with te name provided """
        if Manager.SERVICE is None:
            return None
        folder_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent:
            folder_metadata['parents'] = [parent]
        try:
            folder = Manager.SERVICE.files().create(
                body=folder_metadata,
                fields='*'
            ).execute()
            Manager.SERVICE.permissions().create(
                fileId=folder.get('id'),
                body={
                    'role': 'reader',
                    'type': 'anyone',
                }
            ).execute()
        except Exception as e:
            print(e)
            return None
        result = {
            'drive_id': folder.get('id'),
            'drive_name': folder.get('name'),
            'parents': parent,
        }
        return result

    def create_file(self, parent, file):
        """ Creates a file and stores in the appropriate drive """
        if Manager.SERVICE is None:
            return None
        mimetype = guess_type(file._name)[0]
        extension = guess_extension(mimetype, strict=False)
        filename = file._name
        if extension:
            if filename[len(filename) - len(extension):] != extension:
                filename = filename + extension
        file_metadata = {
            'name': filename,
            'parents': [parent]
        }
        bytes_io = BytesIO(file.read())
        file_media = MediaIoBaseUpload(bytes_io, mimetype=mimetype)
        try:
            file = Manager.SERVICE.files().create(
                body=file_metadata,
                media_body=file_media,
                fields='*'
            ).execute()
            Manager.SERVICE.permissions().create(
                fileId=file.get('id'),
                body={
                    'role': 'reader',
                    'type': 'anyone',
                }
            ).execute()
        except Exception as e:
            print(e)
            return None
        result = {
            'download': file.get('webContentLink'),
            'drive_id': file.get('id'),
            'drive_name': file.get('name'),
            'size': int(file.get('size')),
            'parents': parent,
        }
        return result

    def delete_book(self, drive_id: str):
        """ Deletes the book data from the drive """
        if Manager.SERVICE is None:
            return None
        try:
            Manager.SERVICE.files().delete(fileId=drive_id).execute()
        except Exception as e:
            print(e)
            return None
