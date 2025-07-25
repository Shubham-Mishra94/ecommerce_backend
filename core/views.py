# Django & Redis connection
from django.core.cache import cache
from django.contrib.auth import get_user_model

# For DRF core requirements
from rest_framework import viewsets, generics, permissions, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

# For Django Filters (3rd Party)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# For Django Models (internally)
from .models import Category, Product, Order

# For Serializers
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    CustomTokenObtainPairSerializer,
    OrderSerializer
)

from .notifications import broadcast_order_status  # optional: move logic here

# For Custom django-filter
from .filters import ProductFilter  




User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]  # only admin can CRUD categories


    def list(self, request, *args, **kwargs):
        cached_data = cache.get('category_list')
        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set('category_list', response.data, timeout=3600)  # 1 hour cache (60x60)
        return response

    def perform_create(self, serializer):
        serializer.save()
        cache.delete('category_list')

    def perform_update(self, serializer):
        serializer.save()
        cache.delete('category_list')

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete('category_list')


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'stock']
    search_fields = ['name', 'description']

    def list(self, request, *args, **kwargs):
        cached_products = cache.get('product_list')
        if cached_products:
            return Response(cached_products)

        queryset = self.filter_queryset(self.get_queryset())  # Apply filters/search
        page = self.paginate_queryset(queryset)


        if page is not None:
            serializer = self.get_serializer(page, many=True)
            cache.set('product_list', serializer.data, timeout=3600)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        cache.set('product_list', serializer.data, timeout=3600)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete('product_list')  # Invalidate cache
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        cache.delete('product_list')  # Invalidate cache
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        cache.delete('product_list')  # Invalidate cache
        return response
    



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        if 'status' in serializer.validated_data:
            broadcast_order_status(instance)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)









        