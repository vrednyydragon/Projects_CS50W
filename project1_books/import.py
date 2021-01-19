import os 
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# import psycopg2
# import sys

# Функция sqlalchemy.create_engine() создает новый экземпляр класса 
# sqlalchemy.engine.Engine который предоставляет подключение к базе данных.
engine = create_engine(os.getenv("DATABASE_URL"))
# создание scoped session что обеспечивает взаимодействие различных пользователей с
# базой данных и хранит все отдельно
db = scoped_session(sessionmaker(bind=engine))

books_table = '''CREATE TABLE IF NOT EXISTS books  
	 (isbn VARCHAR PRIMARY KEY NOT NULL,
	 title VARCHAR NOT NULL,
	 author VARCHAR NOT NULL,
	 year INTEGER NOT NULL
	 );
	'''
db.execute(books_table)
# print("Table books created successfully")

file = open("books.csv")
reader = csv.reader(file)
for isbn, title, author, year in reader:
	if not (isbn == "isbn" and title == "title" and author == "author" and year == "year"):
		db.execute("INSERT INTO books (isbn, title, author, year) \
		VALUES (:isbn, :title, :author, :year) ON CONFLICT (isbn) DO NOTHING",
		{"isbn": isbn, 
		"title": title,
		"author": author,
		"year": year})
print(f"Books imported to database.")		

users_table = '''CREATE TABLE IF NOT EXISTS users 
	 (name VARCHAR(20) NOT NULL,
	 email VARCHAR(30) PRIMARY KEY NOT NULL,
	 password VARCHAR(10) NOT NULL,
	 date_of_creation TIMESTAMP NOT NULL
	 );
	 '''
db.execute(users_table)
# print("Table users created successfully")

reviews_table = '''CREATE TABLE IF NOT EXISTS reviews  
	 -- (number_of_rew INT PRIMARY KEY NOT NULL,
	 (id serial PRIMARY KEY NOT NULL,
	 books_isbn VARCHAR REFERENCES books(isbn),
	 users_email VARCHAR REFERENCES users(email),
	 date_of_review TIMESTAMP NOT NULL,
	 review VARCHAR NOT NULL,
	 grid VARCHAR(10) NOT NULL
	 );
	 '''
db.execute(reviews_table)
# print("Table reviews created successfully")
db.commit() 
db.close() # close conection with db