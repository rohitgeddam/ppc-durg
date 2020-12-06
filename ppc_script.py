#!/usr/bin/python 

import os
import time
import webbrowser


URL = "http://localhost:8000/"
PROJECT_PATH = r"/"
# CHROME_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'


def print_start_line():
	print('*' * 20)

def open_web_browser():
	try:
		print("opening browser")
		webbrowser.open(URL, new=2)
	except:
		print("error occured")


def start_django_server():
	print("starting django server")

	os.system('cmd /c "python manage.py runserver" ')

	print("django server started")	


def change_to_project_directory():
	try:
		os.chdir(PROJECT_PATH)
	except:
		print("Failed to change directory please ensure PROJECT_PATH is correct")


change_to_project_directory()
print_start_line()
open_web_browser()
print_start_line()
start_django_server()