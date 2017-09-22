import json
import requests
import StringIO
import sys
from elasticsearch import Elasticsearch
from elasticsearch import ElasticsearchException
from elasticsearch import helpers



'''
CityAnalyzer objects store "WeatherGuides" which
correspond to each location and categorize
cities by cloud_percentage,
humidity, temperature, and wind_speed
'''

class CityAnalyzer(object):
	def __init__(self, city_weather_guides = []):
		self.weather_guides = city_weather_guides
	def index_weather_guides(self):
		#All schemas/mappings
		#for the city_statistics index
		#are generated/created within
		#Elasticsearch.
		try:
			es = Elasticsearch(hosts = ["10.0.2.15"], http_auth = ('elastic', 'changeme'), port = 9200, request_timeout  = 2)
			if(not(es.indices.exists(index = "city_statistics"))):
				res = es.indices.create(index = 'city_statistics', body = 
				'''{
  					"settings": {
    					"number_of_replicas": 1,
						"number_of_shards": 3,
    					"analysis": {
      
    					},
	    				"refresh_interval": "1s"
  					},
  					"mappings": {
    					"city_statistics": {
      						"properties": {
        						"cloud_percentage": {
        							"type" : "float"
        						},
        						"humidity_percentage": {
        							"type": "float"
        						},
        						"temperature": {
        							"type": float
        						},
        						"wind_speed": {
        							"type" : float
        						}, 
        						"name": {
          							"type": "text"
        						},
        						"country": {
         							 "type": "text"
        						},

        					}
    					}		
  					}
				}''')
			else: 
				return False
		except ElasticsearchException as es1:
			print "Unable to authenticate or connect."

		#Weather data
		#for each city is indexed 
		#into Elasticsearch
		for entry in range(len(self.weather_guides)):
			headers = {
				"cloud_percentage": self.weather_guides[entry].overall_cloud_percentage,
				"humidity_percentage": self.weather_guides[entry].overall_humidity_percentage,
				"temperature": self.weather_guides[entry].overall_temperature,
				"wind_speed": self.weather_guides[entry].overall_wind_speed,
				"name": self.weather_guides[entry].name.split(',')[0],
				"country": self.weather_guides[entry].name.split(',')[1]
			}
			print headers
			try:
				response = es.index(index = "city_statistics", doc_type = "city", id = entry+1, body  = headers, request_timeout = 2)
			except ElasticsearchException as es1:
				print "Unable to authenticate or connect."
	def find_best_cities(self, preferred_cloud_percentage, preferred_humidity, preferred_temperature, preferred_wind_speed):
		#Function scoring/Decay functions
		#are used to determine the best 
		#cities by cloud_percentage, humidity, wind_speed,
		#and temperature
		try:
			es = Elasticsearch(hosts = ["10.0.2.15"],  http_auth=('elastic', 'changeme'),  port = 9200, request_timeout = 2)
		except ElasticsearchException as es1:
			print "Unable to authenticate or connect."
		query = {
			"from": 0,
			"size": 50,
			"query": {
        	"function_score": {
            	"gauss": {
                	"cloud_percentage": {
                      	"origin": preferred_cloud_percentage, 
                      	"scale": 5,
                      	"offset": 0, 
                      	"decay" : 0.5 
                	}
            	}
        	}
    	  }
		}


		try:
			addresses = open("cities_near_travelers.txt", 'w+')
		except IOError:
			print "Cities near travelers file not provided"
			return 0

		

		'''
		Best Cities by Cloud Percentage
		'''
		resp = {}
		try:
			resp = es.search(index = "city_statistics", body = query, request_timeout = 2)
		except elasticsearch.ElasticsearchException as es1:
			print es1


		addresses.write("\n\nBest Cities by Cloud Percentage: \n")
		for entry in range(len(resp['hits']['hits'])):
			addresses.write(resp['hits']['hits'][entry]['_source']['name'] + ' , ' + resp['hits']['hits'][entry]['_source']['country'] + "\n")


		


		query['query']['function_score']['gauss']['temperature'] = query['query']['function_score']['gauss'].pop('cloud_percentage')
		query['query']['function_score']['gauss']['temperature']['origin'] = preferred_temperature

		

		

		'''
		Best Cities by Temperature
		'''
		
		try:
			resp = es.search(index = "city_statistics", body = query, request_timeout = 2)
		except elasticsearch.ElasticsearchException as es1:
			print es1

		addresses.write("\n\nBest Cities by Temperature: \n")
		for entry in range(len(resp['hits']['hits'])):
			addresses.write(resp['hits']['hits'][entry]['_source']['name'] + ' , ' + resp['hits']['hits'][entry]['_source']['country'] + "\n")


		


		query['query']['function_score']['gauss']['humidity_percentage'] = query['query']['function_score']['gauss'].pop('temperature')
		query['query']['function_score']['gauss']['humidity_percentage']['origin'] = preferred_humidity



		

		'''
		Best Cities by Humidity Percentage
		'''
		try:
			resp = es.search(index = "city_statistics", body = query, request_timeout = 2)
		except elasticsearch.ElasticsearchException as es1:
			print es1
		addresses.write("\n\nBest Cities by Humidity Percentage: \n")
		for entry in range(len(resp['hits']['hits'])):
			addresses.write(resp['hits']['hits'][entry]['_source']['name'] + ' , ' + resp['hits']['hits'][entry]['_source']['country'] + "\n")

		






		query['query']['function_score']['gauss']['wind_speed'] = query['query']['function_score']['gauss'].pop('humidity_percentage')
		query['query']['function_score']['gauss']['wind_speed']['origin'] = preferred_wind_speed


	

		'''
		Best Cities by Wind Speed
		'''

		try:
			resp = es.search(index = "city_statistics", body = query, request_timeout = 2)
		except elasticsearch.ElasticsearchException as es1:
			print es1
		addresses.write("\n\nBest Cities by Wind Speed: \n")
		for entry in range(len(resp['hits']['hits'])):
			addresses.write(resp['hits']['hits'][entry]['_source']['name'] + ' , ' + resp['hits']['hits'][entry]['_source']['country'] + "\n")
		