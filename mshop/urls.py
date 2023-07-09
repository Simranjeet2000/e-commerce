from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index , name = "MegaShop"),
    path("productpage/", views.productpage , name = "ProductPage"),
    path("search/", views.search , name = "Search"),
    path("about/", views.about , name = "AboutUs"),
    path("checkout/", views.checkout , name = "Checkout"),
    path("cart/", views.cart , name = "cart"),
    path("account/", views.account , name = "account"),
    path("login/", views.login , name = "login"),
    path("logout/", views.logout , name = "logout"),
]
