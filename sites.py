#!/usr/bin/python3

from requests_html import HTMLSession	# pour le crawling
from collections import Counter 		# pour les stats
import configparser 					#pour la modularite
import datetime 						#pour logger
try: # pour l'import des wordlist dans le fichier de config
    import json
except ImportError:
    import simplejson as json

total_coeffs = 0
log_filename = 'log.txt'

def initsite(total_coeffs_global,log_file_name):
	global total_coeffs,log_filename
	# print(wordlist[0]['name'] + ':'+str(wordlist[0]['coef']))
	total_coeffs = total_coeffs_global
	log_filename = log_file_name

def analyse_site(url,wordlist):
	session = HTMLSession()
	links_list = parse_site(url,session)
	site_score = 0
	for link in links_list:
		site_score += inspect_page(link,wordlist,session)
	#site_score = 20 si tous les mots sont mentionnés sur un cinquième des pages
	score = 0
	if links_list : 
		score = site_score*5*20/(len(links_list)*total_coeffs)
	if score > 20 : score = 20
	return (float("{0:.3f}".format(score)))


def parse_site(url,session):
	links_list = []
	try:
		page = session.get(url)
		links = page.html.find('a[href]')
		url_short = url.split('.')[len(url.split('.'))-2]
		# print('url short : '+url_short)
		for link in links:
			if link.links : 
				if url_short in link.absolute_links.pop():
					links_list.append(link.absolute_links.pop())
	except:
		log_error(url,'get main page of website')
	return links_list

def inspect_page(url,wordlist,session):
	# print('page : '+url)
	session = HTMLSession()
	try:
		#marcherait aussi avec html
		page = session.get(url).text.split(' ')
		count = 0
		for word in wordlist:
			count += page.count(word['name'])*word['coef']
			# print(word['name']+' : '+str(count))
		return count
	except:
		log_error(url,'inspect website page')
		return 0



def log_error(addr,funct):
	'''logs a scraping/parsing error in the global variable-specified log file'''
	print('######### Error dans la fonction '+funct+' du parsing de '+addr)
	logfile = open(log_filename, "a")
	logfile.write('######   ERROR : '+str(datetime.date.today())+'  #####\n')
	logfile.write('Error dans la fonction '+funct+' du parsing de '+addr+'\n')
	logfile.close()