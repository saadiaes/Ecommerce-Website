from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.index.as_view(),name='index'),
    path('produits/',views.produits,name='produits'),
    path('<int:id>/',views.detail,name='detail'),
    path('checkout/',views.checkout,name='checkout'),
    
    # PANIER URLS
    path('Shopping-cart',views.ShoppingCartDetail.as_view(),name="cart"),
    path('add-to-cart', views.addTocart.as_view(), name="add-to-cart"),
    path('delete-from-cart',views.delete_cart_item,name='delete-from-cart'),
    path('update-cart',views.update_cart_item,name='update-cart'),
]
