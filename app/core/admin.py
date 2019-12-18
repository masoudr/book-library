from django.contrib import admin
from core.models import User, Author, Book

# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Author)
