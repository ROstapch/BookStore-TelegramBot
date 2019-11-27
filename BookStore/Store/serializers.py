from rest_framework import serializers
from Store import models



class AuthorSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Author
		fields = ['id', 'name', 'photo', 'date_of_birth']


class PublisherSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Publisher
		fields = ['id', 'name', 'notes']


class BookSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Book
		fields = ['id', 'name', 'cover', 'author', 'publisher', 'pages', 'year']

