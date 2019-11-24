from django.shortcuts import render
from Store.models import *


def books(request):
	books_list = Book.objects.order_by('name')
	return render(request, 'Store/books.html', {'books': books_list})