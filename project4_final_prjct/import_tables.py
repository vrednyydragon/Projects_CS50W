# import os
# import time
# import requests

import os.path

from flask import Flask, jsonify, render_template, request,  session, flash, redirect, url_for, abort
from flask_socketio import SocketIO, emit

from pathlib import Path

from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Set up database
engine = create_engine('postgresql://healthyfood:Y24977c1@52.35.199.96:5432/healthyfoodbd')
db = scoped_session(sessionmaker(bind=engine))

users_table = '''CREATE TABLE IF NOT EXISTS users_login 
             (id_users serial PRIMARY KEY,
	    	 name text NOT NULL,
	    	 email text NOT NULL,
	    	 password text NOT NULL,
	    	 date_of_creation TIMESTAMP NOT NULL
	    	 );
	    	 '''
db.execute(users_table)

profile_table = '''CREATE TABLE IF NOT EXISTS users_profile(
                    id_profile INTEGER PRIMARY KEY REFERENCES users_login(id_users),
                    date_of_birth date NOT NULL,
                    gender text NOT NULL,
                    user_height numeric NOT NULL,
                    user_weight numeric NOT NULL,
                    type_of_food text NOT NULL,
                    activity_level numeric  NOT NULL
                    );
                    '''
db.execute(profile_table)

relation_user_meal = '''CREATE TABLE IF NOT EXISTS relation_user_meal(
                    id_relation serial PRIMARY KEY,
                    type_of_relation text NOT NULL
                    );
                    '''
db.execute(relation_user_meal)

users_meal_table = '''CREATE TABLE IF NOT EXISTS users_meal_additionals(
					table_id serial PRIMARY KEY,
                    id_users INTEGER REFERENCES users_login(id_users),
					id_meal INTEGER NOT NULL,
					relation_type INTEGER REFERENCES relation_user_meal(id_relation)
                    );
                    '''
db.execute(users_meal_table)

db.commit()
db.close()

