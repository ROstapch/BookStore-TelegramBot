from rest_framework import routers
from Store import api_views as store_views

router = routers.DefaultRouter()
router.register(r'authors', store_views.AuthorViewset)
router.register(r'publishers', store_views.PublisherViewset)
router.register(r'books', store_views.BookViewset)