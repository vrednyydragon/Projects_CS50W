# Final Project

*Designing and implementing a web application of your own with Python and JavaScript.*

#### Overview

You can see the result of this work on youtube by the link: 
https://youtu.be/vAjL45NtobE

The final project I called HF(Healthy Food). This is not only a website where are collected recipes but a place where users can regulate and watch the results of everything they eating per day.  
In this web application, users can choose a specific nutritional goal, do calculations on a calculator for additional data. User has their account where they can change information about themselves, change image profile, they can see calculations results, add recipes that they like, create everyday eating history and check how many kcal, proteins, fats, carbs and sugar they ate per day.  
Users can choose tags of recipes as they want and combine searching with these tags.

In this web application, I made a huge work with database and Django ORM. I created 30 models and worked with them, they connected by foreign keys. It's doesn't like other projects that I did. First I had practice changing the language on the web application, it was interesting because I translated every word from Russian into English and all recipes, that I collected, was in Russian first. Then all data was saved in the database. Now HF has two languages English and Russian and the both of them works. 

Also, I applied Ajax for some requests from client to server and got a response.
Daily diagrams were created using SVG.

The database of this project is on the amazon server because I started my work before the update on 1 July 2020 and for that time were other requirements for the Final Project. But I rewrote all functionality of the web application for new requirements.

How did I decide to choose this topic? First of all, it was interesting for me and in the future, I hope it will work :)

***My project is satisfying such requirements:***
-  it sufficiently distinct from the other projects in this course and it doesn't base on the old CS50W Pizza project, and more complex than those.
-  it doesn't have a social network and it doesn't look like Project 4(Network). 
-   it is not an e-commerce site and distinct from Project 2(Commerce) because there no buy or sell services but only calculating eated food per day.
-  my web application utilized Django, there included at least 30 models on the back-end and it has JavaScript on the front-end.
- my web application is mobile-responsive.

***Folders and files:***
- hf_website - this folder contains:
	- migrations (models migrations)
	- static - this folder contains:
		- product_img folder and recipes_img folder, which contains images of recipes and products for web application;
		- index.js - file with JavaScript functions for the front-end;
		- styles.css - file contains different styles for decoration the front-end;
		- food9.jpg - background image for web application;
		- man.jpg, pen.jpg, scrollTopArrow.png, woman.jpg - images for web application.
	- templates - this folder contains main pages of web application:
		- base.html
		- calculator.html
		- index.html
		- login.html
		- one_recipe_page.html
		- recipes.html
		- register.html
		- user_profile.html
	- __init__.py
	- admin.py
	- apps.py
	- models.py
	- tests.py
	- urls.py
	- views.py - file that contains all server functions
- env.cmg - file with environment configuration variables
- media - folder contains users account images
- project4_final_v2020 - this folder contains:
	- __pycache__
	- __init__.py
	- asgi.py
	- settings.py - file with main settings of app
	- urls.py
	- wsgi.py
- templates - empty folder
-.gitignore - file that conteins hidden files or folders that don't need in git repository
- hf_translate.py - file for translating data from Russian to English and vice versa;
- import_tables.py - creating new tables for database if they don't exists;
- manage.py
- README.md - include a writeup describing of the project  

*My application easy to run from command string using commands:*
- env.cmg
- python manage.py runserver