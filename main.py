#!/usr/bin/python3

import argparse
import configparser

import scraping as scrp
import sites
import twitter as twt

global operation_realisee



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

	#scraping DB
	(session,csv_writer) = scrp.initscrp(args.config,args.d)
	liste_communes = scrp.get_dept(session,args.d)
	#scraping Twitter
	(twitter_api,wordlist) = twt.init_twitter(args.config)
	for commune in liste_communes:
		results=scrp.get_commune(session,commune,args.d)
		results.extend(twt.get_note(twitter_api,results[2],results[0],results[1],wordlist)) 
		scrp.write_to_csv(csv_writer,results)
		print(results)
	
	
	#scraping site
	# (session,wordlist,moderation) = sites.initsite(args.config)
	# sites.parse_site(session,'http://www.avernes95.fr')
	
