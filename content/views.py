from django.shortcuts import render
from django_filters import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from knox.auth import TokenAuthentication

from content.models import Post, Category
from content.serializers import PostSerializer, CategorySerializer


class PostFilter(FilterSet):
	title_contains = filters.CharFilter(field_name="title", lookup_expr='icontains')
	created_before = filters.DateTimeFilter(field_name='created_on', lookup_expr='lte')
	updated_before = filters.DateTimeFilter(field_name='updated_on', lookup_expr='lte')

	class Meta:
		model = Post
		fields = ['title_contains', 'created_before', 'updated_before', 'categories']


class PostViewSet(ReadOnlyModelViewSet):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filterset_class = PostFilter
	queryset = Post.objects.filter(published=True)
	serializer_class = PostSerializer
	search_fields = ('title', 'sub_title')


class CategoryList(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	@staticmethod
	def get(request):
		queryset = Category.objects.all()
		serializer = CategorySerializer(queryset, many=True)
		return Response(serializer.data, status=200)


class CategoryDetail(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	@staticmethod
	def get(request, pk):
		c = get_object_or_404(Category, id=pk)
		serializer = CategorySerializer(c)
		return Response(serializer.data, status=200)

