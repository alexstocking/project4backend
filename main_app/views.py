from django.contrib.auth.models import Group, User
from .models import *
from rest_framework import permissions, viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
   
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartProductViewSet(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer

class ListProductViewSet(viewsets.ModelViewSet):
    queryset = ListProduct.objects.all()
    serializer_class = ListProductSerializer

class SignUpView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')

        try:
            new_user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
            new_user.set_password(password)
            new_user.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class EditAccountView(APIView):
    def put(self, request):
        user = request.user

        username = request.data.get('username')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')

        try:
            # Update only if the data is provided
            if username:
                user.username = username
            if email:
                user.email = email
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if password:
                user.set_password(password)
                
            user.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class NewCartRequest(APIView):
    def post(self, request):
        personalization = request.data.get('personalization')
        cart_id = request.data.get('cart_id')

        try:
            cart = Cart.objects.get(pk=cart_id)
        except:
            return Response({"error": "Cart does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cart.personalization = personalization
            cart.save()
            return Response({"success": "Personalization added to cart"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class NewRequest(APIView):
    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')
        date = request.data.get('date')
        price_range = request.data.get('price_range')
        tags_data = request.data.get('tags') 
        user_id = request.data.get('user') 

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_request = Request.objects.create(
                name=name,
                description=description,
                date=date,
                price_range=price_range,
                user=user
            )
            
            if tags_data:
                tags = [Tag.objects.get_or_create(name=tag)[0] for tag in tags_data]
                new_request.tags.add(*tags)

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class EditRequest(APIView):
    def put(self, request, pk):
        try:
            # Retrieve the request object to update
            try:
                request_instance = Request.objects.get(pk=pk)
            except Request.DoesNotExist:
                return Response({"error": "Request does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Update only if the data is provided
            name = request.data.get('name')
            description = request.data.get('description')
            date = request.data.get('date')
            price_range = request.data.get('price_range')

            if name:
                request_instance.name = name
            if description:
                request_instance.description = description
            if date:
                request_instance.date = date
            if price_range:
                request_instance.price_range = price_range

            # Save the updated request
            request_instance.save()

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Failed to update request."}, status=status.HTTP_400_BAD_REQUEST)
            
@api_view(['GET'])
def current_user(request):
    user = request.user
    serializer = CurrentUserSerializer(user)
    return Response(serializer.data)

class CartProductCreateAPIView(generics.CreateAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

    def create(self, request, *args, **kwargs):
        # Logic to create a new cart if it doesn't exist for the user
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        
        # Logic to add product to the cart
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)
        
        # Add the product to the cart
        cart_item = CartProduct.objects.create(cart=cart, product_id=product_id, quantity=quantity)
        serializer = self.serializer_class(cart_item, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CartProductRemoveAPIView(generics.DestroyAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

    def destroy(self, request, *args, **kwargs):
        cart_product_id = kwargs.get('pk')
        cart_product = get_object_or_404(CartProduct, pk=cart_product_id)
        
        # Check if the cart product belongs to the current user
        if cart_product.cart.user != request.user:
            return Response({"error": "You don't have permission to delete this cart product."},
                            status=status.HTTP_403_FORBIDDEN)
        
        # Delete the cart product
        cart_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ListProductCreateAPIView(generics.CreateAPIView):
    queryset = ListProduct.objects.all()
    serializer_class = ListProductSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        list, created = List.objects.get_or_create(user=user)
        
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)
        
        list_item = ListProduct.objects.create(list=list, product_id=product_id, quantity=quantity)
        serializer = self.serializer_class(list_item, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ListProductRemoveAPIView(generics.DestroyAPIView):
    queryset = ListProduct.objects.all()
    serializer_class = ListProductSerializer

    def destroy(self, request, *args, **kwargs):
        list_product_id = kwargs.get('pk')
        list_product = get_object_or_404(ListProduct, pk=list_product_id)
        
        if list_product.list.user != request.user:
            return Response({"error": "You don't have permission to delete this list product."},
                            status=status.HTTP_403_FORBIDDEN)
        list_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)