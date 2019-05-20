#!/usr/bin/python3

import tweepy
import configparser 	#pour la modularite
try:
    import json
except ImportError:
    import simplejson as json
import csv

config_file = 'config.ini'
total_coeffs = 1

def get_note(api,name,code,name_short,wordlist):
	print('start Twitter : '+name)
	pertinence = 1
	if(name == ''):
		name = name_short
		pertinence = 0.5

	raw_score = get_raw_search(api,name,wordlist)
	userslist = get_users(api,name,code)
	officials_score = 0
	for user in userslist:
		# print(user.screen_name+ ' : '+user.name+' : '+ user.description)
		user_score = get_raw_search(api,'from:'+user.screen_name,wordlist) #une brilliante reutilisation de la fonction precedente
		officials_score += user_score/(userslist.index(user)+1)
	
	pertinence *= (1/(1+len(userslist)))
	#formule finale a revoir!!!
	# = 30 si tous les mots apparaissent 10 fois /100 et viennent d un compte officiel unique
	# score_twitter = ((10*raw_score+(20*officials_score/(len(userslist)+1)))/total_coeffs)
	score_twitter = ((10*raw_score+(20*officials_score))/total_coeffs)
	if (score_twitter > 20):
		score_twitter = 20
		pertinence/2
	return (score_twitter,float("{0:.2f}".format(pertinence)))


def init_twitter(config_file_name):
	global config_file, total_coeffs
	config_file = config_file_name
	global_config=configparser.ConfigParser()
	global_config.read(config_file_name)
	twitter_api_file_name = global_config['TWEEPY']['API_FILE']
	print('Using Twitter API file : '+twitter_api_file_name)

	wordlist = json.loads(global_config['ANALYSIS']['WORDLIST'])
	moderation = json.loads(global_config['ANALYSIS']['MODERATION'])
	for word in wordlist:
		total_coeffs += word['coef']

	twitter_config = configparser.ConfigParser()
	twitter_config.read(twitter_api_file_name)
	CONSUMER_KEY =twitter_config['API']['CONSUMER_KEY']
	CONSUMER_SECRET = twitter_config['API']['CONSUMER_SECRET']
	ACCESS_TOKEN = twitter_config['API']['ACCESS_TOKEN']
	ACCESS_SECRET = twitter_config['API']['ACCESS_SECRET']

	#authenticate on twitter
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	# Create the api to connect to twitter with your credentials
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
	return(api,wordlist)

def get_raw_search(api,name,wordlist):
	query = " ".join([word['name'] for word in wordlist])
	score = 0
	for word in wordlist:
		count = keyword_count(api,name+' "'+word['name']+'" since:2014-04-30 -filter:retweets')
		# count2 = keyword_count(api,code+' "'+word['name']+'" since:2014-04-30 -filter:retweets')
		# print(name+' : "'+word['name']+'" : '+str(count)+' with coeff '+str(word['coef']))
		score += ((count)*word['coef'])
	return score

def keyword_count(api,query):
	'''gerer les RT'''
	tweet_list = api.search(query,lang='fr',rpp=100)
	return(len(tweet_list))

def get_users(api,name,code):
	users = api.search_users('ville '+name)
	users.extend(api.search_users('mairie '+name))
	users.extend(api.search_users('maire '+name))
	users.extend(api.search_users('ville '+code))
	# users.extend(api.search_users(name)) #waaaaay too generic
	return users
