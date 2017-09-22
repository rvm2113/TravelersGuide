import json
import requests
import StringIO
import sys
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from weather_guide import WeatherGuide
from city_analyzer import CityAnalyzer


'''
TravelGuide objects seek to determine
all airports within a certain
distance of each destination provided. 
Additionally, given a series
of traveler addresses and addresses to avoid,
the TravelGuide determines all
cities that are within a certain distance of the 
traveler addresses and beyond a certain distance
of the areas to avoid.

'''

class TravelGuide(object):

	def __init__(self, destinations_file = ' ', travelers_addresses_file = ' ', airport_distance = 0, avoid_areas_file = ' ', avoid_distance = 0, city_file = ' '):
		self.destinations = destinations_file
		self.travelers_addresses = travelers_addresses_file
		self.avoid_areas = avoid_areas_file
		self.distance = airport_distance
		self.distance_avoid = avoid_distance
		self.city_preferences = city_file



	# The Google Geocoding API
	# is used to convert the given address to 
	# a list of longitude of latitude.
	def geocode(self, address):
		api_key = 'AIzaSyBxQz8JecvI5q2RyaDLArP-WfitxwQFo8k'
		query_list = []
		query = {} 
		query['address'] = address
		query['key'] = api_key

		try:
			url = "https://maps.googleapis.com/maps/api/geocode/json"
			response = requests.get(url, query)
		except requests.exceptions.RequestException as error: 
			print error
			sys.exit(1)

		location = None
		if(len(response.json()['results']) == 0):
			print "Unable to geocode this address.."
		else:
			latitude = response.json()['results'][0]['geometry']['location']['lat']
			longitude = response.json()['results'][0]['geometry']['location']['lng']
			location = [longitude, latitude]
		return location



	#The function find_airports_near_destinations
	#seeks to find all airports within a 
	#user-determined distance of each 
	#provided destination
	def find_airports_near_destinations(self):
		search_arr = []
		try:
			addresses = open(self.destinations, 'r')
		except IOError:
			print "Destinations input file not provided"
			return 0
		lines = addresses.readlines()

		for x in range(len(lines)):
			#print lines[x]
			location = self.geocode(lines[x])
			if(location != None):
				search_arr.append({'index': 'transportation', 'type': 'station'})
				search_arr.append({
				"from": 0,
				"size": 50,
				"query": {
	  				"bool": {
	    	   			"must": {
	       		 			"match_all" : {}
	       	 			},
	       				"filter": {
	        				"geo_shape": {
	            				"location": {
	             					"shape": {
	                  					"type": "circle",
	                 					"radius": str(self.distance) + "km",
	                 					"coordinates": location
	             		 			},
	            					"relation": "within"
	        	    			}
	    	      			}
      	
	      				}
	   		 		}
	  		 	}
				}) 	 
		request = ""
		for req in search_arr:
			request+= '%s \n' %json.dumps(req)


		#Multiple queries
		#are executed in parallel
		#with usage of Elasticsearch's Multisearch Python API

		try:
			es = Elasticsearch(hosts = ["10.0.2.15"],  http_auth=('elastic', 'changeme'),  port = 9200, request_timeout = 2)
		except elasticsearch.ElasticsearchException as es1:
			print "Unable to Authenticate or connect."
		resp = es.msearch(body = request, request_timeout = 2)


		
		
		try:
			airport_file = open("airports_near_destinations.txt", 'w+')
		except IOError:
			print "Airports near destinations file not provided"
			return 0
		for y in range(len(resp['responses'])):
			airport_file.write("\n\n\n")
			airport_file.write("Airports within a "+ str(self.distance) + " km radius of: " + lines[y] + "\n" + "\n" + "\n")
			for x in range(len(resp['responses'][y]['hits']['hits'])):
				curr_response_parsed = resp['responses'][y]['hits']['hits'][x]['_source']['name'] + ' ' + resp['responses'][y]['hits']['hits'][x]['_source']['city'] 
				curr_response_parsed +=' ' + resp['responses'][y]['hits']['hits'][x]['_source']['country'] + "\n"
				airport_file.write(curr_response_parsed)
			print "\n" 


		print "\n"
		print "\n"
		print "\n"
		return resp
	



	#The function find_common_cities()
	#seeks to find all cities that are
	#within the geo_shape formed
	#by all traveler's addresses
	# and disjoint/outside of the 
	#circle geoshape formed 
	#by each area address to avoid.
	def find_common_cities(self):
		print self.travelers_addresses
		try:
			addresses = open(self.travelers_addresses, 'r')
		except IOError:
			print "Traveler addresses file not provided"
			return 0
		lines = addresses.readlines()
		print lines
		locations = [[]]
		first_location = []
		# Each provided address
		# is geocoded prior to execution
		# of the query
		for x in range(len(lines)):
			location = self.geocode(lines[x].rstrip())
			print location
			if(x==0):
				first_location = location
			locations[0].append(location)
			print locations
		locations[0].append(first_location)
		print locations


		#All traveler addresses form a geo_shape
		all_polygons = []	
		within_polygon = {
	 		"geo_shape": {
	    		"location": {
	        		"shape": {
	            		"type": "polygon",
	             		"coordinates": locations
	         		},
	   			"relation": "within"
	    		}
	  		}
		}
		all_polygons.append(within_polygon)
		print self.avoid_areas
		if(self.avoid_areas != ' '):
			try:
				avoid_addresses = open(self.avoid_areas, 'r')
			except IOError:
				print "Avoided areas file not provided/not found"
				return 0
			avoid_lines = avoid_addresses.readlines()
			for y in range(len(avoid_lines)):
				curr_location = self.geocode(avoid_lines[y])
				#print "CURRENT AVOID LOCATIONS: " + str(curr_location)
				#each address to avoid(if provided) forms a a geo_shape/circle
				curr_polygon = {
			 		"geo_shape": {
	    				"location": {
	        				"shape": {
	            				"type": "circle",
	            				"radius": str(self.distance_avoid) + "km",
	             				"coordinates": curr_location
	         				},
	   						"relation": "disjoint"
	    				}
	  				}

				}
				all_polygons.append(curr_polygon)

		print "All polygons: " 
		print "All Polygons: " + str(all_polygons)
		search_query = 	{
			"from": 0,
			"size": 50,
			"query": {
	  			"bool": {
	    	   		"must": {
	       			 	"match_all" : {}
	       	 		},
	       			"filter": all_polygons
	   		 	}
	  		}
		}

		try:
			es = Elasticsearch(hosts = ["10.0.2.15"],  http_auth=('elastic', 'changeme'),  port = 9200, request_timeout = 2)
		except elasticsearch.ElasticsearchException as es1:
			print "Unable to authenticate or connect."


		#Usage of the Python Elasticsearch Search API
		try:
			resp = es.search(index = "cities", body = search_query, request_timeout = 2)
		except elasticsearch.ElasticsearchException as es1:
			print es1
		#print "RESPONSE: " + str(resp)
		city_resp = resp['hits']['hits']
		city_list_names = []
		
		for city in range(len(city_resp)):
			city_list_names.append(city_resp[city]['_source']['name'] + ' , ' + city_resp[city]['_source']['country'])
		#print "CITY LIST NAMES: " + str(city_list_names)


		city_weather = []

		for curr_city in range(len(city_list_names)):
			wg = WeatherGuide(city_list_names[curr_city])
			wg.compute_aggregate_weather_information()
			#print "Weather Guide " + str(curr_city) + " : " + str(wg.overall_cloud_percentage) + "  ,  " + str(wg.overall_humidity_percentage) + " , " + str(wg.overall_temperature) + " , "+ str(wg.overall_wind_speed)
			city_weather.append(wg)

		#After weather data is stored for each city, cities
		# are categorized by a CityAnalyzer object
		ca = CityAnalyzer(city_weather)
		ca.index_weather_guides()

		try:
			city_preferences_resp = open(self.city_preferences, 'r')
		except IOError:
			print "City Preferences file not provided."
			return 0
		lines = city_preferences_resp.readlines()

		if(len(lines) == 4):
			ca.find_best_cities(float(lines[0].rstrip()), float(lines[1].rstrip()), float(lines[2].rstrip()), float(lines[3].rstrip()))



	