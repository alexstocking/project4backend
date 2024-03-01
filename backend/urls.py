"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from main_app import views
from main_app.views import current_user, CartProductCreateAPIView, CartProductRemoveAPIView, ListProductCreateAPIView, ListProductRemoveAPIView, NewCartRequest


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'carts', views.CartViewSet)
router.register(r'cartproducts', views.CartProductViewSet)
router.register(r'lists', views.ListViewSet)
router.register(r'listproducts', views.ListProductViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'requests', views.RequestViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name ='auth_logout'),
    path('signup/', views.SignUpView.as_view(), name ='auth_register'),
    path('account/edit/', views.EditAccountView.as_view(), name ='account_edit'),
    path('newrequest/', views.NewRequest.as_view(), name ='new_request'),
    path('request/edit/<int:pk>/', views.EditRequest.as_view(), name ='edit_request'),
    path('api/current_user/', current_user, name='current_user'),
    path('cart/add/', CartProductCreateAPIView.as_view(), name='cart-add'),
    path('cart/remove/<int:pk>/', CartProductRemoveAPIView.as_view(), name='cart-remove'),
    path('list/add/', ListProductCreateAPIView.as_view(), name='list-add'),
    path('list/remove/<int:pk>/', ListProductRemoveAPIView.as_view(), name='list-remove'),
    path('newcartrequest/', NewCartRequest.as_view(), name='new_cart_request'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]