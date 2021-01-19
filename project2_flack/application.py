import os
import requests

import os.path
# import socket

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

from pathlib import Path

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

lim_messages = 100
saved_channels = {}
saved_channels["General"] = []
users = ["user1"]
download_folder = "./downloads_s"

@app.route("/")
def index():
    # return "Project 2: TODO"
    return render_template("index.html")#, all_messages= saved_messages)

@socketio.on('connect')
def connect():
	''' load existing channels to the page '''
	emit("load existing channels", {"existing_channels":saved_channels}) #добавить загрузку файлов

@socketio.on('new user is login')
def new_user_login(data):
	''' add new user '''
	# print(f'user = {data}')
	flag = True
	if data["new_user"] in users:
		flag = False
	else:
		users.append(data["new_user"])
	emit("user exists alert", flag)

@socketio.on('one channel data')
def one_chan_data(data):
	'''loading messages for one  active channel '''
	if len(saved_channels[data['active_channel']]) != 0:
		channel_messages = saved_channels[data['active_channel']]
		for msg in channel_messages:
			if msg['message_type'] == 'file' and msg['file_info']['file_type'] in('image/png','image/jpeg'):
				print(f"имя файла = {msg['message']}")
				download_file= open_file(msg['message'])
				msg['file'] = download_file
		emit("load one channel",\
				{"one_channel_data":saved_channels[data['active_channel']]})

@socketio.on("try_upload_file")
def message(data):
	'''save file in to server '''
	if not os.path.exists(download_folder): #checking folder existence
		os.mkdir(download_folder)
	print(data['fix_active_channel'])
	file_info = {#'file_name': data['file_name'], \
				'file_size': data['file_size'],\
				'file_type': data['file_type']}
	write_in_sved_chnnls(data["fix_active_channel"], 
						data['print_name'],\
						data['print_date'],
						data['file_name'], 
						data["message_type"], file_info)
	print(saved_channels)
	f = open(download_folder+'/'+data['file_name'], 'wb')
	f.write(data['file_data'])

	emit("load file", {"file_name": data['file_name'], \
						"message_type": data['message_type'], \
						"file":data['file_data'], \
						"file_type": data['file_type'],\
						"file_size": data['file_size'],\
						"active_channel":data["fix_active_channel"], \
						"print_date" : data['print_date'],\
						"print_name" : data['print_name']},\
						broadcast=True)
	f.close()
	emit("channel blincking", data["fix_active_channel"], broadcast=True)

@socketio.on("submit message")
def message(data):
	'''add messages to the current channel '''
	# print(data)
	fix_active_channel = data["fix_active_channel"]
	write_in_sved_chnnls(data["fix_active_channel"], data['print_name'],\
						data['print_date'], data["print_message"], data["message_type"])

	emit("announce message", {'print_message':data["print_message"],\
	'print_name':data['print_name'],"print_date":data['print_date'],\
	'fix_active_channel': data["fix_active_channel"], \
	'message_type': data["message_type"]},\
	broadcast=True)
	emit("channel blincking", fix_active_channel, broadcast=True)

@socketio.on("submit channel")
def new_channel(data):
	'''check existing channels and create new channel '''
	new_channel_ = data["selection"]
	if new_channel_ in saved_channels:
		emit("channel exists alert")
	else:
		saved_channels[new_channel_]=[]
		emit("announce channel", {"selection": new_channel_}, broadcast=True)

@socketio.on("delete user from users list")
def del_logout_user(data):
	'''logout user from the chat '''
	print(data)
	print(f'user list before logout = {users}')
	for name in data:
		print(f'what is this ? = {data[name]}')
		users.remove(data[name])
	print(f'user list after logout = {users}')

@socketio.on('I need file')
def file_from_server(data):
	'''send file on request'''
	print(f"maybe this is file name = {data['name_file']}")
	f = open(download_folder+'/'+ data["name_file"], 'rb')
	fix_active_channel = data["fix_active_channel"]
	#f.read()
	# file_contents = data = Path(download_folder+'/'+ data["name_file"]).read_bytes()
	file_contents = f.read()
	print(f"file_contents len = {len(file_contents)}")
	# print(f"file = {file_contents}")
	for ch_info in saved_channels[fix_active_channel]:
		print(ch_info)
		if ch_info['message_type'] == 'file' and ch_info['message'] == data["name_file"]:
			emit("send file from server", {"file":file_contents,\
											"file_name": data["name_file"], \
											"file_type": ch_info['file_info']['file_type'],\
											"file_size": ch_info['file_info']['file_size']})
	f.close()

def write_in_sved_chnnls(fix_active_channel, print_name, print_date, \
						print_message, message_type,file_info="null"):
	'''this function write all information in dictionary saved_channels'''
	if len(saved_channels[fix_active_channel]) == lim_messages:
		saved_channels[fix_active_channel].pop(0)
	if message_type == "text":
		saved_channels[fix_active_channel].append({'user': print_name,\
													'data': print_date,\
													'message': print_message\
													,'message_type': message_type\
												})
	else:
		saved_channels[fix_active_channel].append({'user': print_name,\
													'data': print_date,\
													'message': print_message\
													,'file_info': file_info\
													,'message_type': message_type\
												})

def open_file(name_file):
	f = open(download_folder+'/'+ name_file, 'rb')
	file_contents = f.read()
	return file_contents