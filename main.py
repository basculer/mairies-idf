#!/usr/bin/python3

import argparse 		#pour que le script soit propre
import configparser 	#pour que le script soit modulable
import csv 				#pour écrire les résults
try: 					# pour l'import des wordlist dans le fichier de config
    import json
except ImportError:
    import simplejson as json
import datetime 		#pour logger

import scraping as scrp
import sites
import twitter as twt
import transiscope as trans

from requests_html import HTMLSession #pour recuperer la liste des villes


total_coeffs = 0


def init_config(config_file_name):
	config=configparser.ConfigParser()
	config.read(config_file_name)
	log_filename = config['LOG']['LOG_FILE']
	wordlist = json.loads(config['ANALYSIS']['WORDLIST'])
	moderation = json.loads(config['ANALYSIS']['MODERATION'])
	twitterapifile = config['TWEEPY']['API_FILE']
	transi_db_file = config['TRANSISCOPE']['DB_FILENAME']
	transi_wordlist = json.loads(config['TRANSISCOPE']['WORDLIST'])
	csv_dir = config['CSV']['CSV_DIR']
	csv_file = config['CSV']['CSV_FILE']
	return(log_filename,wordlist,twitterapifile,transi_db_file,transi_wordlist, csv_dir+csv_file)


def init_csv(csv_filepattern,dept):
	csv_filename = csv_filepattern+dept+'.csv'
	csv_writer = csv.writer(open(csv_filename,'w'))
	TITLES=['code postal','nom','nom','maire','numéro de la mairie','mail de la mairie','site de la mairie','adresse de la mairie','population','orientation du conseil municipal','étiquette du maire','étiquette du maire','circonscription','député','parti du député','not site','note twitter','pertinence twitter','nbre projets transiscopre','note écolo transiscope']
	csv_writer.writerow(TITLES)
	return csv_filename


def count_total_coeff(wordlist):
	global total_coeffs
	for word in wordlist:
		total_coeffs += word['coef']
	return total_coeffs

def get_dept_in_csv(dept,wordlist,csv_filename, transiscope,trans_wordlist):
	twitter_api = twt.get_twitter_api(twitter_auth)
	session_list = HTMLSession()
	liste_communes = scrp.get_dept(session_list,dept)
	session_list.close()
	for commune in liste_communes:
		get_commune_csv(csv_filename,commune,dept,wordlist,trans_wordlist,transiscope,twitter_api)
		# print(results)

def get_commune_csv(csv_filename,commune,dept, wordlist,trans_wordlist, transiscope,twitter_api):
	results=scrp.get_commune(commune,dept)
	results.append(sites.analyse_site(results[6],wordlist))
	results.extend(twt.get_note(twitter_api,results[2],results[0],results[1],wordlist)) 
	results.extend(trans.get_city(transiscope,results[0],trans_wordlist))
	write_to_csv(csv_filename,results)


def write_to_csv(csv_filename,results):
	'''ecrit le tableau de resultat dans le fichier csv dont le nom est specifie ici'''
	csv_writer = csv.writer(open(csv_filename,'a'))
	csv_writer.writerow(results)


#---------------------------------------------------------------------------------------------------------------------
# MAIN PROCESS
#---------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	
	#recupere les arguments du programme
	parser = argparse.ArgumentParser(description='Script pour La Bascule IDF\nscraping des mairies en IDF.')
	parser.add_argument('--config', help='required config file', default='config.ini')
	parser.add_argument('--log', '-l', help='log file, default : log.txt', default='log.txt')
	parser.add_argument('-d', type=str, help='Département à gérer')
	args = parser.parse_args()

	print('Using config file : '+str(args.config)+' and logging to : '+args.log)

	#initie le fichier de config
	(log_filename,wordlist,twitterapifile,transi_db_file,transi_wordlist,csv_filepattern) = init_config(args.config)
	total_coeffs = count_total_coeff(wordlist)

	
	#initie le scraping Twitter
	(twitter_auth) = twt.init_twitter(twitterapifile,total_coeffs,log_filename)
	#initie le scraping site
	sites.initsite(total_coeffs,log_filename)

	#initie le fichier JSON du transiscope
	transiscope = trans.init_trans(transi_db_file)

	if(args.d):
		csv_filename = init_csv(csv_filepattern,args.d)
		scrp.initscrp(args.config,log_filename)
		get_dept_in_csv(args.d,wordlist,csv_filename,transiscope,transi_wordlist)
	else:
		# dans ce cas-la, tous les resultats seront ecrits dans un unique CSV central
		scrp.initscrp(args.config,log_filename) 
		csv_filename = init_csv(csv_filepattern,'all')
		for dept in [77,78,91,92,93,94,95,75]:
			get_dept_in_csv(str(dept),wordlist,csv_filename,transiscope,transi_wordlist)
	flag = open('finish.txt','w')
	flag.write('finished at : '+str(datetime.datetime.now()))
	flag.close()

