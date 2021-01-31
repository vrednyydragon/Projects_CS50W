# Project 2: Flack

Web Programming with Python and JavaScript

You can see the result of this work on youtube by the link: 
https://youtu.be/EF9xQjYz0Go

This project is an online messaging service using Flask, similar in spirit to Slack. Users will be able to sign into your site with a display name, create channels (i.e. chatrooms) to communicate in, as well as see and join existing channels. Once a channel is selected, users will be able to send and receive messages with one another in real time. 

***Personal Touch:*** 
- blincking non-active channels, if there messages come;
- sending files;
- sending images.

***Folders and files:***

- static  - folder that contains styles.css, index.js, download_pic.png, send_file.png.
- templates - folder that contains index.html.
- application.py, 
- .gitignore, 
- requirements.txt, 
- README.md

**How to run:**

- Download the project2_flack

- In a terminal window, navigate into your project2_flack directory

- Run pip3 install -r requirements.txt in your terminal window to make sure that all of the necessary Python packages are installed

- Set the environment variable FLASK_APP to be application.py. On a Mac or on Linux, the command to do this is export FLASK_APP=application.py. On Windows, the command is instead set FLASK_APP=application.py.

- Run _flask run_ to start up the Flask application

- If you navigate to the URL provided by Flask, you should see the start page of the application