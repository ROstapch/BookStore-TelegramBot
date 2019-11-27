from rest_framework import viewsets
from Store import models
from Store import serializers



class AuthorViewset(viewsets.ModelViewSet):
	queryset  = models.Author.objects.all()
	serializer_class = serializers.AuthorSerializer


class PublisherViewset(viewsets.ModelViewSet):
	queryset  = models.Publisher.objects.all()
	serializer_class = serializers.PublisherSerializer


class BookViewset(viewsets.ModelViewSet):
	queryset  = models.Book.objects.all()
	serializer_class = serializers.BookSerializer
