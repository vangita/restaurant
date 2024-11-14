from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import RegisterAPIView

router = DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurant')
router.register(r'main-categories', views.MainCategoryViewSet, basename='maincategory')
router.register(r'sub-categories', views.SubCategoryViewSet, basename='subcategory')
router.register(r'dishes', views.DishViewSet, basename='dish')


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
]

urlpatterns += router.urls