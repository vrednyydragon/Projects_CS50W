from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import MenuPosition, MenuTable, Orders, OrderDetails
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User


# orders_status_list = ["in basket","new", "in procces", "closed"]

def index(request):
	if not request.user.is_authenticated:
		return render(request, "login.html", {"message": None, "user": None})
	all_orders = Orders.objects.exclude(order_status="in basket")
	order_details = OrderDetails.objects.exclude(order_number__order_status="in basket")
	context = {
		"menu_list": MenuPosition.objects.values_list(),\
		"user": request.user,\
		"total_cost": order_prise(request.user),\
		"all_orders": all_orders,\
		"order_details": order_details
	}
	return render(request,"index.html", context) 

def menu(request, menu_position):
	menu_table = list(MenuTable.objects.filter(category=menu_position).values())
	# print(menu_table)
	toppings = MenuTable.objects.filter(category="Toppings").values()
	price_lrg = MenuTable.objects.filter(category=menu_position).values("price_lrg")
	# print(f'price_lrg = {price_lrg}')
	flag = False
	for price in price_lrg:
		# print(price["price_lrg"])
		if price["price_lrg"] != None:
			flag = True
			break
	context = {\
				"user": request.user,\
				"menu_position":menu_position,\
				"menu_list": MenuPosition.objects.values_list(),\
				"menu_table": menu_table,\
				"toppings":toppings,\
				"flag": flag,\
				"total_cost": order_prise(request.user)
	}
	return render(request,"menu.html", context) 

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "login.html", {"message": "Invalid credentials.",\
        										"user": None} )

def logout_view(request):
    logout(request)
    context = {
		"message": "Logged out.",\
		"user": None
	}
    return render(request, "login.html", context)

def register_view(request):
	if request.method == "POST":
		print("hi")
		print(request)
		user_name = request.POST["user_name"]
		first_name = request.POST["first_name"]
		last_name = request.POST["last_name"]
		email = request.POST["email"]
		password = request.POST["password"]
		password_2 = request.POST["password_2"]
		if password != password_2:
			return render(request, "register.html",\
						 {"message":"Oops, passwords don't match!", "user": None})
		user = User.objects.create_user(username=user_name, email=email, password=password)
		user.first_name = first_name
		user.last_name = last_name
		user.save()
		return render(request, "login.html", {"message":"Thank for register.\
												 Fill in the fields to log in","user": None}) 
	return render(request,"register.html", {"user": None}) 

def add_in_basket(request, menu_position, id_position, price_category, topping_list):
	id_user1= User.objects.get(username=request.user).id
	# print("id_user1")
	check_order(request.user) 
	order_number = Orders.objects.filter(user_id=request.user, order_status="in basket").get().order_number
	fk_order_number = Orders.objects.get(order_number=order_number)
	fk_id_position = MenuTable.objects.get(id_position=id_position)
	# print(fk_order_number, fk_id_position)
	# if menu category doesn't have toppings
	if topping_list == "None":
		price_list = MenuTable.objects.filter(id_position=id_position).values(price_category)
		price_for_one = price_list[0][price_category]
		add_dish(fk_order_number, fk_id_position, price_for_one)
	# if menu category has toppings
	else:
		price_list = MenuTable.objects.filter(id_position=id_position).values(price_category)
		price_for_one = price_list[0][price_category]
		add_dish(fk_order_number, fk_id_position, price_for_one)
		pizza_position_list = MenuTable.objects.filter(category=menu_position).values("dish_name")
		# print(f'pizza_position = {pizza_position_list}')
		topping_list1 = topping_list.split(",")
		#add toppings in Order
		for n in topping_list1:
			fk_id_position1 = MenuTable.objects.get(id_position=n)
			topping_for1 = OrderDetails.objects.filter(order_number=fk_order_number,dish_id=id_position).first()
			add_dish(fk_order_number, fk_id_position1,topping_for=topping_for1 )
	return menu(request, menu_position)

def user_basket(request):
	check_order(request.user)
	user_order = Orders.objects.filter(user=request.user, order_status="in basket").get()
	order_number = user_order.order_number
	# print(f'order_number = {order_number}')
	user_basket_list = OrderDetails.objects.filter(order_number=order_number)#.order_by('-dish_id')
	order_list = []
	new_order_list = []
	new_order_list2 = []
	for obj in user_basket_list:
		# print(\
		# 		f'dish category: {obj.dish_id.category}; ' +\
		# 		f'dish name: {obj.dish_id.dish_name}; ' +\
		# 		f'dish price: {obj.price}; '+\
 	# 			f'topping for: {obj.topping_for}'\
 	# 			)
		order_list.append({
			"dish_category":obj.dish_id.category,\
			"dish_name":obj.dish_id.dish_name,
			"dish_price":obj.price,\
			"topping_for":obj.topping_for,\
			"dish_id":obj.dish_id.id_position\
			})

	for dict1 in order_list:
		if dict1 not in new_order_list:
			new_order_list.append(dict1)
			dict2 = dict1.copy() 
			dict2["count"] = 1
			new_order_list2.append(dict2)
		else:
			# print(new_order_list2[0])
			for dict2 in new_order_list2:
				if dict2['dish_name'] == dict1['dish_name'] and\
					dict2['dish_price'] == dict1['dish_price']:
					dict2["count"] += 1
	
	for ord_dict in new_order_list2:
		if ord_dict['dish_category'] != "Toppings":
			ord_dict["total_price"] = ord_dict['count']*ord_dict['dish_price']

	# new_order_list2={"dish_category"
	# 					'dish_name'
	# 					'dish_price'
	# 					'topping_for'
	# 					'count'
	# 					'total_price'
	# 					}
	user_old_orders = Orders.objects.filter(user=request.user).exclude(order_status="in basket")
	# print(f'user_old_orders = {user_old_orders}')
	old_order_dict = []
	for old_order in user_old_orders:
		list_= []
		old_order_list = OrderDetails.objects.filter(order_number=old_order.order_number)
		for obj in  old_order_list:
			list_.append([obj.dish_id.category, obj.dish_id.dish_name, obj.price])
		old_order_dict.append({"order_number":old_order.order_number,\
							"order_status":old_order.order_status,\
							"value":list_})
	# print(new_order_list2)
	context = {
				"user": request.user,\
				"menu_list": MenuPosition.objects.values_list(),\
				"order_list": new_order_list2,\
				"total_cost": order_prise(request.user),\
				"user_old_orders": old_order_dict
	}
	return render(request, "basket.html", context) 

def clear_basket(request):
	order_number = Orders.objects.get(user=request.user, order_status="in basket").order_number
	basket = OrderDetails.objects.filter(order_number=order_number)
	basket.delete()
	return(user_basket(request))

def send_order(request):
	order_number = Orders.objects.get(user=request.user, order_status="in basket")
	order_number.order_status = "new"
	order_number.save()
	# check_order(request.user)
	return(user_basket(request))

def change_ord_status(request, ord_numb, status):
	order = Orders.objects.get(order_number=ord_numb)
	order.order_status = status
	order.save()
	return index(request)

def change_count(request, dish_id, count):
	position = OrderDetails.objects.filter(order_number__order_status="in basket",\
										order_number__user__username=request.user,\
										dish_id__id_position=dish_id).first()
	if count == "minus":
		position.delete()
	else:
		fk_order_number = Orders.objects.get(user__username=request.user, order_status="in basket")
		fk_id_position = MenuTable.objects.get(id_position=dish_id)
		add_dish(fk_order_number, fk_id_position, price_for_one = position.price)
	return(user_basket(request))

# function save values in OrderDetails 
def add_dish(fk_order_number, fk_id_position, price_for_one=None, topping_for=None):

	order_details = OrderDetails(order_number=fk_order_number,\
										dish_id=fk_id_position,\
										price=price_for_one,\
										topping_for=topping_for)
	order_details.save()

def order_prise(user_id):
	check_order(user_id)
	order_price = 0
	user_order = Orders.objects.filter(user_id=user_id, order_status="in basket").get()
	user_ord_numb = user_order.order_number
	order_list = OrderDetails.objects.filter(order_number=user_ord_numb)
	if user_order:
		for one_dish in order_list:
			if one_dish.dish_id.category != "Toppings":
				order_price += one_dish.price
	return order_price

def check_order(user_id):
	order_list_ = Orders.objects.filter(user_id=user_id, order_status="in basket").values()
	if len(order_list_) == 0:
		user_order = Orders(user=user_id, order_status="in basket")
		user_order.save()

