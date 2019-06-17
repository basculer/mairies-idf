#!/usr/bin/python3

from requests_html import HTMLSession
import argparse
try:
    import json
except ImportError:
    import simplejson as json

def get_score(project_list, wordlist):
	score = 0
	for project in project_list:
		# print(project)
		if('tags' in project):
			if('Écologie' in project['tags']):
				score += 2
			if('Agrimentation' in project['tags']):
				score += 2
		if('abstract' in project):
			for word in wordlist:
				if(word in project['abstract']):
					score+=1
	# print(score)
	return(len(project_list),score)


# returns a list of projects
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
		if("postalCode" in elmt['address'] and 'tags' in elmt):
			print(str(elmt['address']['postalCode'])+' : '+str(elmt['tags']))

def init_trans(db_filename):
	with open(db_filename, 'r') as file_db:
		transiscope = json.load(file_db)
	return transiscope

def get_city(transiscope, code,wordlist):
	project_list = get_projects(transiscope,code)
	transiscore,score_ecolo = get_score(project_list,wordlist)
	return [transiscore, score_ecolo]

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Script pour récupérer infos du transiscope')
	parser.add_argument('--db',help='required JSON file for testing')
	args = parser.parse_args()
	transiscope = init_trans(args.db)
	parse_json(transiscope)	
	project_list = get_projects(transiscope,'95400')
	wordlist = ['écologie','nature','transition','bio','biodiversité']
	get_score(project_list, wordlist)
