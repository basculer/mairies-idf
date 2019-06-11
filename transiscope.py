#!/usr/bin/python3

from requests_html import HTMLSession
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# import time
# from selenium.webdriver.common.keys import Keys
import argparse
try:
    import json
except ImportError:
    import simplejson as json

def seleget_FH(url):
	options = Options()
	# options.add_argument("--headless")
	options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0")
	options.add_argument("token=a730b2dc-86a5-4a02-b667-0b1dbc1cc5a6")
	options.headless = True
	driver = webdriver.Firefox(options=options)
	print("### Firefox Headless Browser Invoked")
	driver.get(url)
	time.sleep(10)
	# elem = driver.find_element_by_id("menu")
	print(driver.page_source)
	driver.quit()

def get_projects(transiscope, city_code):
	city_projects = []
	for elmt in transiscope['data']:
		if("postalCode" in elmt['address']):
			if(elmt['address']['postalCode']==city_code):
				city_projects.append(elmt)
	return city_projects

def parse_json(transiscope):
	'''ORGA DU JSON : 
		- licence
		- ontology
		- data[] :
			- id
			- name
			- geo{}
			- sourceKey
			- address{}
				- streetAddress
				- addressLocality
				- postalCode
				- addressCountry
			- createdAt
			- updatedAt
			- categories[]
			- addressString
			- abstract
			- website
			- tags[]
	'''
	for elmt in transiscope['data']:
		if("postalCode" in elmt['address']):
			print(elmt['address']['postalCode'])

def init_trans(db_filename):
	with open(db_filename, 'r') as file_db:
		transiscope = json.load(file_db)
	return transiscope,HTMLSession()



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Script pour récupérer infos du transiscope')
	parser.add_argument('--db',help='required JSON file for testing')
	args = parser.parse_args()
	(transiscope,session) = init_trans(args.db)
	# parse_json(transiscope)	
	project_list = get_projects(transiscope,'95400')
