from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView

from menu.models import Dish, SubCategory, MainCategory, Restaurant
from menu.serializers import DishSerializer, SubCategorySerializer, MainCategorySerializer, RestaurantSerializer, \
    RegisterSerializer, RestaurantMinimalSerializer, MainCategoryMinimalSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'restaurant'):
            return obj.restaurant.owner == request.user
        elif hasattr(obj, 'parent_category'):
            return obj.parent_category.restaurant.owner == request.user
        elif hasattr(obj, 'subcategory'):
            return obj.subcategory.parent_category.restaurant.owner == request.user
        return False


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RestaurantSerializer
        return RestaurantMinimalSerializer

class MainCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = MainCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = MainCategory.objects.all()
        restaurant_id = self.request.query_params.get('restaurant', None)
        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MainCategorySerializer
        return MainCategoryMinimalSerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = SubCategory.objects.all()
        parent_id = self.request.query_params.get('parent_category', None)
        name = self.request.query_params.get('name', None)

        if parent_id:
            queryset = queryset.filter(parent_category_id=parent_id)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = DishSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Dish.objects.all()
        subcategory_id = self.request.query_params.get('subcategory', None)
        name = self.request.query_params.get('name', None)

        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.context['ingredients'] = request.data.get('ingredients', [])
        self.perform_create(serializer)
        return Response(serializer.data)


class RegisterAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Send a POST request to register."})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"detail": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


