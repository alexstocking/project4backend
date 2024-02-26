from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Product, Request, Tag, Cart, CartProduct, List, ListProduct

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.SerializerMethodField()

    def get_tags(self, obj):
        # Assuming tags is a ManyToMany field in the Product model
        return [tag.name for tag in obj.tags.all()]
    
    class Meta:
        model = Product
        fields = ['id', 'url', 'name', 'description', 'stock', 'price', 'tags']

class RequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'url', 'name']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = '__all__'

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'

class ListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListProduct
        fields = '__all__'