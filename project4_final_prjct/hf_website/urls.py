from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("calculator", views.calculator, name="calculator"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("profile", views.user_profile, name="user_profile"),
    path("recipes", views.recipes, name="recipes"),
    path("one_recipe/<str:recipe_id>", views.one_recipe_page, name="one_recipe_page"),
    path("product/<str:product_uid>", views.product_page, name="product_page")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)