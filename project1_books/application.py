import os
import time 
import requests

from flask import Flask, session, render_template, request, flash, redirect, url_for, jsonify, abort  #make_response
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
	raise RuntimeError("DATABASE_URL is not set")
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=["GET","POST"])
def index():
	'''filling the registration form for new user'''
	if request.method == "POST":
		session["in_usr_name1"] = request.form.get("in_usr_name")
		session["email1"] = request.form.get("email")
		print (session["in_usr_name1"])
		print (session["email1"])
		rows_check = db.execute("SELECT email FROM users WHERE email = :p_email",
			{"p_email":request.form.get("email")})
		email_check = rows_check.fetchone()
		# print("db_email <{}>".format(email_check))
		# checking passwords into matching during registration
		if request.form.get("password") == request.form.get("psw-repeat"):
			# Insert register into DB
			if email_check is None:
				db.execute("INSERT INTO users (name, email, password,date_of_creation)\
				 VALUES (:name, :email, :password, current_timestamp)",
					{"name":session["in_usr_name1"],
					"email":session["email1"], 
					"password":request.form.get("password"),
					})
				# print('exec insert')
				db.commit() # Commit changes to database
				# print('exec commit')
				flash('Thank you for registering, please fill in the fields to enter the site.')
				return render_template("login.html")
			else:
				# print('user already exists')
				flash(f'user with e-mail {request.form.get("email")} is already exists!')
				return render_template("login.html")
		else: 
			flash('Oops, passwords do not match!')
			return render_template("index.html",in_usr_name1=session.get("in_usr_name1"), email1=session.get("email1"))
			# error = 'Oops, passwords do not match'
			# return render_template("index.html", error=error, in_usr_name1=session.get("in_usr_name1"), email1=session.get("email1"))
	return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
	''' when registration is completed you need to re-fill the form 
	to enter the page'''
	us_mail = request.form.get("email")
	us_pass = request.form.get("password")
	# print("us_mail <{}>".format(us_mail))
	# print("us_pass <{}>".format(us_pass))
	if request.method == "POST":
		rows_check_m = db.execute("SELECT name FROM users WHERE email = :us_email \
		and password = :us_pass",{"us_email":request.form.get("email"), "us_pass":request.form.get("password")})
		r_row = rows_check_m.fetchone()
		if r_row is None:
			flash('Oops, email or password is not correct.')
			return render_template("login.html")
			# error = 'Oops, email or password is not correct.'
			# return render_template("login.html", error=error)
		else:
			session["curr_user_name"] =r_row[0]
			session["curr_email"] = us_mail
			# print('email and pass match with database')
			return redirect(url_for("books_searching"))
	return render_template("login.html")

@app.route("/logout")#, methods=["GET"])
def logout():
    """ Logout user """
    session.clear()
    return redirect(url_for("index"))

@app.route("/books_searching",methods=["GET", "POST"])
def books_searching():
	""" books serching """
	if request.method == "POST":
		column_to_select = str(request.form.get("search_list"))
		value_to_select = request.form.get("serch_text")
		# print(column_to_select)
		# print(value_to_select)
		sql_query = ""
		# if column_to_select == "isbn" or column_to_select == "year":
		if column_to_select == "year":
			sql_query = "SELECT * FROM books WHERE ("+column_to_select+") = (:param) "
		else:
			sql_query = "SELECT * FROM books WHERE  upper("+column_to_select+") like upper(:param) "
			value_to_select = "%"+value_to_select+"%"
		serch_row = db.execute(sql_query,{"param":value_to_select})
		serch_row_f = serch_row.fetchall()
		session["curr_isbns"]  = serch_row_f
		# print(serch_row_f)
		len_serch_row = 1 if len(serch_row_f) > 0 else None
		# checkin if book in db
		if len_serch_row is None:
			flash(f'Oops, there no "{request.form.get("serch_text")}" in "{column_to_select}"')
			return render_template("books_searching.html", rows_exists = 0, \
				cur_user_name=session["curr_user_name"],serch_text=request.form.get("serch_text"))
			# error = f'Oops, there no "{request.form.get("serch_text")}" in "{column_to_select}"'
			# return render_template("books_searching.html", error=error, rows_exists = 0)
		else:
			if request.form.get("for_book_page") == "0":
				print("for_book_page = 0")
			else:
				session["_isbn"] = request.form.get("for_book_page")
				print(f'_isbn = {session["_isbn"]}')
				return redirect(url_for("book_page"))

			return render_template("books_searching.html", rows = serch_row_f,\
			rows_exists= len_serch_row, cur_user_name=session["curr_user_name"],\
			serch_text=request.form.get("serch_text"))

	return render_template("books_searching.html", cur_user_name=session["curr_user_name"])

@app.route("/book_page",methods=["GET", "POST"])
def book_page():
	''' This page about book is selected by the user '''
	if request.method == "GET":
		print(f' request.method <"{request.method}">')
		_isbn = session["_isbn"]
		book_from_dbt1 = db.execute("SELECT * FROM books WHERE isbn = :_isbn", {"_isbn":_isbn})
		session["book_info_dbt"] = book_from_dbt1.fetchone()
		book_info_dbt = session["book_info_dbt"]
		# print("book_page.book_info_dbt")
		# print(book_info_dbt)
		session["book_isbn"] = book_info_dbt[0]
		session["book_title"] = book_info_dbt[1]
		session["book_author"] = book_info_dbt[2]
		session["book_year"] = book_info_dbt[3]
		KEY = "nJi51HnrSYGPgaJV6cbVFw"
		res = requests.get("https://www.goodreads.com/book/review_counts.json",\
		params={"key": KEY, "isbns": _isbn})
		good_reads_res = res.json() # json of book from goodreads.com
		
		for keys in good_reads_res.get("books"):
			session["ratings_count_js"] = keys["ratings_count"]
			session["average_rating_js"] = keys["average_rating"]
		# return render_template("book_page.html", some_data = _isbn, isbn_of_b= session["book_isbn"],\
		# title_of_b = session["book_title"], author_of_b=session["book_author"], year_of_b= session["book_year"],\
		# ratings_count_gr = session["ratings_count_js"], average_rating_gr = session["average_rating_js"],\
		# public_reviews = session['all_reviews'])
	if request.method == "POST":
		print(f' request.method <"{request.method}">')
		# print(request.form.get("user_review"))
		session["user_review"] = request.form.get("user_review")
		session["user_rate"] = int(request.form.get("rate_list"))
		# print(request.form.get("rate_list"))
		rows_check = db.execute("SELECT users_email, books_isbn FROM reviews WHERE users_email = :p_email and \
		books_isbn = :books_isbn",	{"p_email":session["curr_email"], "books_isbn":session["book_isbn"]})
		email_check = rows_check.fetchone()
		# print(f"email_check = {email_check}")
		user_name = db.execute("SELECT name FROM users WHERE email = :p_email",
			{"p_email":session["curr_email"]})
		user_name = user_name.fetchone()
		if email_check is None:
			# filling in the table reviews
			db.execute("INSERT INTO reviews (books_isbn, users_email, date_of_review, review, grid)\
			VALUES (:books_isbn, :users_email, current_timestamp , :review, :grid)",
			{"books_isbn" :session["book_isbn"],
			"users_email":session["curr_email"], 
			"review" :session["user_review"],
			"grid" :session["user_rate"]
			})
			db.commit()
		else:
			flash("You have already submitted one comment!")
			flash(" Only one comment for one book!")
		# return render_template("book_page.html", some_data = session["_isbn"], isbn_of_b= session["book_isbn"],\
		# title_of_b = session["book_title"], author_of_b=session["book_author"], year_of_b= session["book_year"],\
		# ratings_count_gr = session["ratings_count_js"], average_rating_gr = session["average_rating_js"],\
		# public_reviews = session['all_reviews'])
	
	# show all reviews for this book
	all_reviews = db.execute("SELECT users.name, grid, review  FROM reviews JOIN users ON users.email =users_email \
		WHERE reviews.books_isbn = :books_isbn",\
		{"books_isbn" :session["book_isbn"]})
	session['all_reviews'] = all_reviews.fetchall()
	# print(f"all_reviews {session['all_reviews']}")

	return render_template("book_page.html", some_data = session["_isbn"], isbn_of_b= session["book_isbn"],\
	title_of_b = session["book_title"], author_of_b=session["book_author"], year_of_b= session["book_year"],\
	ratings_count_gr = session["ratings_count_js"], average_rating_gr = session["average_rating_js"],\
	public_reviews = session['all_reviews'], cur_user_name=session["curr_user_name"])
	# return render_template("book_page.html")

@app.route("/api/<isbn>", methods=['GET'])
def api_request(isbn):
	'''this is api request of my website '''
	book_row =  db.execute("SELECT title, author, year, isbn,\
		COUNT(reviews.books_isbn) as review_count,\
		AVG(COALESCE(reviews.grid, 0)) as average_score \
		FROM books LEFT JOIN reviews ON books.isbn = reviews.books_isbn\
		WHERE isbn = :isbn \
		GROUP BY title, author, year, isbn", {"isbn" :isbn})
	book_row = book_row.fetchall()
	print(f"book_row {book_row}")
	if len(book_row) == 0:
		abort(404)
	else:
		for n in book_row:
			book_dict = {
			    "title": n[0],
			    "author": n[1],
			    "year": n[2],
			    "isbn": n[3] ,
			    "review_count": n[4],
			    "average_score":  float(n[5])
			    }
	return jsonify(book_dict)
