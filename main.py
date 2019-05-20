#!/usr/bin/python3

import argparse
import configparser
try: # pour l'import des wordlist dans le fichier de config
    import json
except ImportError:
    import simplejson as json

import scraping as scrp
import sites
import twitter as twt

global operation_realisee
total_coeffs = 0


def init_config(config_file_name):
	config=configparser.ConfigParser()
	config.read(config_file_name)
	log_filename = config['LOG']['LOG_FILE']
	wordlist = json.loads(config['ANALYSIS']['WORDLIST'])
	moderation = json.loads(config['ANALYSIS']['MODERATION'])
	twitterapifile = config['TWEEPY']['API_FILE']
	return(log_filename,wordlist,twitterapifile)

def count_total_coeff(wordlist):
	global total_coeffs
	for word in wordlist:
		total_coeffs += word['coef']
	return total_coeffs

def get_dept_in_csv(session,dept,wordlist,csv_writer):
	liste_communes = scrp.get_dept(session,dept)

	for commune in liste_communes:
		results=scrp.get_commune(session,commune,dept)
		results.append(sites.analyse_site(results[6],wordlist))
		# results.extend(twt.get_note(twitter_api,results[2],results[0],results[1],wordlist)) 
		scrp.write_to_csv(csv_writer,results)
		# print(results)

#---------------------------------------------------------------------------------------------------------------------
# MAIN PROCESS
#---------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	global operation_realisee
	
	#Instantiate the parser
	parser = argparse.ArgumentParser(description='Script pour La Bascule IDF\nscraping des mairies en IDF.')
	parser.add_argument('--config', required=True, help='required config file')
	parser.add_argument('--log', '-l', help='log file, default : log.txt', default='log.txt')
	parser.add_argument('-d', type=str, help='Département à gérer')
	args = parser.parse_args()

	# operation_realisee=str(input("Opération réalisée : "))
	print('using config file : '+str(args.config)+' and logging to : '+args.log)

	#init config file
	(log_filename,wordlist,twitterapifile) = init_config(args.config)
	total_coeffs = count_total_coeff(wordlist)

	
	#init scraping Twitter
	(twitter_api) = twt.init_twitter(twitterapifile,total_coeffs,log_filename)
	#init scraping site
	sites.initsite(total_coeffs,log_filename)

	if(args.d):
		#scraping DB
		(session,csv_writer) = scrp.initscrp(args.config,args.d,log_filename)
		get_dept_in_csv(session,args.d,wordlist,csv_writer)
	else:
		#init scraping DB
		(session,csv_writer) = scrp.initscrp(args.config,'all',log_filename) # only log all in one CSV file
		for dept in [77,78,91,92,93,94,95]:
			get_dept_in_csv(session,str(dept),wordlist,csv_writer)

	# sites.analyse_site('http://www.avernes95.fr',wordlist)
	# print(sites.analyse_site('http://www.vaujours.fr',wordlist))
	# sites.inspect_page('http://www.vaujours.fr/-Les-espaces-natures-',wordlist)
	# sites.inspect_page('http://www.vaujours.fr/Collecte-des-dechets',wordlist)
	
