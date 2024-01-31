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
from mimetypes import guess_type, guess_extension
from uuid import uuid4

# Models
from .models import Book, Code, Folder, Tag, Uploader


COLLEGES = ['COLENG']
DEPTS = ['ABE', 'CVE', 'ELE', 'MCE', 'MTE', 'GEN']
LEVELS = ['100', '200', '300', '400', '500', 'TXT']
COURSES = ['PQS']
SESSIONS = ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']


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
        print(f"Generating DB from Drive by {uploader.username}...")
        for college in COLLEGES:
            college_folder = self.get_folder_details(college)[0]
            # Optimize try except
            if college not in [folder.name for folder in Folder.objects.all()]:
                col_folder = Folder.objects.create(
                    name=college_folder['name'],
                    parent=None,
                    id=college_folder['id']
                )
            try:
                college_obj = Folder.objects.get(name=college)
            except Exception:
                raise Exception('Could not create or find college')
            print(f"{college}: ")
            dept_folders = self.get_folder_details(parents=college_folder['id'])
            for dept in dept_folders:
                if dept.get('name') not in [folder.name for folder in Folder.objects.all()]:
                    dept_folder = Folder.objects.create(
                        name=dept.get('name'),
                        parent=college_obj,
                        id=dept.get('id')
                    )  # Can also say dept folders are tags
                print(f"  Dept: {dept.get('name')}")
                try:
                    tag = Tag.objects.get_or_create(
                        name=dept.get('name')
                    )[0]
                except Exception:
                    raise Exception('Could not create or find tag')
                try:
                    dept_obj = Folder.objects.get(name=dept.get('name'))
                except Exception:
                    raise Exception('Could not create or find dept')
                level_folders = self.get_folder_details(parents=dept.get('id'))
                for level in level_folders:
                    if level.get('name') not in [folder.name for folder in Folder.objects.all()]:
                        level_folder = Folder.objects.create(
                            name=level.get('name'),
                            parent=dept_obj,
                            id=level.get('id')
                        )
                    print(f"    Level: {level.get('name')}")
                    try:
                        level_obj = Folder.objects.get(name=level.get('name'))
                    except Exception:
                        raise Exception('Could not create or find level')
                    semester_folders = self.get_folder_details(parents=level.get('id'))
                    for semester in semester_folders:
                        if semester.get('name') not in [folder.name for folder in Folder.objects.all()]:
                            semester_folder = Folder.objects.create(
                                name=semester.get('name'),
                                parent=level_obj,
                                id=semester.get('id')
                            )
                        print(f"      Semester: {semester.get('name')}")
                        try:
                            semester_obj = Folder.objects.get(name=semester.get('name'))
                        except Exception:
                            raise Exception('Could not create or find semester')
                        session_folders = self.get_folder_details(parents=semester.get('id'))
                        for session in session_folders:
                            if session.get('name') not in [folder.name for folder in Folder.objects.all()]:
                                session_folder = Folder.objects.create(
                                    name=session.get('name'),
                                    parent=semester_obj,
                                    id=session.get('id')
                                )
                            print(f"        Session: {session.get('name')}")
                            # Can also say course folders are course codes
                            try:
                                session_obj = Folder.objects.get(name=session.get('name'))
                            except Exception:
                                raise Exception('Could not create or find session')
                            course_folders = self.get_folder_details(parents=session.get('id'))
                            for course in course_folders:  # and PQS
                                if course.get('name') not in [folder.name for folder in Folder.objects.all()]:
                                    course_folder = Folder.objects.create(
                                        name=course.get('name'),
                                        parent=session_obj,
                                        id=course.get('id')
                                    )
                                try:
                                    code = Code.objects.get_or_create(
                                        code=course.get('name')
                                    )[0]
                                except Exception:
                                    raise Exception('Could not create or find code')
                                try:
                                    course_obj = Folder.objects.get(name=course.get('name'))
                                except Exception:
                                    print('Could not create or find course')
                                print(f"          Course: {course.get('name')}")
                                book_files = self.get_files_details(parent=course.get('id'))
                                for book in book_files:
                                    if book.get('name') not in [book.title for book in Book.objects.all()]:
                                        book_file = Book.objects.create(
                                            title=book.get('name'),
                                            parents=[
                                                college_obj.id,
                                                dept_obj.id,
                                                level_obj.id,
                                                session_obj.id,
                                                course_obj.id
                                            ],
                                            drive_id=book.get('id'),
                                            download=book.get('webContentLink'),
                                            size=int(book.get('size')),
                                            level=level.get('name'),
                                            session=session.get('name'),
                                            uploader=uploader,
                                            tag=tag,
                                            code=code
                                        )
                                    print(f"            {book.get('name')}", end='')
                                print('')
        print('Done!')

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
        if parent:
            q += f" and '{parent}' in parents"
        results = Manager.SERVICE.files().list(
            q=q,
            pageSize=200,
            fields="nextPageToken, files(id, name, parents, webContentLink, size)"
        ).execute()
        files = results.get('files', None)

        return files
