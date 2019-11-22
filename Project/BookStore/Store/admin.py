from django.contrib import admin
from Store.models import *

# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)