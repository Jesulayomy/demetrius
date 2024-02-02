""" Contains the models for the project """
from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError


LEVELS = {
    0: "Any Level",
    100: "100 Level",
    200: "200 Level",
    300: "300 Level",
    400: "400 Level",
    500: "500 Level",
}


def get_default_year() -> int:
    """ Returns the default year for the session """
    if datetime.now().month < 9:
        DEFAULT_YEAR = datetime.now().year - 1
    else:
        DEFAULT_YEAR = datetime.now().year
    return DEFAULT_YEAR


def session_validator(value: int):
    """ Validates the session value """
    if value < 1990 or value > datetime.now().year:
        raise ValidationError("Session must be between 1990 and current year")


class Folder(models.Model):
    """ Representation of the google drive filesystem """
    name = models.CharField(
        max_length=64,
        help_text="The name of the folder"
    )
    folder_id = models.CharField(
        max_length=64,
        help_text="The drive id of the folder"
    )
    parent = models.ForeignKey(
        'Folder',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
        help_text="The parent folder of this folder"
    )

    def __str__(self):
        rep = f"{self.name}"
        if self.parent:
            rep += f" < {self.parent.name}"
            if self.parent.parent:
                rep += f" < {self.parent.parent.name}"
                if self.parent.parent.parent:
                    rep += f" < {self.parent.parent.parent.name}"
                    if self.parent.parent.parent.parent:
                        rep += f" < {self.parent.parent.parent.parent.name}"
        return rep


class Uploader(models.Model):
    """ Table for the uploaders of the books """
    username = models.CharField(
        unique=True,
        max_length=64,
        help_text="The username of the uploader"
    )
    email = models.EmailField(
        null=True,
        blank=True,
        max_length=255,
        help_text="The email of the uploader"
    )

    def __str__(self):
        return f"{self.username}"


class Tag(models.Model):
    """
        A course representation for the books, i.e ELE, ABE, CSC
        used for filtering
    """
    name = models.CharField(
        primary_key=True,
        max_length=3,
        help_text="""
            The tag for the book, usually the course code letters or GEN
            (general), used for searching or filtering
        """
    )
    full_name = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text="The full name of the tag, used for display"
    )

    def __str__(self):
        return f"{self.name} > {self.full_name}"


class Code(models.Model):
    """ Represents a course code instance """
    code = models.CharField(
        primary_key=True,
        max_length=8,
        help_text="The course code for this book (i.e. ELE 102)"
    )
    course = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        help_text="The course this book is required for (i.e. Power Systems)"
    )

    def __str__(self) -> str:
        return f"{self.code} | {self.course}"


class Book(models.Model):
    """ Represents a book in the database """
    level = models.IntegerField(
        choices=LEVELS,
        help_text="The level this book is required for, use 0 if more than one"
    )

    size = models.IntegerField(
        default=0,
        help_text="The file's size estimated by drive properties"
    )

    tag = models.ForeignKey(
        Tag,
        default="GEN",
        on_delete=models.SET_DEFAULT,
        related_name="books",
        help_text="""
            The tag for the book, the course code letters or GEN (general)
        """
    )

    title = models.CharField(
        max_length=256,
        help_text="""
            The book's title or topic or note index as it appears on the
            cover or lecture note (i.e Engineering Mathematics,
            First Order Differential Equations, Note 6)
        """
    )

    code = models.ForeignKey(
        Code,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="books",
        help_text="Foreign key to the course codes"
    )

    uploader = models.ForeignKey(
        Uploader,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="books",
        help_text="The uploader of this book"
    )

    session = models.IntegerField(
        validators=[session_validator],
        default=get_default_year,
        help_text="""
            The session this book is required for, use the preceding year.
            i.e. 2018/2019 should be 2018 session.
        """
    )

    downloads = models.IntegerField(
        default=0,
        help_text="The number of times this book has been downloaded"
    )

    description = models.TextField(
        null=True,
        blank=True,
        max_length=999,
        help_text="A short description of the book"
    )

    download = models.URLField(
        null=True,
        blank=True,
        max_length=512,
        help_text="The download link for the book"
    )

    drive_id = models.CharField(
        null=True,
        blank=True,
        max_length=64,
        help_text="The drive id of the book"
    )

    parents = models.JSONField(
        null=True,
        blank=True,
        help_text="The parent drive id's of the book"
    )

    def __str__(self):
        return f"{self.title}"
