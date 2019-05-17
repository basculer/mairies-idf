#!/usr/bin/python3

from requests_html import HTMLSession
from collections import Counter
import configparser 	#pour la modularite
import os				#pour supprimer les vieux csv
import csv 				#pour la tambouille
import datetime 		#pour logger

configfile = 'config.ini'
log_filename = 'log.txt'

def initscrp(configfilename,dept):
	global configfile,log_filename
	configfile = configfilename
	(csv_filename,log_filename)=init_csv(configfile)
	session = HTMLSession()
	return(session,csv_filename+dept+'.csv')

def get_dept(session,dept,csv_filename):
	page = session.get('https://www.mairie.biz/plan-mairie-'+dept+'.html')
	liste_communes = page.html.find('div.list-group>a')
	csv_file = open(csv_filename,'w')
	for commune in liste_communes:
		url = commune.html.split('href="/mairie-')[1].split('.html')[0]
		urlarray = url.split('-')
		code = urlarray[len(urlarray)-1]
		name = url.split('-'+dept)[0] #l'astuce de ouf
		print('scraping de '+name)
		results = [code,name]
		# print(name)

		## ici nous avons 4 sources differentes pour nos infos
		(ville,nom_maire3,telephone,email,site,adresse,population,conseil) = mon_maire_fr(session,name,dept)
		results.extend((ville,nom_maire3,telephone,email,site,adresse,population,conseil))
		
		(nom_maire2,bord_maire) = mairie_biz(session,url)
		results.append(bord_maire)
		
		(nom_maire1,circonscription,depute,bord_dep) = mairie_net(session,url)
		results.extend((circonscription,depute,bord_dep))
		
		# (adresse2,telephone2,email2,site2,population2) = annuaire_des_mairies_com(session,'vaujours','93')
		# results.extend((adresse2,telephone2,email2,site2,population2))
		write_to_csv(csv_file,dept,results)

def mairie_net(session, url):
	if('-st-' in url):
		url = url.replace('-st-','-saint-')
	if(url == 'noisy-le-sec-93134'):
		url = 'noisy-le-sec-93130'
	(nom_maire,circonscription,depute,politique) = ('','','','')
	try:
		page= session.get('https://www.mairie.net/local/mairies-villes-communes/mairie-'+url+'.htm')
		nom_maire = page.html.find('strong')[2].text
		par_depute = page.html.find('h3~p',clean=True)[2].text
		circonscription = par_depute.split('cette ',1)[1].split(' ')[0]
		depute = par_depute.split('est ',1)[1].split(' élu',1)[0]
		politique = par_depute.split('politique ',1)[1].split('.',1)[0]
	except IndexError:
		log_error(url,'mairie_net')
	return(nom_maire,circonscription,depute,politique)

def annuaire_des_mairies_com(session,name,dept):
	page=session.get('http://www.annuaire-des-mairies.com/'+dept+'/'+name+'.html')
	renseignements = page.html.find('tr.txt-primary.tr-last>td')
	(adresse,telephone,mail,site,population) = ('','','','','')
	try:
		adresse = renseignements[1].text
		telephone = renseignements[3].text
		mail = renseignements[7].text
		site = renseignements[9].text
		population = renseignements[13].text
	except IndexError:
		log_error(name+'-'+dept,'annuaire_des_mairies_com')
	return(adresse,telephone,mail,site,population)

def mairie_biz(session,url):
	page= session.get('https://www.mairie.biz/mairie-'+url+'.html')
	(nom,bord)=('','')
	try:
		maire = page.html.find('div.col-lg-4>strong~p')[0].text
		nom = maire.split(' (')[0]
		if maire.split('(') : bord = maire.split('(')[1].split(')')[0]
	except IndexError:
		log_error(url,'mairies_biz')
	return(nom,bord)

def mon_maire_fr(session,name,dept):
	if(name[1] == '-'):
		name = name[0]+name[2:]
	if('-st-' in name):
		name = name.replace('-st-','-saint-')
	page= session.get('http://www.mon-maire.fr/maire-de-'+name+'-'+dept)
	(ville,nom_maire,telephone,email,site,adresse,population,conseil3) = ('','','','','','','','')
	try:
		ville = page.html.find('title',first=True).text.split('de ',1)[1].split(' (')[0]
		nom_maire = page.html.find('b~span[itemprop=name]')[0].text
		if page.html.find('b~span[itemprop=telephone]') : telephone = page.html.find('b~span[itemprop=telephone]')[0].text
		if page.html.find('b~span[itemprop=email]') : email = page.html.find('b~span[itemprop=email]')[0].text
		if page.html.find('b~span[itemprop=url]') : site = page.html.find('b~span[itemprop=url]')[0].text
		adresse = page.html.find('b~span[itemprop=streetAddress]')[0].text
		population = page.html.find('div.constructeur')[0].text.split(': ')[2].split('\nDép')[0]
		conseil = page.html.find('td[class]')
		if conseil:
			conseil2 = []
			for elmt in conseil:
				conseil2.append(elmt.text)
			conseil3=Counter(conseil2).most_common(3)
	except IndexError:
		log_error(name+'-'+dept,'mon_maire_fr')
	return(ville,nom_maire,telephone,email,site,adresse,population,conseil3)

def write_to_csv(csv_file,dept,results):
	writer = csv.writer(csv_file)
	writer.writerow(results)

def init_csv(configfile):
	config=configparser.ConfigParser()
	config.read(configfile)
	csv_dir = config['CSV']['CSV_DIR']
	csv_file = config['CSV']['CSV_FILE']
	log_file = config['LOG']['LOG_FILE']
	# os.remove(csv_dir+csv_file+dept+'.csv')
	return(csv_dir+csv_file,log_file)

def log_error(addr,funct):
	print('######### Error dans la fonction '+funct+' du parsing de '+addr)
	logfile = open(log_filename, "a")
	logfile.write('######   ERROR : '+str(datetime.date.today())+'  #####\n')
	logfile.write('Error dans la fonction '+funct+' du parsing de '+addr+'\n')
	logfile.close()