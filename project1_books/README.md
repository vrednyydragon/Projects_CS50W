# Project 1: Books

***Web Programming with Python and JavaScript***

You can see the result of this work on youtube by the link: 
https://youtu.be/12me8IB22sw

#### Overview

In this project, I built a book review website. Users will be able to register for the website and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. I also used a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via the website’s API.

For this project, I set up a PostgreSQL database to use with this application. I used a database hosted by Heroku, an online web hosting service.

***Files and folders:***

- .gitignore - the file containing a list of files not important for this project

- import.py - the file with programm which create table "books" and filled it of data from file books.csv and create tables "users" and "reviews"

- application.py - Flask code (working script) which contains the functions for the website

- books.csv - table for database

- templates:
	- index.html - template file which contains the registration page
	- login.html - template file which contains the login page
	- layout.html - template file which contains layouts
	- book_page.html - template file which contains the book page
	- books_searching.html - template file which contains the books searching page

- static:
	- goodreads.png - picture from goodreads website used in book page
	- styles.css - css file which contains main stylesheets with different CSS properties

**How to run:**

- Download the project1_books

- In a terminal window, navigate into your project1_books directory

- Run pip3 install -r requirements.txt in your terminal window to make sure that all of the necessary Python packages are installed

- Set the environment variable FLASK_APP to be application.py. On a Mac or on Linux, the command to do this is export FLASK_APP=application.py. On Windows, the command is instead set FLASK_APP=application.py. You may optionally want to set the environment variable FLASK_DEBUG to 1, which will activate Flask’s debugger and will automatically reload your web application whenever you save a change to a file.

- set DATABASE_URL=postgres://bkctkzncoaiuoi:bc7af65da1075e66d6d3f97f60584a249b82f82367db00cc35349bb38741bd69@ec2-107-21-126-201.compute-1.amazonaws.com:5432/destd2oum5btae

- Run _flask run_ to start up the Flask application

- If you navigate to the URL provided by flask, you should see the start page of the application








