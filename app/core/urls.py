from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core import views


app_name = 'core'

router = DefaultRouter()
router.register('author', views.AuthorViewSet)
router.register('book', views.BookViewSet)
router.register('books', views.BookDocumentViewSet, basename='booksearch')

urlpatterns = [
    path('', include(router.urls)),
]
