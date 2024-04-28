import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from drf_yasg.utils import swagger_auto_schema

from django.core.files.storage import default_storage
from rest_framework import serializers
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import viewsets
from openai import OpenAI
from .service import get_keywords, get_keyword_val
from .models import Post


class GetKeywordsSerializers(serializers.Serializer):
    text = serializers.CharField(max_length=5000)


class GetKeywords(generics.GenericAPIView):
    serializer_class = GetKeywordsSerializers

    @swagger_auto_schema(query_serializer=GetKeywordsSerializers)
    def post(self, request, *args, **kwargs):
        text = request.GET.get('text')
        result = get_keywords(text)
        return Response({'result': result},status=status.HTTP_200_OK, headers={'Content-Type': 'application/json; charset=utf-8'})



class GetKeywordVal(generics.GenericAPIView):

    @swagger_auto_schema(query_serializer=GetKeywordsSerializers)
    def post(self, request, *args, **kwargs):
        text = request.GET.get('text')
        result = get_keyword_val(text)

        

        return Response({'result': result},status=status.HTTP_200_OK, headers={'Content-Type': 'application/json; charset=utf-8'})



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'



class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer