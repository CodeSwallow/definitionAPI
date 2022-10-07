from django.urls import path, include
from rest_framework.routers import DefaultRouter

from dictionary.views import WordDetailView, WordViewSet, DefinitionViewSet

router = DefaultRouter()
router.register(r'words', WordViewSet, basename='word')
router.register(r'definitions', DefinitionViewSet, basename='definition')

app_name = "dictionary"
urlpatterns = [
    path('', include(router.urls)),
    path('definition/<str:pk>', WordDetailView.as_view()),
]
