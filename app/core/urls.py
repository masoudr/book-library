from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core import views


app_name = 'core'

router = DefaultRouter()
router.register('author', views.AuthorViewSet)
router.register('book', views.BookViewSet)


urlpatterns = [
    path('', include(router.urls))
]
