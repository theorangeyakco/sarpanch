from django.urls import path
from rest_framework.routers import DefaultRouter

from content.views import PostViewSet, CategoryList


app_name = 'content'

post_viewset_router = DefaultRouter()
post_viewset_router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
	path('categories/', CategoryList.as_view(), name='category_list')
]

urlpatterns += post_viewset_router.urls


