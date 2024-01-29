""" Generates some uploaders, codes, tags and books for the application """
import os
import random

from library.models import Uploader, Code, Tag, Book



TAGS = [
    'ABE', 'ELE', 'CVE', 'MCE', 'MTE', 'GEN', 'CSC', 'PHY', 'CHM', 'BIO',
]

COURSE_NUMBERS = [
    104, 101, 102, 103,
    204, 201, 202, 203,
    304, 301, 302, 303,
    404, 401, 402, 403,
    504, 501, 502, 503,
]

USERNAMES = [
    'justice', 'layomi', 'david', 'daniel', 'michael', 'philip'
]


def generate_uploaders():
    """ Generates some uploaders """
    for username in USERNAMES:
        Uploader.objects.create(
            username=username,
            email=f"{username}@gmail.com",
        )


def generate_tags():
    """ Generates some tags """
    for tag in TAGS:
        Tag.objects.create(
            name=tag,
            full_name=f'{tag} full name',
        )


def generate_codes():
    """ Generates some codes """
    for tag in TAGS:
        for number in COURSE_NUMBERS:
            Code.objects.create(
                code=f'{tag} {number}',
            )


def generate_books():
    """ Generates some books """
    for _ in range(20):
        level = random.choice([0, 100, 200, 300, 400, 500])
        tag = random.choice(Tag.objects.all())
        code = random.choice(
            Code.objects.filter(
                code__startswith=tag.name,
            )
        )
        uploader = random.choice(Uploader.objects.all())
        title = f'{code.code} title'
        session = random.choice([2022, 2023, 2021])
        book = Book.objects.create(
            title=title,
            level=level,
            tag=tag,
            code=code,
            uploader=uploader,
            session=session,
        )
        print(f"Created {book.title} by {book.uploader.username}")


if __name__ == '__main__':
    generate_uploaders()
    generate_tags()
    generate_codes()
    generate_books()
    print('Done!')