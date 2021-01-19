from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
from datetime import date

from .models import UsersLogin, UsersProfile, ItemAttributes, ItemImages, \
	ItemTags, Recepies, RecepiesIngredients, RecepiesInstructions, RelationUserMeal, \
	UsersMealAdditionals, ItemTranslations, RecepiTranslations, RecepiInstructionTranslations, \
	Components, ComponentsTranslations, ItemTranslations, ItemTypesCatalog, ItemsCatalog,\
	Languages, MeasureUnits, MeasureUnitsTranslations, Products, ProductComponents, ProductImages, ProductTags, \
	ProductTranslations, RecepiInstructionTranslations, RecepiTags, RecepiTranslations,\
	Tags, TagsCategory, TagsTranslations, UsersFoodLog

import decimal
from decimal import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import django.core.exceptions
from random import randint
import random

from django import forms
from django.db import connections, connection

from django.http import JsonResponse
from django.db.models.functions import Lower
from django.http import HttpResponseNotFound, HttpResponse
from django.http import Http404
from django.core.exceptions import ValidationError
import json as simplejson

import uuid

def index(request):
	if request.is_ajax():
		if "curr_language" in str(request):
		# if request.GET["curr_language"]:
			return JsonResponse(set_curr_lang(request))
	return render(request, "index.html", {"user_name": get_user_name(request.session.get("curr_user_id")),
	                                      "website_attributes": get_website_attributes(request)})

def calculator(request):
	if request.is_ajax():
		if "curr_language" in str(request):
		# if request.GET["curr_language"]:
			return JsonResponse(set_curr_lang(request))
	return render(request, "calculator.html", {"user_name": get_user_name(request.session.get("curr_user_id")),
	                                           "website_attributes": get_website_attributes(request)})

def register(request):
	if request.is_ajax():
		if "curr_language" in str(request):
			return JsonResponse(set_curr_lang(request))
	if not request.session.get("curr_user_id"):
		if request.method == "POST":
			user_name = request.POST["user_name"]
			user_mail = request.POST["email"]
			user_pass = request.POST["password"]
			user_pass2 = request.POST["password_2"]
			email_check = UsersLogin.objects.filter(email=user_mail)
			# print(f'register rows_check = {email_check}')
			# print(f'register rows_check = {type(email_check)}')
			if user_pass == user_pass2:
				if len(email_check) == 0:
					user_register = UsersLogin(name=user_name, \
					                           email=user_mail, \
					                           password=user_pass, \
					                           date_of_creation=datetime.datetime.now(), \
					                           login_flag=False)
					user_register.save()
					return render(request, "login.html", {"message": "Thank you for registering, please \
					                                        fill in the fields to enter the site."})
				else:
					return render(request, "login.html",
					              {"message": f"user with e-mail {user_mail} is already exists!"})
			else:
				return render(request, "register.html", {"message": "Oops, passwords don't match!"})

		return render(request, "register.html", {"website_attributes": get_website_attributes(request)})

	else:
		return HttpResponseRedirect(reverse("user_profile"))


def login(request):
	if request.is_ajax():
		if "curr_language" in str(request):
			return JsonResponse(set_curr_lang(request))
	if not request.session.get("curr_user_id"):
		if request.method == "POST":
			user_mail = request.POST["email"]
			user_pass = request.POST["password"]
			# print(f'user_mail = {user_mail}; user_pass = {user_pass} ')

			rows_check = UsersLogin.objects.filter(email=user_mail, password=user_pass)
			# print(f'user login row = {rows_check}')
			# print(f'len login row = {len(rows_check)}')
			if len(rows_check) == 0:
				return render(request, "login.html", {"message": "Oops, e-mail or password isn't correct."})
			else:
				request.session['curr_user_email'] = user_mail
				user_info = UsersLogin.objects.filter(email=request.session.get('curr_user_email')).get()
				print(f'user_info {user_info}')
				print(f'user_info {user_info.name}')
				request.session['curr_user_id'] = user_info.id_users
				user_info.login_flag = True
				user_info.save()
			# print(f"User profile : curr_user_email={request.session.get('curr_user_email')},\
			# 						curr_user_name = {request.session.get('curr_user_name')},\
			# 						curr_user_id = {request.session.get('curr_user_id')}")
			return HttpResponseRedirect(reverse("user_profile"))
		return render(request, "login.html", {"website_attributes": get_website_attributes(request)})
	else:
		return HttpResponseRedirect(reverse("user_profile"))


def logout(request):
	user_info = UsersLogin.objects.filter(email=request.session.get('curr_user_email')).get()
	user_info.login_flag = False
	user_info.save()
	del request.session['curr_user_email']
	del request.session['curr_user_id']
	return HttpResponseRedirect(reverse("index"))


def user_profile(request):
	if request.is_ajax():
		if "curr_language" in str(request):
			return JsonResponse(set_curr_lang(request))
	# print(f' method , request = {request} ')
	if request.session.get('curr_user_id'):
		user_id = request.session.get('curr_user_id')
		user_name = get_user_name(user_id)
		fs = FileSystemStorage()
		favorite_list = []
		check_user_id = UsersProfile.objects.filter(id_profile=user_id)
		if request.method == "POST":
			if check_user_id.exists():
				if "change_user_name" in request.POST:
					UsersLogin.objects.filter(pk=user_id).update(
						name=request.POST["change_user_name"])

				if request.FILES:
					myfile = request.FILES['download_img']
					check_img = UsersProfile.objects.get(id_profile=user_id).profile_img
					if check_img:
						uploaded_file_url = fs.url(check_img)
						print(uploaded_file_url)
						fs.delete(name=check_img)
					file_type = os.path.splitext(str(request.FILES['download_img']))[1]
					# print(f'file_type = {file_type}')
					user_filename = str(user_id) + "_" + get_user_name(user_id) + file_type
					filename = fs.save(user_filename, myfile)
					UsersProfile.objects.filter(id_profile=user_id).update(
						profile_img=user_filename)
				# if user wants change their information
				if "date_of_birth" in request.POST:
					UsersProfile.objects.filter(id_profile=user_id).update(
						date_of_birth=request.POST["date_of_birth"],
						gender=request.POST["gender"],
						user_height=request.POST["user_height"],
						user_weight=request.POST["user_weight"],
						type_of_food=request.POST["type_of_food"],
						activity_level=request.POST["activity_level"])
			else:
				user_profile = UsersProfile(
					id_profile=UsersLogin.objects.get(id_users=user_id),
					date_of_birth=request.POST["date_of_birth"],
					gender=request.POST["gender"],
					user_height=request.POST["user_height"],
					user_weight=request.POST["user_weight"],
					type_of_food=request.POST["type_of_food"],
					activity_level=request.POST["activity_level"])
				user_profile.save()
			return HttpResponseRedirect(reverse("user_profile"))
		if check_user_id.exists():
			us_profile_info = UsersProfile.objects.get(id_profile=user_id)
			us_birth_day = us_profile_info.date_of_birth
			us_gender = us_profile_info.gender
			us_height = us_profile_info.user_height
			us_weight = us_profile_info.user_weight
			type_of_food = us_profile_info.type_of_food
			us_activity = us_profile_info.activity_level
			us_age = user_age(us_birth_day)
			if us_profile_info.profile_img:
				# print("true")
				user_img_url = fs.url(us_profile_info.profile_img)
			else:
				user_img_url = ""
			# print(f'user_img_url = {user_img_url}')
			# print(f'us_age = {us_age}')
			calc_result = hf_calculator(us_age, us_gender, us_height, \
			                            us_weight, type_of_food, us_activity)
			favorite_meal = Recepies.objects.filter(usersmealadditionals__id_users=user_id,\
			                                        usersmealadditionals__relation_type=1).values('recepi_uid')
			if favorite_meal.exists():
				for favorite_obj in favorite_meal:
					# print(f'favorite_obj = {favorite_obj}')
					favorite_list.append(find_recipe_by_uid(request, favorite_obj['recepi_uid']))
			# print(f'favorite_list = {favorite_list}')
			page_obj = paginator_for_webpage(request, favorite_list, 6)
			eaten_food = UsersFoodLog.objects.filter(user_uid=user_id).values('recipe_uid','recipe_weight','food_time','date_creation')
			eaten_food_days_list_2 = {}
			all_nutrics_by_day = {}
			if eaten_food.exists():
				print(f'eaten_food = {eaten_food}')
				for meal in eaten_food:
					one_recipe = find_recipe_by_uid(request, meal["recipe_uid"])
					recipe_nutric_list = get_recipe_nutrics(request, one_recipe) # nutric in 100 g of recipe
					# print(f'users recipe_nutric_list 100g = {recipe_nutric_list}')
					# nutrics in current recipes weight
					for n in recipe_nutric_list:
						n[1] = round(n[1] / 100 * meal["recipe_weight"], 2)
					# print(f'users recipe_nutric_list {meal["recipe_weight"]} g = {recipe_nutric_list}')
					if meal["date_creation"] not in all_nutrics_by_day:
						all_nutrics_by_day[meal["date_creation"]] = recipe_nutric_list
					else:
						for i in recipe_nutric_list:
							for n in all_nutrics_by_day[meal["date_creation"]]:
								if i[0] in n:
									n[1] = round(n[1]+i[1], 2)
								else:
									n[1] = round(n[1], 2)
					recipe_name = find_recipe_by_uid(request, meal["recipe_uid"])
					# print(f'eaten recipe_name user = {recipe_name["name"]}')

					add_one_dict = {}
					if meal["date_creation"] not in eaten_food_days_list_2:
						# print(f'eaten_food_days_list_2 before = {eaten_food_days_list_2}')
						add_one_dict[meal["food_time"]] = [{
											"recipe_uid": recipe_name["uid_recipe"],
											"recipe_name": recipe_name["name"],
											"recipe_weight": meal["recipe_weight"]}]
						eaten_food_days_list_2[meal["date_creation"]] = add_one_dict
						# print(f'eaten_food_days_list_2 after = {eaten_food_days_list_2}')
					else:
						if meal["food_time"] not in eaten_food_days_list_2[meal["date_creation"]]:
							eaten_food_days_list_2[meal["date_creation"]][meal["food_time"]] = [{
																								"recipe_uid": recipe_name["uid_recipe"],
																								"recipe_name": recipe_name["name"],
							                                                                    "recipe_weight": meal["recipe_weight"]}]
						else:
							eaten_food_days_list_2[meal["date_creation"]][meal["food_time"]].append({
								"recipe_uid": recipe_name["uid_recipe"],
								"recipe_name": recipe_name["name"],
								"recipe_weight": meal["recipe_weight"]})
			# print(f'eaten_food_days_list_2 = {eaten_food_days_list_2}')
			print(f'all_nutrics_by_day = {all_nutrics_by_day}')
			context = {
				"user_name": user_name,
				"date_of_birth": str(us_birth_day),
				"user_age": us_age,
				"gender": us_gender,
				"user_height": us_height,
				"user_weight": us_weight,
				"type_of_food": type_of_food,
				"activity_level": us_activity,
				"user_hf_calc": calc_result,
				"user_img_url": user_img_url,
				"page_obj": page_obj,
				"website_attributes": get_website_attributes(request),
				"eaten_food2": eaten_food_days_list_2,
				"all_nutrics_by_day": all_nutrics_by_day
			}
		else:
			context = {"user_name": user_name,
			           "website_attributes": get_website_attributes(request)}
		return render(request, "user_profile.html", context)
	else:
		return HttpResponseRedirect(reverse("index"))


def recipes(request):
	print(f'recipes request = {request}')
	recipes_list = []
	search_list = []
	recipes_uid = []
	products_uid = []
	if request.is_ajax():
		# print(f'recipes request ajax  = {request}')
		if "curr_language" in str(request):
			return JsonResponse(set_curr_lang(request))
		if "choosen_tag_uid" in str(request):
			# print(f'choosen_tag_uid = {request.GET["choosen_tag_uid"]}')
			ch_tag_uid = request.GET["choosen_tag_uid"]
			add_tag_in_session(request, ch_tag_uid)#, ch_tag_name)
			data = {"flag":True}
			return JsonResponse(data)
		# print(f'choosen_tag_uid = {request.session.get("choosen_tags")}')
		if "deleted_tag_uid" in str(request):
			# print(f'deleted_tag_uid = {request.GET["deleted_tag_uid"]}')
			del_tag_uid = str(request.GET["deleted_tag_uid"]).replace('-', '')
			for one_tag in request.session['choosen_tags']:
				# print(f'one_tag = {one_tag}')
				if one_tag['choosen_tag_uid'] == del_tag_uid:
					# print("was deleted")
					request.session['choosen_tags'].remove(one_tag)
					request.session.modified = True

			# print(f'deleted request.session.get("choosen_tags") = {request.session.get("choosen_tags")}')
			data = {"flag": True}
			return JsonResponse(data)
		find_recipes = Recepies.objects.filter(recepitranslations__language_code=request.session['curr_website_lang']).\
										values('recepi_uid','recepitranslations__translation')#.all()#[:10]
		# print(f'find_recipes {find_recipes}')
		for obj in find_recipes:
			# print(f'obj find_recipes = {obj} ')
			search_list.append({"search_id": obj['recepi_uid'],
			                    "search_name": obj['recepitranslations__translation']})
		# print(f'search_list = {search_list}')
		data = {"recipe_list": search_list}
		return JsonResponse(data)
	# this is serch input
	if request.method == "POST":
		search_name = request.POST["txtSearch"]
		print(f'search_name = {search_name}')
		if len(request.session['choosen_tags']) > 0:
			recipes_uid, products_uid = recip_tags_exist(request, search_text=search_name)
		else:
			recipes_uid = Recepies.objects.filter( recepitranslations__language_code=request.session['curr_website_lang'], \
			                                      recepitranslations__translation__contains=search_name). \
				                                    values('recepi_uid').distinct().order_by('recepi_name')[:60]
			products_uid = Products.objects.filter(producttranslations__language_code=request.session['curr_website_lang'],\
			                                      producttranslations__translation__contains=search_name).\
									               values('product_uid').distinct().order_by('product_name')[:60]
		print(f' search {search_name} \n {recipes_uid}')
		if not recipes_uid.exists():
			context = {
				"search_message_err": f'"{search_name}" doesn\'t much any request',
				"user_name": get_user_name(request.session.get("curr_user_id")),
				"website_attributes": get_website_attributes(request)
			}
			return render(request, "recipes.html", context)
	else:
		if len(request.session['choosen_tags']) > 0:
			recipes_uid, products_uid = recip_tags_exist(request)
		else:
			recipes_uid = Recepies.objects.values('recepi_uid').order_by('recepi_name')[:60] #20 recipes
			products_uid = Products.objects.values('product_uid').order_by('product_name')[:60]
	rec_uid_list = []
	prod_uid_list = []
	for uid in recipes_uid:
		rec_uid_list.append(uid['recepi_uid'])
	for uid in products_uid:
		prod_uid_list.append(uid['product_uid'])
	rec_prod_list = sorted(rec_uid_list + prod_uid_list)
	# print(f'rec_prod_list = {rec_prod_list}')
	# print(f'len rec_prod_list = {len(rec_prod_list)}')
	for uid in rec_prod_list:
		recipes_list.append(find_recipe_by_uid(request, uid))
		# break
	page_obj = paginator_for_webpage(request, recipes_list, 12)  # Show 12 recipes per page
	tags_obj = Tags.objects.exclude(tag_category=None). \
		filter(tagstranslations__language_code=request.session['curr_website_lang']). \
		values_list('tag_uid','tag_category', 'tagstranslations__translation'). \
		order_by('tagstranslations__translation')
	tags_list = []
	# print(f'tags_list = {tags_obj}')
	filter_uid_list = ['fc3c49a8-cf20-49a5-87e6-f9219c7ec1f7', '9105a5fe-ed1d-4b8a-a358-d6d87da3dcc5', '66092bef-976d-4520-b41a-86e00e7fc75e']
	filter_tags_obj = Tags.objects.filter(tag_uid__in=filter_uid_list, tagstranslations__language_code=request.session['curr_website_lang']).\
									values('tag_uid','tagstranslations__translation')

	# print(f'filter_tags_obj = {filter_tags_obj}')
	for one_tag in tags_obj:
		tag_uid = one_tag[0].hex
		tag_category = one_tag[1]
		tag_name = one_tag[2]
		tags_list.append({'tag_uid':tag_uid,
		                  'tag_category':tag_category,
		                  'tag_name':tag_name
		                  })
	# print(f'selected tags = {request.session["choosen_tags"]}')
	new_tags_uid_list = []
	for n in request.session['choosen_tags']:
		new_tags_uid_list.append(n['choosen_tag_uid'])
	selected_tags_name = Tags.objects.filter(tag_uid__in=new_tags_uid_list, tagstranslations__language_code=request.session['curr_website_lang']).\
										distinct().values('tag_uid','tagstranslations__translation')
	print(f'selected_tags_name finish = {selected_tags_name}')
	context = {
		"page_obj": page_obj,
		"user_name": get_user_name(request.session.get("curr_user_id")),
		"tags": tags_list,
		"website_attributes": get_website_attributes(request),
		"selected_tags": selected_tags_name,
		"filter_tags": filter_tags_obj
	}
	return render(request, "recipes.html", context)

def one_recipe_page(request, recipe_id):
	recipe_uid = recipe_id
	print(f'one_recipe_page recipe_id = {recipe_uid}')
	print(f'one recipe request = {request}')
	if not Recepies.objects.filter(recepi_uid=recipe_uid).exists():
		raise Http404
	user_id = request.session.get("curr_user_id")
	fav_meal_flag = "0"
	if user_id:
		user_id_fk = UsersLogin.objects.get(id_users=user_id)
		favorite = RelationUserMeal.objects.get(id_relation=1)
		row_check = UsersMealAdditionals.objects.filter(id_users=user_id, id_meal=recipe_uid, relation_type=favorite)
		if row_check.exists():
			fav_meal_flag = "1"
	if request.is_ajax():
		if "curr_language" in str(request):
			return JsonResponse(set_curr_lang(request))
		# when user add\delete favorite recipe
		elif "flag" in str(request):
			flag_ajax = request.GET["flag"]
			one_rec_uid = Recepies.objects.get(recepi_uid=recipe_uid)
			save_dell_meal_to_fav(user_id_fk, one_rec_uid, flag_ajax, favorite)
		elif "add_to_eaten" in str(request):
			# print(f'added to eaten {request.GET["eat_recipe_uid"]}, {request.GET["eat_recipe_weight"]},{request.GET["food_time"]}')
			user_eat_meal = UsersFoodLog(
				user_uid=UsersLogin.objects.get(id_users=user_id),
				recipe_uid=Recepies.objects.get(recepi_uid=request.GET["eat_recipe_uid"]),
				recipe_weight=int(request.GET["eat_recipe_weight"]),
				food_time=request.GET["food_time"],
				date_creation=datetime.datetime.now()
			)
			user_eat_meal.save()
		elif "choosen_tag_uid" in str(request):
			ch_tag_uid = request.GET["choosen_tag_uid"]
			add_tag_in_session(request, ch_tag_uid)#, ch_tag_name)
			data = {"flag": True}
			return JsonResponse(data)

	one_recipe = find_recipe_by_uid(request, recipe_uid)
	recipe_nutric_list = get_recipe_nutrics(request, one_recipe)
	context = {
		"recipe_uid": recipe_uid,
		"user_name": get_user_name(user_id),
		"one_recipe": one_recipe,
		"btn_fav_value": fav_meal_flag,
		"website_attributes": get_website_attributes(request),
		"nutricients": recipe_nutric_list
	}
	return render(request, "one_recipe_page.html", context)

def product_page(request, product_uid):
	prod_uid =product_uid
	if not Products.objects.filter(product_uid=prod_uid).exists():
		raise Http404
	user_id = request.session.get("curr_user_id")
	one_product = find_recipe_by_uid(request, prod_uid)
	prod_nutric_list = one_prod_nutrics(request, prod_uid)
	if request.is_ajax():
		if "curr_language" in str(request):
			return JsonResponse(set_curr_lang(request))
	context = {
		"product_uid": prod_uid,
		"user_name": get_user_name(user_id),
		"product": one_product,
		"website_attributes": get_website_attributes(request),
		"nutricients":prod_nutric_list
	}
	return render(request, "product_page.html", context)

def hf_calculator(age, gender, height, weight, type_food, activity):
	# print(f'results1 {(age, gender, height, weight, type_food, activity)}')
	bmr_finish = 0
	man_coeff = 5
	woman_coeff = 161
	with_type_food = 0.2
	water_coeff = 30
	sugar_coeff = 0.05
	pr_f_carb = [0, 0, 0]

	# bmr - basal metabolic rate by Harris-Benedict's formula
	bmr = decimal.Decimal(9.99) * weight + decimal.Decimal(6.25) * height - decimal.Decimal(4.92) * age
	if (gender == "female"):
		bmr -= woman_coeff
	else:
		bmr += man_coeff
	bmr *= activity  # multiply on physical activity coeff
	if (type_food == "weight_loss"):
		bmr_finish = bmr - (bmr * decimal.Decimal(with_type_food))
		# 30 / 20 / 50
		pr_f_carb = prot_fat_carb_calc(0.3, 0.2, 0.5, bmr_finish)
	elif (type_food == "muscle_gain"):
		bmr_finish = bmr + (bmr * decimal.Decimal(with_type_food))
		# 35 / 30 / 55
		pr_f_carb = prot_fat_carb_calc(0.35, 0.3, 0.55, bmr_finish)
	# print(f'bmr_finish "weight_loss" = {bmr_finish}')
	elif (type_food == "weight_maintenance"):
		bmr_finish = bmr
		# 30 / 30 / 40
		pr_f_carb = prot_fat_carb_calc(0.3, 0.3, 0.4, bmr_finish)
	protein = pr_f_carb[0]
	fat = pr_f_carb[1]
	carb = pr_f_carb[2]
	calc_water = water_coeff * weight / 1000  # daily norm of water
	calc_sugar = decimal.Decimal(sugar_coeff) * bmr_finish / 4  # daily norm of sugar
	return {"calories": round(bmr_finish),
	        "protein": round(protein),
	        "fat": round(fat),
	        "carb": round(carb),
	        "water": round(calc_water, 2),
	        "sugar": round(calc_sugar)
	        }


def prot_fat_carb_calc(per_prot, per_fat, per_carb, bmr_finish):
	protein_kcal = 4  # 1g = 4kcal
	fat_kcal = 9  # 1g = 9kcal
	carb_kcal = 4  # 1g = 4kcal

	calc_protein = decimal.Decimal(per_prot) * bmr_finish / protein_kcal
	calc_fat = decimal.Decimal(per_fat) * bmr_finish / fat_kcal
	calc_carb = decimal.Decimal(per_carb) * bmr_finish / carb_kcal

	return [calc_protein, calc_fat, calc_carb]


def user_age(birthday):
	today = date.today()
	age = today.year - birthday.year
	if today.month < birthday.month:
		age -= 1
	elif today.month == birthday.month and today.day < birthday.day:
		age -= 1
	return age


def find_recipe_by_uid(request, rec_uid):
	recip_dict = {}
	# print(f'rec_uid = {rec_uid}')
	# print(f'find_recipe_by_uid request = {request}')
	# print(request.session['curr_website_lang'])
	website_language = request.session['curr_website_lang']
	# print(f'website_language = {website_language}')
	recipe_instruction = ()
	if Recepies.objects.filter(recepi_uid=rec_uid).exists():
		# print(f'rec_uid = {rec_uid}')
		recipe_object = Recepies.objects.get(recepi_uid=rec_uid)
		# print(f'recipe_object = {recipe_object}')
		recepitranslations_set = recipe_object.recepitranslations_set
		# print(f'recepitranslations_set = {recepitranslations_set}')
		recipe_name = recepitranslations_set.filter(language_code=website_language).values('translation')[0]["translation"]
		# print(f'recepitranslations_translation = {recipe_name}')
		ingredients_set = recipe_object.recepiesingredients_set
		recipe_ingredients = ingredients_set.filter(product_uid__producttranslations__language_code=website_language, \
		                                            measure_unit_uid__measureunitstranslations__language_code=website_language). \
											values_list('product_uid','product_uid__producttranslations__translation', 'amount', \
											           'measure_unit_uid__measureunitstranslations__translation', \
											            'measure_unit_uid'). \
											order_by('product_uid__producttranslations__translation')
		# print(f'ingredients_set = {recipe_ingredients}')
		if "one_recipe" in str(request):
			instruction_set = recipe_object.recepiesinstructions_set
			recipe_instruction = instruction_set.filter(recepiinstructiontranslations__language_code=website_language). \
											values_list('step_number','recepiinstructiontranslations__translation'). \
											order_by('step_number')
			# print(f'recipe_instruction = {recipe_instruction}')
		recipe_img = recipe_object.itemimages_set.filter(item_uid=rec_uid).values("image_name")
		curr_img = "recipes_img/" + [image["image_name"] for image in recipe_img][0]
		# print(curr_img)
		recipe_tags = recipe_object.recepitags_set.filter(tag_uid__tagstranslations__language_code=website_language).\
													values('tag_uid','tag_uid__tagstranslations__translation'). \
													order_by('tag_uid__tagstranslations__translation')
		data_dict = {
			"uid_recipe": rec_uid, # uid_recipe,
			"name": recipe_name,
			"ingredients": recipe_ingredients,
			"instructions": recipe_instruction,
			"img": curr_img,
			"tags": recipe_tags,
			"type": "recipe"
			}
	elif Products.objects.filter(product_uid=rec_uid).exists():
		# print(f'prod_uid = {rec_uid}')
		prod_object = Products.objects.get(product_uid=rec_uid)
		producttranslations_set = prod_object.producttranslations_set
		prod_name = producttranslations_set.filter(language_code=website_language).values('translation')[0]['translation']
		# print(f'prod name = {prod_name}')
		prod_img = prod_object.productimages_set.filter(product_uid=rec_uid).values("image_name")
		curr_img = "product_img/" + [image["image_name"] for image in prod_img][0]
		prod_tags = prod_object.producttags_set.filter(tag_uid__tagstranslations__language_code=website_language). \
								values('tag_uid','tag_uid__tagstranslations__translation'). \
								order_by('tag_uid__tagstranslations__translation')
		data_dict = {
			"uid_recipe": rec_uid, #uid_prod,
			"name": prod_name,
			"img": curr_img,
			"tags": prod_tags,
			"type": "product"
		}
	return data_dict

def get_user_name(user_id):
	if user_id:
		user_info = UsersLogin.objects.get(id_users=user_id)
		user_name = user_info.name
		return user_name

def save_dell_meal_to_fav(user_id_fk, recipe_id, flag_ajax, type_relations):
	""" add/dell meal to/from favorite"""
	favorite = RelationUserMeal.objects.get(id_relation=1)
	if flag_ajax == "true":
		user_fav_meal = UsersMealAdditionals(
			id_users=user_id_fk,
			relation_type=favorite,
			id_meal=recipe_id
			)
		user_fav_meal.save()
	else:
		UsersMealAdditionals.objects.filter(id_users=user_id_fk, id_meal=recipe_id, relation_type=favorite).delete()

def paginator_for_webpage(request, list, count):
	paginator = Paginator(list, count)  # Show 10 recipes per page
	page = request.GET.get('page')
	try:
		page_obj = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		page_obj = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		page_obj = paginator.page(paginator.num_pages)

	return page_obj

def get_website_attributes(request):
	'''web site attributes with current language'''
	# print(f'curr_website_lang 1 = {request.session.get("curr_website_lang")}')
	if not request.session.get('curr_website_lang'):
		request.session['curr_website_lang'] = "en"
	# print(f'curr_website_lang 2 = {request.session.get("curr_website_lang")}')
	db_attr_obj = ItemTranslations.objects.filter(table_source='website_text_attributs', \
	                                              language_code=request.session.get('curr_website_lang'))
	return db_attr_obj


def set_curr_lang(request):
	request.session['curr_website_lang'] = request.GET["curr_language"]
	print(f'curr_website_after changing= {request.session.get("curr_website_lang")}')
	data = {"current_language": request.session.get('curr_website_lang')}
	return data

def is_valid_uuid(val):
	'''from hex type to uuid type'''
	try:
		return uuid.UUID(str(val))
	except ValueError:
		return None

def one_prod_nutrics(request, product_uid):
	''' get nutricients for one product '''
	for_nutric_table = [1, 36, 29, 28, 26] #, 49, 2, 5, 3, 25]
	product_nutric_list = ProductComponents.objects.filter(product_uid=product_uid, \
	                                                   component_uid__componentstranslations__language_code=request.session['curr_website_lang'], \
	                                                   measure_unit_uid__measureunitstranslations__language_code=request.session['curr_website_lang'],\
	                                                   component_uid__component_id__in=for_nutric_table). \
												values_list('component_uid__componentstranslations__translation', 'amount', \
											                'measure_unit_uid__measureunitstranslations__translation'). \
												order_by('component_uid__componentstranslations__translation')
	return product_nutric_list

def recip_tags_exist(request, search_text=None):
	''' get query of products and recipes when tags choosen in serching field or by choosing tags '''
	tags_uid_list = []
	for tag in request.session['choosen_tags']:
		tags_uid_list.append(is_valid_uuid(tag['choosen_tag_uid']))
	if search_text is None:
		recipes_uid = Recepies.objects.filter(recepitags__tag_uid__in=tags_uid_list).distinct().values('recepi_uid'). \
			              order_by('recepi_name')[:60]
		products_uid = Products.objects.filter(producttags__tag_uid__in=tags_uid_list).distinct().values('product_uid'). \
			               order_by('product_name')[:60]
	else:
		recipes_uid = Recepies.objects.filter(recepitags__tag_uid__in=tags_uid_list, \
		                                      recepitranslations__translation__contains=search_text).\
						              distinct().values('recepi_uid'). \
						              order_by('recepi_name')[:60]
		products_uid = Products.objects.filter(producttags__tag_uid__in=tags_uid_list,\
		                                       producttranslations__translation__contains=search_text).\
						               distinct().values('product_uid'). \
						               order_by('product_name')[:60]
	return recipes_uid, products_uid

def add_tag_in_session (request, ch_tag_uid): #, ch_tag_name):
	if 'choosen_tags' not in request.session:
		request.session['choosen_tags'] = [ch_tag_uid]
	else:
		if ch_tag_uid not in request.session['choosen_tags']:
			request.session['choosen_tags'].append({'choosen_tag_uid': ch_tag_uid})
			request.session.modified = True


def get_recipe_nutrics(request, one_recipe):
	''' get recipes nutrics per 100g of recipe'''
	convert_in_g = {
			'9ec166d9-f14a-4f16-86d5-638f4428b628': 50,
			'5aed1573-aff6-4a7e-90a4-ad93035047e4': 1,
			'1709b265-c163-4859-8583-c01b00f0f74d': 1000,
			'c1efef6d-f9c6-4652-b682-b93f686053a2': 50,
			'0bea224b-6792-4da8-8359-6dbfc93f2085': 200,
			'edc21330-9816-4ff6-a611-3d50409cfcbe': 1000,
			'e9796977-bd1b-4a42-a0a9-65de581ec887': 5,
			'91204099-0c3f-468a-8d03-1a1b48b350e2': 20,
			'16e19334-cbfb-44c4-9225-391a2627066c': 450,
			'0f797ea0-04cc-48b8-b7b8-6ba3d527780f': 2,
			'42c31765-e394-4b46-a11e-7e6eae02ffc8': 200,
			'4ca4b06c-65bf-4d64-8dc9-9ecc8e502303': 0.000001,
			'2b7b7c34-3b01-4d94-b021-c80ebb796894': 50,
			'c2530c18-bee8-4c5a-b39c-edf1a8c16d35': 10,
			'15bffade-9868-46a8-839c-fd6c22e3f7a1': 200,
			'5865c5db-7f8b-4556-acc8-6043676fdbce': 0.001
		}
	recipe_nutric_list = []
	summary_weight_recipe = 0
	ingredients = one_recipe['ingredients']
	# print(f' one recipe ingredients === {ingredients}')
	for one_ingr in ingredients:
		new_nutric_list = []
		ingr_uid = one_ingr[0]
		ing_nutric_list = one_prod_nutrics(request, ingr_uid)
		# print(f'product name = {one_ingr[1]}')
		#converting measure values in to the g
		ing_gram_value = 0
		for key in convert_in_g:
			if str(one_ingr[4]) == key:
				ing_gram_value = one_ingr[2] * convert_in_g[key]
			elif str(one_ingr[4]) == 'a002e67f-8462-40db-a6fa-1d089b5f2a45':
				ing_gram_value = one_ingr[2]
		# print(f'ing_gram_value = {ing_gram_value}')
		summary_weight_recipe += ing_gram_value
		# from tuple in list
		for n in ing_nutric_list:
			new_nutric_list.append(list(n))
		# print(f'new_nutric_list tupple = {new_nutric_list}')
		for n in new_nutric_list:
			n[1] = n[1]/100 * ing_gram_value
		# print(f'new_nutric_list with current gramm value = {new_nutric_list}')
		if len(recipe_nutric_list) == 0:
			recipe_nutric_list = new_nutric_list
			# print(f'recipe_nutric_list = {recipe_nutric_list}')
		else:
			count = 0
			for i in new_nutric_list:
				# print(f'new_nutric_list i = {i}')
				for n in recipe_nutric_list:
					# print(f'new_nutric_list n = {n}')
					if i[0] in n:
						n[1] = round(n[1] + i[1], 2)
						# print(f'rounded and summ {n[1]}')
					else:
						n[1] = round(n[1], 2)
						# print(f'just rounded {n[1]}')

	# print(f'----recipe_nutric_list before = {recipe_nutric_list}')
	# print(f'recipe weight = {summary_weight_recipe} g')

	# nutricients in 100 g of recipe
	for n in recipe_nutric_list:
		n[1] = round(n[1]*100 / summary_weight_recipe, 2)
	# print(f'----for 100 g recipe_nutric_list = {recipe_nutric_list}')
	return recipe_nutric_list
