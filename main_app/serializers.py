from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Product, Request, Tag, Cart, CartProduct, List, ListProduct

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'first_name', 'last_name', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )
    
    class Meta:
        model = Product
        fields = ['id', 'url', 'name', 'description', 'stock', 'price', 'tags', 'image']

class RequestSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Request
        fields = ['id', 'name', 'description', 'date', 'price_range', 'user', 'tags']


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'cart']

class CartSerializer(serializers.ModelSerializer):
    cart_product = CartProductSerializer(many = True)
    class Meta:
        model = Cart
        fields = ['id', 'url', 'user', 'cart_product', 'personalization']


class ListProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = ListProduct
        fields = ['id', 'list', 'product']

class ListSerializer(serializers.ModelSerializer):
    list_product = ListProductSerializer(many = True)
    class Meta:
        model = List
        fields = ['id', 'url', 'user', 'list_product']

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')