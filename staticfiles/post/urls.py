from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    GetKeywords,
    GetKeywordVal,
    PostModelViewSet
)


router = DefaultRouter()
router.register(r'posts', PostModelViewSet)


urlpatterns = [
    #auth
    path('api/v1/get_keywords',GetKeywords.as_view()),

    path('api/v1/get_keywords_val',GetKeywordVal.as_view()),
    path('', include(router.urls)),
    
]
