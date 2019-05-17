#!/usr/bin/python3

from requests_html import HTMLSession	# pour le crawling
from collections import Counter 		# pour les stats
import configparser 					#pour la modularite
try: # pour l'import des wordlist dans le fichier de config
    import json
except ImportError:
    import simplejson as json

configfile = 'config.ini'

def initsite(configfilename):
	global configfile
	configfile = configfilename
	config=configparser.ConfigParser()
	config.read(configfilename)
	wordlist = json.loads(config['ANALYSIS']['WORDLIST'])
	moderation = json.loads(config['ANALYSIS']['MODERATION'])
	# print(wordlist[0]['name'] + ':'+str(wordlist[0]['coef']))
	return(HTMLSession(),wordlist,moderation)

def parse_site(session,url):
	page = session.get(url)
	links = page.html.find('a[href]')
	for link in links:
		if link : print(link.links.pop())

#XPATH ? ou search/searchall
