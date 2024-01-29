"""
    This module contains the Manager class
    (Mostly for creating files and folders)
"""
from __future__ import print_function

import os

from datetime import datetime
from google.auth.transport.requests import Request
# Used for credential
from google.oauth2.credentials import Credentials
# Used to get credentials from token.json
from google_auth_oauthlib.flow import InstalledAppFlow
# Helps create the file
from googleapiclient.discovery import build
# This is used to build the service
from googleapiclient.errors import HttpError
# Handles error in requests
from googleapiclient.http import (
    MediaFileUpload,
    MediaIoBaseUpload,
)
# Creates a media file to upload
from mimetypes import guess_type, guess_extension
from uuid import uuid4

# Models
from .models import Book
from .models import Uploader


