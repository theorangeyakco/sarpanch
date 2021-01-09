from rest_framework.routers import DefaultRouter

from content.views import PostViewSet


app_name = 'content'

recipe_viewset_router = DefaultRouter()
recipe_viewset_router.register(r'recipes', PostViewSet, basename='recipe')

urlpatterns = [

]

urlpatterns += recipe_viewset_router.urls


