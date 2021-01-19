from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("menu/<str:menu_position>", views.menu, name="menu"),
	path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("order", views.user_basket, name="order"),
    path("add_in_basket/<str:menu_position>/<str:id_position>/<str:price_category>/<str:topping_list>",\
    		views.add_in_basket, name="add_in_basket"),
    path("clear_basket", views.clear_basket, name="clear_basket"),
    path("order_confirmed", views.send_order, name="order_confirmed"),
    path("order_status/<str:ord_numb>/<str:status>", views.change_ord_status, name="order_status"),
    path("count/<str:dish_id>/<str:count>", views.change_count, name="count")

]
