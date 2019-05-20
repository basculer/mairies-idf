#!/usr/bin/python3

import tweepy
import configparser 	#pour la modularite
try:
    import json
except ImportError:
    import simplejson as json
import csv

config_file = 'config.ini'

def get_note(api,name,code,wordlist):
	print('start Twitter : '+name)
	raw_score = get_raw_search(api,name,code,wordlist)
	print(raw_score)
	# get_users(api,name,code)


def init_twitter(config_file_name):
	global config_file
	config_file = config_file_name
	global_config=configparser.ConfigParser()
	global_config.read(config_file_name)
	twitter_api_file_name = global_config['TWEEPY']['API_FILE']
	print('Using Twitter API file : '+twitter_api_file_name)

	wordlist = json.loads(global_config['ANALYSIS']['WORDLIST'])
	moderation = json.loads(global_config['ANALYSIS']['MODERATION'])

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

def get_raw_search(api,name,code,wordlist):
	query = " ".join([word['name'] for word in wordlist])
	score = 0
	for word in wordlist:
		count = keyword_count(api,name+' '+word['name']+' since:2014-04-30 -filter:retweets')
		score += count*word['coef']
	return score

def keyword_count(api,query):
	'''gerer les RT'''
	tweet_list = api.search(query,lang='fr',rpp=100)
	return(len(tweet_list))

def get_users(api,name,code):
	api.search_users('name'+'code')